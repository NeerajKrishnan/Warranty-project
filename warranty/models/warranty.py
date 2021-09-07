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
    customer_id = fields.Many2one('res.partner')
    invoice_id = fields.Many2one('account.move')
    invoice_date = fields.Date(related='invoice_id.invoice_date')
    product_from_invoice = fields.One2many(related='invoice_id.invoice_line_ids'
                                           )
    product_id = fields.Many2one('product.template')
    serial_number_id = fields.Many2one('stock.production.lot')
    requested_date = fields.Date(string="Requested Date",
                                 default=datetime.today(),
                                 readonly=True)
    warranty_expire_date = fields.Date(string='Expiration Date',
                                       compute='_compute_expiration_date')
    warranty_period_form = fields.Integer(related='product_id.warranty_period')
    state = fields.Selection([('first', ''), ('draft', 'Draft'),
                              ('to approve', 'To Approve'),
                              ('approved', 'Approved'), ('cancel', 'Cancel')],
                             default='first')

    @api.depends('invoice_date')
    def _compute_expiration_date(self):
        if self.invoice_date:
            for test in self:
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
                               ('name', 'ilike', 'INV/')
                               ]}
        }

    @api.onchange('invoice_id')
    def filter_according_product_id(self):
        print([i.product_id.id for i in self.product_from_invoice])
        return {
            'domain': {
                'product_id': [('name', '=', [i.product_id.name
                                              for i in self.product_from_invoice
                                              ]),
                               ('has_warranty', '=', True)
                               ]

            }
        }

    @api.onchange('product_id')
    def filter_lot_or_serial(self):
        return {
            'domain': {
                'serial_number_id': [('product_id.name', '=',
                                      self.product_id.name)]

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
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancel'
