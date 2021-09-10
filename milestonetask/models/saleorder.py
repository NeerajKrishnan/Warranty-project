from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    milestone= fields.Integer(string='Milestone')

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def action_create_project(self):
             project_template2 = self.env['project.project'].create({
            'name': self.name,
            'active': True
             })
             avoid_repeat = []
             parent_task=[]
             temp_sale_order=self.order_line
             for i in temp_sale_order:
                 if not (i.milestone in avoid_repeat):
                     avoid_repeat.append(i.milestone)
             for i in avoid_repeat:
                 p_task =self.env['project.task'].create(
                     {
                         'name': 'Milestone - '+str(i),
                         'project_id': project_template2.id
                     }
                 )
                 parent_task.append([i,p_task.id])
             for i in temp_sale_order:
                 for k in parent_task:
                     if i.milestone == k[0]:
                        p_task = self.env['project.task'].create(
                        {
                         'name': 'Milestone - ' + str(i.milestone)+" "+i.product_id.name,
                         'project_id': project_template2.id,
                         'parent_id': k[1]
                        }
                      )


