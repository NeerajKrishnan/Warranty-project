# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Payment Link',
    'version': '14.0.1.0',
    'summary': 'Payment Link',
    'sequence': -200,
    'description': """ Payment Link  """,
    'website': 'https://www.cybrosys.com/',
    'depends': ['account',
                'sale',
                'purchase',
                'mail',
                'website_slides'
                ],

    'data': [
        'security/ir.model.access.csv',
        'views/payment_link.xml',
        'data/mail_template.xml'


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
