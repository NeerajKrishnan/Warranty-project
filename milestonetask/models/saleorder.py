from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    x = fields.Char(string="Milestone")