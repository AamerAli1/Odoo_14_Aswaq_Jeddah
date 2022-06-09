# -*- coding: utf-8 -*-
{
    'name': 'Custom POS Module',
    'version': '15.0.1',
    'category': 'Account',
    'author': 'SL TECH ERP SOLUTION',
    'website': 'https://www.sltecherpsolution.com',
    'summary': 'Custom POS Module',
    'description': """
        Custom POS Module
     """,
    'depends': [
        'point_of_sale', 'l10n_gcc_pos', 'l10n_sa_pos',
    ],
    'data': [
        'data/data.xml',
        'views/pos_order.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
        'static/src/xml/reciept.xml'
    ]
}
