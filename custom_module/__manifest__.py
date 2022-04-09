# -*- coding: utf-8 -*-
{
    'name': 'POS Global Sequence',
    'description' : 'Global sequence for POS sessions',
    'version': '15.0.1',
    'category': 'Account',
    'summary': 'Custom POS Module',
    'description': """
        Custom POS Module
     """,
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'data/data.xml',
        'views/pos_order.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ]
}
