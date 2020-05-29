# -*- coding: utf-8 -*-
{
    'name': "metro_park_base_data_10",
    'summary': """10号线基础数据""",
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
                'maintenance_management',
                'funenc_wechat',
                'metro_park_dispatch'],

    'data': [
        'security/ir.model.access.csv',
        'data/line.xml',
        'data/location.xml',
        'data/repair_rule.xml',
        'data/max_repair_info.xml',
        'data/main_line_sec.xml',
        'data/batch_no.xml',
        'data/train_dev.xml',
        'data/signals_banqiao.xml',
        'data/signals_gaodalu.xml',
        'data/rail_secs_banqiao.xml',
        'data/rail_secs_gaodalu.xml',
        'data/switches_banqiao.xml',
        'data/switches_gaodalu.xml',
        'data/electric_area_banqiao.xml',
        'data/electric_area_gaodalu.xml',
        'data/init_rail_and_switch_relation.xml',
        'data/ats_address.xml',
        'data/ats_secs.xml',
        'data/btn_table.xml',
        'data/code_table.xml',
        'data/plan_config_data.xml',
        'data/construction_area_relation.xml',
        'data/init_department_property.xml',
        'data/department_extend.xml',
        'data/max_repair_info.xml',
        'data/init_location_max_repair_info.xml',
        # 'data/base_user.xml',
        'data/maintenance_basic_configuration/station.xml',
        'data/maintenance_basic_configuration/place.xml',
        'data/maintenance_basic_configuration/equipment.xml',
        'data/maintenance_basic_configuration/equipment_state.xml'
    ],

    'qweb': [],
    'application': True
}
