# -*- coding: utf-8 -*-
{
    'name': "metro_park_base_data_6",
    'summary': """6号线基础数据""",
    'description': """
        10号线基础数据
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

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/line.xml',
        'data/location.xml',
        'data/repair_rule.xml',
        'data/rail_type.xml',
        'data/plan_config_data.xml',
        'data/rail_secs_huilong.xml',
        'data/rail_secs_pitong.xml',
        'data/signals_huilong.xml',
        'data/signals_pitong.xml',
        'data/switches_huilong.xml',
        'data/switches_pitong.xml',
        'data/batch_no.xml',
        'data/btn_table.xml',
        'data/code_table.xml',
        'data/train_dev.xml',
        'data/department_extend.xml',
        'data/rail_secs_longdengshan.xml',
        'data/signals_longdengshan.xml',
        'data/switches_longdengshan.xml',
        'data/base_user.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
