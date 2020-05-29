# -*- coding: utf-8 -*-

# 各场段收/发车时出入段线、照查以及相应股道的对应关系数据
# 场段: 98-板桥 99-高大路

# 收车
park_train_back_conditions_map = {
    '10': {
        'park_list': [
            {  # 板桥 '98'
                'name': '板桥',
                'rtu_name': 'ban_qiao',
                'rtu_id': 98,
                'rules': {
                    'ZCJ1': {
                        'hold_sec': 'T1705G',
                        'start_rail': 'T1701G'
                    },
                    'ZCJ3': {
                        'hold_sec': 'T1710G',
                        'start_rail': 'T1714G'
                    }
                },
                'special_station_rails': [{
                    'rtu_id': 17,  # 双流西站
                    'rails': ['T1701', 'T1705', 'T1710', 'T1714']
                }],
                'add_end_tag': True,
                'interlock_client': [{
                    'host': '192.168.100.100',
                    'port': 54321,
                    'tag': 'a'
                }]
            },
            # {  # 高大路 '99'
            #     'name': '高大路',
            #     'rtu_name': 'gao_da_lu',
            #     'rtu_id': 99,
            #     'rules': {
            #             'ZCJ1': {
            #                 'hold_sec': 'T2604G',
            #                 'start_rail': 'T2602G'
            #             },
            #         'ZCJ3': {
            #                 'hold_sec': 'T2615G',
            #                 'start_rail': 'T2617G'
            #             }
            #     },
            #     'special_station_rails': [{
            #         'rtu_id': 26,  # 新平站
            #         'rails': ['T2617', 'T2615', 'T2602', 'T2604']
            #     }],
            #     'add_end_tag': True,
            #     'interlock_client': [{
            #         'host': '192.168.100.100',
            #         'port': 54321,
            #         'tag': 'a'
            #     }]
            # }
        ],
        'ats_client': {
            'host': '192.168.100.100',
            'port': 54324
        }
    },
    '6': {
        'park_list': [
            {  # 回龙 '99'
                'name': '回龙',
                'rtu_name': 'hui_long',
                'rtu_id': 99,
                'rules': {
                    'ZCJ1': {
                        'hold_sec': 'T6604G',
                        'start_rail': 'T6602G'
                    },
                    'ZCJ3': {
                        'hold_sec': 'T6615G',
                        'start_rail': 'T6617G'
                    }
                },
                'special_station_rails': [{
                    'rtu_id': 66,  # 兰家沟站
                    'rails': ['T6602', 'T6604', 'T6615', 'T6617']
                }],
                'add_end_tag': True,
                'interlock_client': [{
                    'host': '192.168.100.100',
                    'port': 54321,
                    'tag': 'a'
                }]
            },
            # {  # 龙灯山 '98'
            #     'name': '龙灯山',
            #     'rtu_name': 'long_deng_shan',
            #     'rtu_id': 98,
            #     'rules': {
            #         'T4615ZCMARK': {
            #             'hold_sec': 'T4615',
            #             'start_rail': 'T4617'
            #         },
            #         'T4623ZCMARK': {
            #             'hold_sec': 'T4623',
            #             'start_rail': 'T4621'
            #         }
            #     },
            #     'special_station_rails': [{
            #         'rtu_id': 46,  # 张家寺站
            #         'rails': ['T4621', 'T4623', 'T4615', 'T4617']
            #     }],
            #     'add_end_tag': False,
            #     'interlock_client': [{
            #         'host': '192.168.100.100',
            #         'port': 54321,
            #         'tag': 'a'
            #     }]
            # },
            # {  # 郫筒 '97'
            #     'name': '郫筒',
            #     'rtu_name': 'pi_tong',
            #     'rtu_id': 97,
            #     'rules': {
            #         'ZC2': {
            #             'hold_sec': 'T1124G',
            #             'start_rail': 'T1126G'
            #         },
            #         'ZC4': {
            #             'hold_sec': 'T1103G',
            #             'start_rail': 'T1101G'
            #         }
            #     },
            #     'special_station_rails': [{
            #         'rtu_id': 11,  # 望丛祠站
            #         'rails': ['T1101', 'T1103', 'T1124', 'T1126']
            #     }],
            #     'add_end_tag': True,
            #     'interlock_client': [{
            #         'host': '192.168.100.100',
            #         'port': 54321,
            #         'tag': 'a'
            #     }]
            # }
        ],
        'ats_client': {
            'host': '192.168.100.100',
            'port': 54324
        }
    },
    '8': {
        'park_list': [
            {  # 元华 '86'
                'name': '元华',
                'rtu_name': 'yuan_hua',
                'rtu_id': 86,
                'rules': {
                    'T2613ZC': {
                        'hold_sec': 'T2613',
                        'start_rail': 'T2609'
                    },
                    'T2806ZC': {
                        'hold_sec': 'T2806',
                        'start_rail': 'T2802'
                    },
                    'T2825ZC': {
                        'hold_sec': 'T2825',
                        'start_rail': 'T2829'
                    }
                },
                'special_station_rails': [{
                    'rtu_id': 26,  # 顺风站
                    'rails': ['T2609', 'T2611', 'T2613']
                }, {
                    'rtu_id': 28,  # 石羊站
                    'rails': ['T2802', 'T2804', 'T2806', 'T2825', 'T2827', 'T2829']
                }],
                'add_end_tag': False,
                'interlock_client': [{
                    'host': '192.168.100.100',
                    'port': 54321,
                    'tag': 'a'
                }]
            }
        ],
        'ats_client': {
            'host': '192.168.100.100',
            'port': 54324
        }
    }
}
