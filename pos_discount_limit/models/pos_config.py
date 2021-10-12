from odoo import api, fields, models
import hashlib
import hmac


class ProductProduct(models.Model):
    _inherit = 'pos.config'
    discount_limit = fields.Integer(string="Discount Limit")
