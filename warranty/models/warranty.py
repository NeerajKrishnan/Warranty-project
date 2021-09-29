from odoo import api, fields, models, _
from datetime import datetime
from datetime import timedelta


class Warranty(models.Model):
    _name = 'warranty.request'
    _description = 'warrant app'
    _inherit = ['mail.thread']
    _rec_name = 'sequence_number'
    sequence_number = fields.Char(string='Order Reference',
                                  copy=False, readonly=True,
                                  default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', required=True )
    invoice_id = fields.Many2one('account.move', required=True)
    invoice_date = fields.Date(related='invoice_id.invoice_date')
    product_from_invoice = fields.One2many(related='invoice_id.invoice_line_ids'
                                           )
    product_id = fields.Many2one('product.product', required=True)
    serial_number_id = fields.Many2one('stock.production.lot', required=True)
    requested_date = fields.Date(string="Requested Date",
                                 default=datetime.today(),
                                 readonly=True, required=True)
    warranty_expire_date = fields.Date(string='Expiration Date',
                                       compute='_compute_expiration_date')
    warranty_period_form = fields.Integer(related='product_id.warranty_period')
    state = fields.Selection([('first', ''), ('draft', 'Draft'),
                              ('to approve', 'To Approve'),
                              ('approved', 'Approved'),
                              ('received', 'Received'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             default='first')
    warranty_type =fields.Selection(related='product_id.warranty_type',
                                    store=True)
    trans_warranty_location = fields.Char(string='Warranty location',
                                          store=True)
    return_warranty_location = fields.Char(string="customer location",
                                           store=True)
    report_invoice_ref=fields.Char(related='invoice_id.name', store=True)
    report_product =fields.Char()
    report_serial = fields.Char(related='serial_number_id.name',store=True)
    report_customer =fields.Char(related='customer_id.name',store= True)

    @api.onchange('product_id')
    def _compute_expiration_date(self):
        if self.invoice_date:
            for test in self:
                test.report_product=test.product_id.read()[0]['partner_ref']
                test.warranty_expire_date = fields.Datetime.from_string(
                    test.invoice_date) + timedelta(
                    days=test.warranty_period_form)
        else:
            self.warranty_expire_date = False

    @api.onchange('customer_id')
    def filter_according_customer_id(self):

        return {
            'domain': {
                'invoice_id': [('partner_id.id', '=', self.customer_id.id),
                               ('move_type', '=', 'out_invoice')
                               ]}
        }

    @api.onchange('invoice_id')
    def filter_according_product_id(self):
        return {
            'domain': {
                'product_id': [('id', '=', self.product_from_invoice.
                                mapped("product_id.id")
                                )
                               , ('has_warranty', '=', True)
                               ]

            }
        }

    @api.onchange('product_id')
    def filter_lot_or_serial(self):
        test = self.env['stock.quant'].search([('location_id.id', '=', 5),
                                               ('quantity', '>', 0)
                                               ])

        return {
            'domain': {
                'serial_number_id': [('product_id.name', '=',
                                      self.product_id.name),
                                     ('name', 'in',
                                      [i.name for i in test.lot_id]),
                                     ]

            }
        }

    @api.model
    def create(self, vals):
        if vals.get('sequence_number', _('New')) == _('New'):
            vals['sequence_number'] = self.env['ir.sequence']. \
                                       next_by_code('warranty.request') or \
                                       _('New')
        response = super(Warranty, self).create(vals)
        return response

    def action_draft(self):
        self.state = 'draft'

    def action_to_approve(self):
        self.state = 'to approve'

    def action_approve(self):
        self.state = 'received'
        test = self.env['stock.quant'].search([('product_id.id', '='
                                                , self.product_id.id),
                                               ('lot_id.name', '=',
                                                self.serial_number_id.name),
                                               ('quantity', '>', 0),
                                               ('location_id.id', '=', 5)
                                               ])
        if self.product_id.warranty_type == 'replacement_warranty':
            trans = self.env['stock.picking'].create({
                'picking_type_id': 5,
                'location_id': 5,
                'location_dest_id': 39,
                'move_lines': [(0, 0, {
                    'name': 'REC' + self.sequence_number,
                    'product_id': test.product_id.id,
                    'product_uom':  test.product_id.uom_id.id,
                     'lot_ids': [{ test.lot_id.id}],
                    'product_uom_qty': 1
                })]
            })
            self.trans_warranty_location = trans.name
            trans.action_confirm()
            trans.button_validate()
        if self.product_id.warranty_type == 'service_warranty':

            trans = self.env['stock.picking'].create({
                'picking_type_id': 5,
                'location_id': 5,
                'location_dest_id': 38,
                'move_lines': [(0, 0, {
                    'name': 'REC' + self.sequence_number,
                    'product_id': test.product_id.id,
                    'product_uom':  test.product_id.uom_id.id,
                    'lot_ids': [{ test.lot_id.id}],
                    'product_uom_qty': 1
                })]
            })
            self.trans_warranty_location = trans.name
            trans.action_confirm()
            trans.button_validate()


    def action_return_product(self):
        self.state = 'done'
        if self.product_id.warranty_type == 'replacement_warranty':
            print("self")
            test = self.env['stock.quant'].search([('product_id.id', '='
                                                , self.product_id.id)
                                                  ,
                                               ('lot_id.name', '=',
                                                self.serial_number_id.name)
                                                  ,
                                               ('quantity', '>', 0)
                                                  ,
                                               ('location_id.id', '=', 39)
                                               ])
            product_id_id = test.product_id
            serial_id_id = test.lot_id
            trans = self.env['stock.picking'].create({
                'picking_type_id': 5,
                'location_id': 39,
                'location_dest_id': 5,
                'move_lines': [(0, 0, {
                'name': 'REP' + self.sequence_number,
                'product_id': product_id_id.id,
                'product_uom': product_id_id.uom_id.id,
                'lot_ids': [{serial_id_id.id}],
                'product_uom_qty': 1
            })]
            })
            self.return_warranty_location=trans.name
            trans.action_confirm()
            trans.button_validate()
        if self.product_id.warranty_type == 'service_warranty':
            test = self.env['stock.quant'].search([('product_id.id', '='
                                                , self.product_id.id)
                                                  ,
                                               ('lot_id.name', '=',
                                                self.serial_number_id.name)
                                                  ,
                                               ('quantity', '>', 0)
                                                  ,
                                               ('location_id.id', '=', 38)
                                               ])
            product_id_id = test.product_id
            serial_id_id = test.lot_id

            trans = self.env['stock.picking'].create({
                'picking_type_id': 5,
                'location_id': 38,
                'location_dest_id': 5,
                'move_lines': [(0, 0, {
                'name': 'RET' + self.sequence_number,
                'product_id': product_id_id.id,
                'product_uom': product_id_id.uom_id.id,
                'lot_ids': [{serial_id_id.id}],
                'product_uom_qty': 1
            })]
            })

            self.return_warranty_location=trans.name
            trans.action_confirm()
            trans.button_validate()

    def preview_stock_move(self):
        return {
            'name': _('Stock Move'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('name','in',[self.trans_warranty_location,
                                     self.return_warranty_location])]
        }
    def action_cancel(self):
        self.state = 'cancel'
