from odoo import api, fields, models, _
from datetime import datetime
from datetime import timedelta


class Warranty(models.Model):
    _name = 'warranty.request'
    _description = 'warrant app'
    _inherit = ['mail.thread']
    _rec_name = 'sequence_number'

    customer_id = fields.Many2one('res.partner', string="Customer",
                                  required=True, tracking=True,

                                  states={'draft': [('readonly', True),
                                                    ('required', False)],
                                          'invoice': [('readonly', True)],
                                          'to approve': [('readonly', True)],
                                          'approved': [('readonly', True)]
                                      , 'cancel': [('readonly', True)]}
                                  )
    date_request = fields.Date(string="Request date", default=datetime.today(),
                               tracking=True, states={'draft': [('readonly',
                                                                 False),
                                                                ('required',
                                                                 True)],
                                                      'invoice': [
                                                          ('readonly', True)],
                                                      'to approve': [
                                                          ('readonly', True)],
                                                      'approved': [
                                                          ('readonly', True)]
            , 'cancel': [('readonly', True)]})
    date_invoice = fields.Date(string="Purchase date", tracking=True,

                               states={'draft': [('readonly', False)],
                                       'invoice': [('required', True)],
                                       'to approve': [('readonly', True)],
                                       'approved': [('readonly', True)]
                                   , 'cancel': [('readonly', True)]})

    state = fields.Selection([('new', 'New'),
                              ('draft', 'Draft'),
                              ('invoice', 'Invoice'),
                              ('to approve', 'To Approve'),
                              ('approved', 'Approved'),
                              ('cancel', 'Cancel')]
                             , default='new', tracking=True)
    sequence_number = fields.Char(string='Order Reference',
                                  copy=False, readonly=True,
                                  default=lambda self: _('New'))
    address_street = fields.Char(string='Address',
                                 related="customer_id.street"
                                 , copy=False, readonly=True)
    address_city = fields.Char(string='',
                               related="customer_id.city",
                               copy=False, readonly=True)
    address_state_id = fields.Many2one(string='',
                                       related="customer_id.state_id",
                                       copy=False, readonly=True)
    address_zip = fields.Char(string='',
                              related="customer_id.zip",
                              copy=False, readonly=True)
    address_country_id = fields.Many2one(string='',
                                         related="customer_id.country_id",
                                         copy=False, readonly=True)
    company_id = fields.Char(string='',
                             related="customer_id.parent_id.name",
                             copy=False, readonly=True)

    product_name_id = fields.Many2one('product.template',
                                      domain=[('has_warranty'
                                               , '=', 'True')],
                                      states={'draft': [('readonly', False)],
                                              'invoice': [('required', True)],
                                              'to approve': [
                                                  ('readonly', True)],
                                              'approved': [('readonly', True)]
                                          , 'cancel': [('readonly', True)]})
    product_serial_id = fields.Many2one('stock.production.lot',
                                        states={'draft': [('readonly', False)]
                                            , 'invoice': [('required', True)],
                                                'to approve': [
                                                    ('readonly', True)],
                                                'approved': [('readonly', True)]
                                            , 'cancel': [('readonly', True)]})

    def filter_serials(self):
        print("test")

    @api.onchange('product_name_id')
    def _filter_serial_id(self):
        test = self.env['warranty.request'].search([('state', '=', 'invoice')
                                                    and (
                                                        'product_serial_id',
                                                        '!=',
                                                        False)])
        print(test)
        print(self.product_serial_id.name)
        return {
            'domain': {'product_serial_id': [('product_id.name', '=',
                                              self.product_name_id.name),
                                             ('name', 'not in',
                                              [i.product_serial_id.name for i in
                                               test])]}

        }

    warranty_period_form = fields.Integer(
        related='product_name_id.warranty_period')
    warranty_type_form = fields.Selection(
        related='product_name_id.warranty_type')

    date_expiration = fields.Date(compute="_compute_date_expiration",
                                  string='Expire', default=False)

    @api.depends('warranty_period_form', 'date_invoice')
    def _compute_date_expiration(self):
        if self.date_invoice:
            print("inside")
            for test in self:
                test.date_expiration = \
                    fields.Datetime.from_string(test.date_invoice) \
                    + timedelta(days=test.warranty_period_form)
        else:
            print("outside")
            self.date_expiration = False

    def action_draft(self):
        self.state = 'draft'
        test = self.env['stock.picking'].create({
            'name': self.sequence_number,
            'location_id': 8,
            'picking_type_id': 5,
            'location_dest_id': 38,
            'move_ids_without_package':
                [{'product_id': 23}]
            # 'product_uom_qty': 10,
            # 'product_uom': 1
        })
        test.action_confirm()



    def action_to_approve(self):
        self.state = 'to approve'




    def action_approved(self):
        self.state = 'approved'


    def action_cancel(self):
        self.state = 'cancel'

    def action_invoice(self):
        self.state = 'invoice'

    @api.model
    def create(self, vals):
        if vals.get('sequence_number', _('New')) == _('New'):
            vals['sequence_number'] = self.env['ir.sequence']. \
                                          next_by_code('warranty.request') or \
                                      _('New')
        response = super(Warranty, self).create(vals)
        return response
