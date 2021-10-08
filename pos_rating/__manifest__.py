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
        'views/test.xml',
        'views/test_1.xml'

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/js_linker.xml',
        'views/product_product.xml'


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
