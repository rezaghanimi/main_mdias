# -*- coding: utf-8 -*-
{
    'name': "driver_plan",
    'summary': """funenc auto gen project""",
    'description': """
        funenc auto gen project
    """,

    'author': "crax",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '1.0',

    'depends': ['base', 'funenc_theme'],

    'data': [
        'security/ir.model.access.csv',
        "views/assets.xml",
        "views/driver_manage.xml",
        "views/root_menu.xml"
    ],

    'qweb': [
    ],
    'application': True
}