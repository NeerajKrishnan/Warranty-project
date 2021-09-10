from odoo import api, fields, models, _


class Invoicing(models.Model):
    _inherit = "account.move"
    test = fields.Many2many('warranty.request.filter', compute='filters')
    @api.depends('test')
    def filters(self):
        self.env['warranty.request.filter'].search([]).unlink()
        list = []
        for rec in self:
            temp = rec.env['warranty.request'].search([('invoice_id.name', '=',
                                                        rec.name)])
            for i in temp:
                value = {
                    'inv_id': i.id,
                    'product_id': i.product_id.id,
                    'requested_date': i.requested_date


                }
                list.append([0,0,value])
            rec.test = list








