from odoo import api, fields, models
import hashlib
import hmac


class ProductProduct(models.Model):
    _inherit = 'product.product'
    product_rating = fields.Selection([
                     ('0', '0'),
                     ('1', '1'),
                     ('2', '2'),
                     ('3', '3'),
                     ('4', '4'),
                     ('5', '5')], string="Rating")
