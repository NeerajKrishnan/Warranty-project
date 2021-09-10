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
    'depends': ['product',
                'barcodes',
                'digest',
                'website_slides',
                'hr',
                'mail',
                'sale',
                'account',
                'purchase',
                'stock',
                'mrp',
                'resource'
                ],

    'data': [
        'security/ir.model.access.csv',
        'views/milestonetask.xml'
        ,'views/saleorder.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
