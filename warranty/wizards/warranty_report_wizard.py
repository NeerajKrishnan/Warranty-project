from odoo import api, fields, models, _
from datetime import datetime
from datetime import timedelta


class WarrantyReport(models.TransientModel):
    _name = 'warranty.report.wizard'
    _description = 'Warranty Report'
    customer_id = fields.Many2one('res.partner')

