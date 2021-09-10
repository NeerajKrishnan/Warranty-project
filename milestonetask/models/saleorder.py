from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    milestone= fields.Integer(string='Milestone')

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def action_create_project(self):
             project_template2 = self.env['project.project'].create({
            'name': self.name,
            'active': True,  # this template is archived
        })



