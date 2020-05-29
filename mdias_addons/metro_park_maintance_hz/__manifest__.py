# -*- coding: utf-8 -*-
{
    'name': "metro_park_maintance_hz",
    'summary': """hz maintaince""",
    'description': """
        车辆检修
    """,

    'author': "crax",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        
        "views/assets.xml",
        "views/hz_frame.xml",
        "views/root_menu.xml"
    ],

    'qweb': [],

    'application': True
}