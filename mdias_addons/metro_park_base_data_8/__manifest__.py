# -*- coding: utf-8 -*-
{
    'name': "metro_park_base_data_8",
    'summary': """funenc auto gen project""",
    'description': """
        funenc auto gen project
    """,

    'author': "funenc",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '1.0',

    'depends': ['base',
                'metro_park_base',
                'metro_park_maintenance',
                'funenc_wechat',
                'metro_park_dispatch'],

    'data': [
        'security/ir.model.access.csv',
        'data/line.xml',
        'data/location.xml',
        'data/signals_yuanhua.xml',
        'data/rail_secs_yuanhua.xml',
        'data/switches_yuanhua.xml',
        'data/init_rail_and_switch_relation.xml',
        'data/batch_no.xml',
        'data/train_dev.xml',
        'data/repair_rule.xml',
        'data/plan_config_data.xml'
    ],

    'qweb': [],
    'application': True
}
