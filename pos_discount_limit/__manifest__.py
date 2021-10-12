# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Rating',
    'version': '14.0.1.0',
    'summary': 'POS Rating',
    'sequence': -200,
    'description': """ POS Rating App """,
    'website': 'https://www.cybrosys.com/',
    'depends': ['sale','point_of_sale'
                ],
    'qweb':[
        'static/src/xml/error.xml',
    ],
    'data': [
        'static/src/xml/discount.xml',
        'views/pos_config.xml'


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
