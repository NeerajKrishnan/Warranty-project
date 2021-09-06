from odoo import api, fields, models, _
from datetime import datetime
from datetime import timedelta


class WarrantyFilter(models.Model):
    _name = 'warranty.request.filter'
    _description = 'warrant filtering'
    warranty_filter_id =fields.Many2one('warranty.request')
    product_id = fields.Many2one('product.template')
