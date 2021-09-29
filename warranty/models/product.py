from odoo import api, fields, models, _


class Product(models.Model):
    _inherit = "product.product"
    has_warranty = fields.Boolean("Has Warranty")
    warranty_period = fields.Integer(string="Warranty Period(Days)", size=10)
    warranty_type = fields.Selection([('service_warranty', 'Service Warranty'),
                                     ('replacement_warranty',
                                      'Replacement warranty')]
                                     , default='service_warranty')






