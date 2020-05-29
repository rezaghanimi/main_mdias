# -*- coding: utf-8 -*-
{
    'name': "metro_park_interlock",
    'summary': """联锁模块""",
    'description': """联锁表数据""",
    'description': """
        funenc auto gen project
    """,

    'author': "funenc",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '1.0',

    'depends': ['base', 'metro_park_base'],

    'data': [
        'security/ir.model.access.csv',
        "views/root_menu.xml",
        "views/interlock_route.xml",
        "views/interlock_table.xml",
        "views/interlock_import_wizard.xml",
        "views/interlock_route_test.xml",
        "views/assets.xml",
        'views/route_cache.xml',
        'views/sub_route_info.xml'],

    'qweb': [
        "static/xml/misc.xml"
    ],

    'application': True
}
