# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Milestone TasksTasks',
    'version': '14.0.1.0',
    'summary': 'milestone tasks',
    'sequence': -200,
    'description': """
Milestone mangement software
   """,
    'website': 'https://www.cybrosys.com/',
    'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/milestone_task.xml',


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
