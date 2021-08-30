from odoo import api, fields, models, _


class WarrantyProduct(models.Model):
    _inherit = "product.template"
    has_warranty = fields.Boolean("Has Warranty")
    warranty_period =fields.Integer(string="Warranty Period(in Days)" ,size=10)
    warranty_type = fields.Selection([('service_warranty', 'Service Warranty'),
                                     ('replacement_warranty',
                                      'Replacement warranty')])





