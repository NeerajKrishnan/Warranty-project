from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    milestone = fields.Integer(string='Milestone')



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_create_project(self):
        project = self.env['project.project'].create({
        'name': self.name,
        'active': True
        })
        parent_task_list = list(set(self.order_line.mapped('milestone')))
        for task in parent_task_list:
            parent_task = self.env['project.task'].create(
                           {
                             'name': 'Milestone - '+str(task),
                             'project_id': project.id
                           })
            for sub_task in self.order_line:
                if task in sub_task.mapped('milestone'):
                    self.env['project.task'].create(
                                {
                                'name': sub_task.product_id.name + str(task),
                                'project_id': project.id,
                                'parent_id':  parent_task.id
                                })
