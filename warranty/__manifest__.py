# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Warranty',
    'version': '14.0.1.0',
    'summary': 'Warranty App',
    'sequence': -100,
    'description': """
Warranty management software
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
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizards/report_wizard.xml',
        'data/cron.xml',
        'views/product.xml',
        'views/warranty.xml',
        'data/Inventory.xml',
        'views/invoicing.xml',
'views/action_manager.xml',
'report/report.xml',
'report/report_template.xml',


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
