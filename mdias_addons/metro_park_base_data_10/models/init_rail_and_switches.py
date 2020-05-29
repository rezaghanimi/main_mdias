
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitRailAndSwitches(models.TransientModel):
    '''
    初始化轨道和道岔信息
    '''
    _name = 'metro_park_base_data_10.init_rail_and_switches'

    name = fields.Char(string='name')

    @api.model
    def init_switches(self):
        '''
        建立板桥道岔位置关系, 一定要先把道岔和轨道建立了才行
        :return:
        '''

        ban_qiao_switch_1 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_1')
        ban_qiao_switch_3 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_3')
        ban_qiao_switch_5 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_5')
        ban_qiao_switch_7 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_7')
        ban_qiao_switch_9 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_9')
        ban_qiao_switch_11 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_11')
        ban_qiao_switch_13 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_13')
        ban_qiao_switch_15 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_15')
        ban_qiao_switch_17 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_17')
        ban_qiao_switch_19 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_19')
        ban_qiao_switch_21 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_21')
        ban_qiao_switch_23 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_23')
        ban_qiao_switch_25 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_25')
        ban_qiao_switch_27 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_27')
        ban_qiao_switch_29 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_29')
        ban_qiao_switch_31 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_31')
        ban_qiao_switch_33 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_33')
        ban_qiao_switch_35 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_35')
        ban_qiao_switch_37 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_37')
        ban_qiao_switch_39 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_39')
        ban_qiao_switch_41 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_41')
        ban_qiao_switch_43 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_43')
        ban_qiao_switch_45 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_45')
        ban_qiao_switch_47 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_47')
        ban_qiao_switch_49 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_49')
        ban_qiao_switch_51 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_51')
        ban_qiao_switch_53 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_53')
        ban_qiao_switch_55 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_55')
        ban_qiao_switch_57 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_57')
        ban_qiao_switch_59 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_59')
        ban_qiao_switch_63 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_63')
        ban_qiao_switch_65 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_65')
        ban_qiao_switch_67 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_67')
        ban_qiao_switch_69 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_69')
        ban_qiao_switch_71 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_71')
        ban_qiao_switch_73 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_73')
        ban_qiao_switch_75 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_75')
        ban_qiao_switch_77 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_77')
        ban_qiao_switch_79 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_79')
        ban_qiao_switch_81 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_81')
        ban_qiao_switch_83 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_83')
        ban_qiao_switch_61 = self.env.ref(
            'metro_park_base_data_10.ban_qiao_switch_61')

        # 所有的区段
        ban_qiao_10G = self.env.ref('metro_park_base_data_10.ban_qiao_10G')
        ban_qiao_11G = self.env.ref('metro_park_base_data_10.ban_qiao_11G')
        ban_qiao_12G = self.env.ref('metro_park_base_data_10.ban_qiao_12G')
        ban_qiao_13G = self.env.ref('metro_park_base_data_10.ban_qiao_13G')
        ban_qiao_14G = self.env.ref('metro_park_base_data_10.ban_qiao_14G')
        ban_qiao_15G = self.env.ref('metro_park_base_data_10.ban_qiao_15G')
        ban_qiao_16G = self.env.ref('metro_park_base_data_10.ban_qiao_16G')
        ban_qiao_17G = self.env.ref('metro_park_base_data_10.ban_qiao_17G')
        ban_qiao_18G = self.env.ref('metro_park_base_data_10.ban_qiao_18G')
        ban_qiao_19G = self.env.ref('metro_park_base_data_10.ban_qiao_19G')
        ban_qiao_20G = self.env.ref('metro_park_base_data_10.ban_qiao_20G')

        ban_qiao_21AG = self.env.ref('metro_park_base_data_10.ban_qiao_21AG')
        ban_qiao_21BG = self.env.ref('metro_park_base_data_10.ban_qiao_21BG')
        ban_qiao_22AG = self.env.ref('metro_park_base_data_10.ban_qiao_22AG')
        ban_qiao_22BG = self.env.ref('metro_park_base_data_10.ban_qiao_22BG')
        ban_qiao_23AG = self.env.ref('metro_park_base_data_10.ban_qiao_23AG')
        ban_qiao_23BG = self.env.ref('metro_park_base_data_10.ban_qiao_23BG')
        ban_qiao_24AG = self.env.ref('metro_park_base_data_10.ban_qiao_24AG')
        ban_qiao_24BG = self.env.ref('metro_park_base_data_10.ban_qiao_24BG')
        ban_qiao_25AG = self.env.ref('metro_park_base_data_10.ban_qiao_25AG')
        ban_qiao_25BG = self.env.ref('metro_park_base_data_10.ban_qiao_25BG')
        ban_qiao_26AG = self.env.ref('metro_park_base_data_10.ban_qiao_26AG')
        ban_qiao_26BG = self.env.ref('metro_park_base_data_10.ban_qiao_26BG')
        ban_qiao_27AG = self.env.ref('metro_park_base_data_10.ban_qiao_27AG')
        ban_qiao_27BG = self.env.ref('metro_park_base_data_10.ban_qiao_27BG')
        ban_qiao_28AG = self.env.ref('metro_park_base_data_10.ban_qiao_28AG')
        ban_qiao_28BG = self.env.ref('metro_park_base_data_10.ban_qiao_28BG')
        ban_qiao_29AG = self.env.ref('metro_park_base_data_10.ban_qiao_29AG')
        ban_qiao_29BG = self.env.ref('metro_park_base_data_10.ban_qiao_29BG')
        ban_qiao_30AG = self.env.ref('metro_park_base_data_10.ban_qiao_30AG')
        ban_qiao_30BG = self.env.ref('metro_park_base_data_10.ban_qiao_30BG')
        ban_qiao_31AG = self.env.ref('metro_park_base_data_10.ban_qiao_31AG')
        ban_qiao_31BG = self.env.ref('metro_park_base_data_10.ban_qiao_31BG')
        ban_qiao_32AG = self.env.ref('metro_park_base_data_10.ban_qiao_32AG')
        ban_qiao_32BG = self.env.ref('metro_park_base_data_10.ban_qiao_32BG')

        ban_qiao_33G = self.env.ref('metro_park_base_data_10.ban_qiao_33G')
        ban_qiao_34G = self.env.ref('metro_park_base_data_10.ban_qiao_34G')
        ban_qiao_35G = self.env.ref('metro_park_base_data_10.ban_qiao_35G')
        ban_qiao_36G = self.env.ref('metro_park_base_data_10.ban_qiao_36G')
        ban_qiao_37G = self.env.ref('metro_park_base_data_10.ban_qiao_37G')
        ban_qiao_38G = self.env.ref('metro_park_base_data_10.ban_qiao_38G')
        ban_qiao_39G = self.env.ref('metro_park_base_data_10.ban_qiao_39G')

        ban_qiao_D1G = self.env.ref('metro_park_base_data_10.ban_qiao_D1G')
        ban_qiao_D5G = self.env.ref('metro_park_base_data_10.ban_qiao_D5G')
        ban_qiao_D7G = self.env.ref('metro_park_base_data_10.ban_qiao_D7G')
        ban_qiao_D37G = self.env.ref('metro_park_base_data_10.ban_qiao_D37G')
        ban_qiao_D65G = self.env.ref('metro_park_base_data_10.ban_qiao_D65G')
        ban_qiao_D67G = self.env.ref('metro_park_base_data_10.ban_qiao_D67G')

        ban_qiao_5_27WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_5/27WG')
        ban_qiao_9_23WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_9/23WG')
        ban_qiao_23_61WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_23/61WG')
        ban_qiao_21_51WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_21/51WG')
        ban_qiao_25_41WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_25/41WG')
        ban_qiao_27_29WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_27/29WG')
        ban_qiao_65_83WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_65/83WG')
        ban_qiao_1_63WG = self.env.ref(
            'metro_park_base_data_10.ban_qiao_1/63WG')

        ban_qiao_T1714G = self.env.ref(
            'metro_park_base_data_10.ban_qiao_T1714G')
        ban_qiao_T1701G = self.env.ref(
            'metro_park_base_data_10.ban_qiao_T1701G')
        ban_qiao_T1710G = self.env.ref(
            'metro_park_base_data_10.ban_qiao_T1710G')
        ban_qiao_T1705G = self.env.ref(
            'metro_park_base_data_10.ban_qiao_T1705G')

        # 从标以仿真程序在1920 * 1280上面的位置为准
        # ban_qiao_switch_1
        ban_qiao_switch_1.positive_rail = ban_qiao_1_63WG.id
        ban_qiao_switch_1.negative_rail = ban_qiao_D1G.id
        ban_qiao_switch_1.header_rail = False
        ban_qiao_switch_1.positive_switch = False
        ban_qiao_switch_1.negative_switch = False
        ban_qiao_switch_1.header_switch = ban_qiao_switch_3.id
        ban_qiao_switch_1.x_pos = 360
        ban_qiao_switch_1.y_pos = 582

        # ban_qiao_switch_3
        ban_qiao_switch_3.positive_rail = ban_qiao_D5G.id
        ban_qiao_switch_3.negative_rail = False
        ban_qiao_switch_3.header_rail = False
        ban_qiao_switch_3.positive_switch = False
        ban_qiao_switch_3.negative_switch = ban_qiao_switch_1.id
        ban_qiao_switch_3.header_switch = ban_qiao_switch_5.id
        ban_qiao_switch_3.x_pos = 379
        ban_qiao_switch_3.y_pos = 469

        # ban_qiao_switch_5
        ban_qiao_switch_5.positive_rail = ban_qiao_5_27WG.id
        ban_qiao_switch_5.negative_rail = False
        ban_qiao_switch_5.header_rail = False
        ban_qiao_switch_5.positive_switch = False
        ban_qiao_switch_5.negative_switch = ban_qiao_switch_7.id
        ban_qiao_switch_5.header_switch = ban_qiao_switch_3.id
        ban_qiao_switch_5.x_pos = 482
        ban_qiao_switch_5.y_pos = 469

        # ban_qiao_switch_7
        ban_qiao_switch_7.positive_rail = ban_qiao_T1714G.id
        ban_qiao_switch_7.negative_rail = False
        ban_qiao_switch_7.header_rail = False
        ban_qiao_switch_7.positive_switch = False
        ban_qiao_switch_7.negative_switch = ban_qiao_switch_5.id
        ban_qiao_switch_7.header_switch = ban_qiao_switch_13.id
        ban_qiao_switch_7.x_pos = 506
        ban_qiao_switch_7.y_pos = 428

        # ban_qiao_switch_13
        ban_qiao_switch_13.positive_rail = False
        ban_qiao_switch_13.negative_rail = False
        ban_qiao_switch_13.header_rail = False
        ban_qiao_switch_13.positive_switch = ban_qiao_switch_19.id
        ban_qiao_switch_13.negative_switch = ban_qiao_switch_15.id
        ban_qiao_switch_13.header_switch = ban_qiao_switch_7.id
        ban_qiao_switch_13.x_pos = 578
        ban_qiao_switch_13.y_pos = 428

        # ban_qiao_switch_19
        ban_qiao_switch_19.positive_rail = False
        ban_qiao_switch_19.negative_rail = False
        ban_qiao_switch_19.header_rail = False
        ban_qiao_switch_19.positive_switch = ban_qiao_switch_13.id
        ban_qiao_switch_19.negative_switch = ban_qiao_switch_17.id
        ban_qiao_switch_19.header_switch = ban_qiao_switch_25.id
        ban_qiao_switch_19.x_pos = 636
        ban_qiao_switch_19.y_pos = 428

        # ban_qiao_switch_17
        ban_qiao_switch_17.positive_rail = False
        ban_qiao_switch_17.negative_rail = False
        ban_qiao_switch_17.header_rail = False
        ban_qiao_switch_17.positive_switch = ban_qiao_switch_15.id
        ban_qiao_switch_17.negative_switch = ban_qiao_switch_19.id
        ban_qiao_switch_17.header_switch = ban_qiao_switch_11.id
        ban_qiao_switch_17.x_pos = 578  # 和13对齐
        ban_qiao_switch_17.y_pos = 334

        # ban_qiao_switch_15
        ban_qiao_switch_15.positive_rail = False
        ban_qiao_switch_15.negative_rail = False
        ban_qiao_switch_15.header_rail = False
        ban_qiao_switch_15.positive_switch = ban_qiao_switch_17.id
        ban_qiao_switch_15.negative_switch = ban_qiao_switch_13.id
        ban_qiao_switch_15.header_switch = ban_qiao_switch_21.id
        ban_qiao_switch_15.x_pos = 636  # 和19对齐
        ban_qiao_switch_15.y_pos = 334  # 和17对齐

        # ban_qiao_switch_21 right
        ban_qiao_switch_21.positive_rail = ban_qiao_21_51WG.id
        ban_qiao_switch_21.negative_rail = False
        ban_qiao_switch_21.header_rail = False
        ban_qiao_switch_21.positive_switch = False
        ban_qiao_switch_21.negative_switch = ban_qiao_switch_23.id
        ban_qiao_switch_21.header_switch = ban_qiao_switch_15.id
        ban_qiao_switch_21.x_pos = 790
        ban_qiao_switch_21.y_pos = 334

        # ban_qiao_switch_23
        ban_qiao_switch_23.positive_rail = ban_qiao_9_23WG.id
        ban_qiao_switch_23.negative_rail = False
        ban_qiao_switch_23.header_rail = ban_qiao_23_61WG.id
        ban_qiao_switch_23.positive_switch = False
        ban_qiao_switch_23.negative_switch = ban_qiao_switch_21.id
        ban_qiao_switch_23.header_switch = False
        ban_qiao_switch_23.x_pos = 844
        ban_qiao_switch_23.y_pos = 212

        # ban_qiao_switch_9
        ban_qiao_switch_9.positive_rail = ban_qiao_9_23WG.id
        ban_qiao_switch_9.negative_rail = False
        ban_qiao_switch_9.header_rail = ban_qiao_D7G.id
        ban_qiao_switch_9.positive_switch = False
        ban_qiao_switch_9.negative_switch = ban_qiao_switch_11.id
        ban_qiao_switch_9.header_switch = False
        ban_qiao_switch_9.x_pos = 451
        ban_qiao_switch_9.y_pos = 212

        # ban_qiao_switch_11
        ban_qiao_switch_11.positive_rail = ban_qiao_T1701G.id
        ban_qiao_switch_11.negative_rail = False
        ban_qiao_switch_11.header_rail = False
        ban_qiao_switch_11.positive_switch = False
        ban_qiao_switch_11.negative_switch = ban_qiao_switch_9.id
        ban_qiao_switch_11.header_switch = ban_qiao_switch_17.id
        ban_qiao_switch_11.x_pos = 491
        ban_qiao_switch_11.y_pos = 334

        # ban_qiao_switch_25
        ban_qiao_switch_25.positive_rail = ban_qiao_25_41WG.id
        ban_qiao_switch_25.negative_rail = False
        ban_qiao_switch_25.header_rail = False
        ban_qiao_switch_25.positive_switch = False
        ban_qiao_switch_25.negative_switch = ban_qiao_switch_27.id
        ban_qiao_switch_25.header_switch = ban_qiao_switch_19.id
        ban_qiao_switch_25.x_pos = 755
        ban_qiao_switch_25.y_pos = 428

        # ban_qiao_switch_27
        ban_qiao_switch_27.positive_rail = ban_qiao_5_27WG.id
        ban_qiao_switch_27.negative_rail = False
        ban_qiao_switch_27.header_rail = ban_qiao_27_29WG.id
        ban_qiao_switch_27.positive_switch = False
        ban_qiao_switch_27.negative_switch = ban_qiao_switch_25.id
        ban_qiao_switch_27.header_switch = False
        ban_qiao_switch_27.x_pos = 755
        ban_qiao_switch_27.y_pos = 428

        # ban_qiao_switch_29
        ban_qiao_switch_29.positive_rail = False
        ban_qiao_switch_29.negative_rail = False
        ban_qiao_switch_29.header_rail = ban_qiao_27_29WG.id
        ban_qiao_switch_29.positive_switch = ban_qiao_switch_37.id
        ban_qiao_switch_29.negative_switch = ban_qiao_switch_31.id
        ban_qiao_switch_29.header_switch = False
        ban_qiao_switch_29.x_pos = 1009
        ban_qiao_switch_29.y_pos = 814

        # ban_qiao_switch_31
        ban_qiao_switch_31.positive_rail = False
        ban_qiao_switch_31.negative_rail = ban_qiao_39G.id
        ban_qiao_switch_31.header_rail = False
        ban_qiao_switch_31.positive_switch = ban_qiao_switch_33.id
        ban_qiao_switch_31.negative_switch = False
        ban_qiao_switch_31.header_switch = ban_qiao_switch_29.id
        ban_qiao_switch_31.x_pos = 1087
        ban_qiao_switch_31.y_pos = 938

        # ban_qiao_switch_33
        ban_qiao_switch_33.positive_rail = ban_qiao_38G.id
        ban_qiao_switch_33.negative_rail = False
        ban_qiao_switch_33.header_rail = False
        ban_qiao_switch_33.positive_switch = False
        ban_qiao_switch_33.negative_switch = ban_qiao_switch_35.id
        ban_qiao_switch_33.header_switch = ban_qiao_switch_31.id
        ban_qiao_switch_33.x_pos = 1129
        ban_qiao_switch_33.y_pos = 938

        # ban_qiao_switch_35
        ban_qiao_switch_35.positive_rail = ban_qiao_37G.id
        ban_qiao_switch_35.negative_rail = ban_qiao_36G.id
        ban_qiao_switch_35.header_rail = False
        ban_qiao_switch_35.positive_switch = False
        ban_qiao_switch_35.negative_switch = False
        ban_qiao_switch_35.header_switch = ban_qiao_switch_33.id
        ban_qiao_switch_35.x_pos = 1180
        ban_qiao_switch_35.y_pos = 891

        # ban_qiao_switch_37
        ban_qiao_switch_37.positive_rail = ban_qiao_35G.id
        ban_qiao_switch_37.negative_rail = False
        ban_qiao_switch_37.header_rail = False
        ban_qiao_switch_37.positive_switch = False
        ban_qiao_switch_37.negative_switch = ban_qiao_switch_39.id
        ban_qiao_switch_37.header_switch = ban_qiao_switch_29.id
        ban_qiao_switch_37.x_pos = 1121
        ban_qiao_switch_37.y_pos = 814

        # ban_qiao_switch_39
        ban_qiao_switch_39.positive_rail = ban_qiao_34G.id
        ban_qiao_switch_39.negative_rail = ban_qiao_33G.id
        ban_qiao_switch_39.header_rail = False
        ban_qiao_switch_39.positive_switch = False
        ban_qiao_switch_39.negative_switch = False
        ban_qiao_switch_39.header_switch = ban_qiao_switch_37.id
        ban_qiao_switch_39.x_pos = 1172
        ban_qiao_switch_39.y_pos = 774

        # ban_qiao_switch_41
        ban_qiao_switch_41.positive_rail = False
        ban_qiao_switch_41.negative_rail = False
        ban_qiao_switch_41.header_rail = ban_qiao_25_41WG.id
        ban_qiao_switch_41.positive_switch = ban_qiao_switch_45.id
        ban_qiao_switch_41.negative_switch = ban_qiao_switch_43.id
        ban_qiao_switch_41.header_switch = False
        ban_qiao_switch_41.x_pos = 1000
        ban_qiao_switch_41.y_pos = 575

        # ban_qiao_switch_43
        ban_qiao_switch_43.positive_rail = ban_qiao_31AG.id
        ban_qiao_switch_43.negative_rail = ban_qiao_32AG.id
        ban_qiao_switch_43.header_rail = False
        ban_qiao_switch_43.positive_switch = False
        ban_qiao_switch_43.negative_switch = False
        ban_qiao_switch_43.header_switch = ban_qiao_switch_41.id
        ban_qiao_switch_43.x_pos = 1136
        ban_qiao_switch_43.y_pos = 456

        # ban_qiao_switch_45
        ban_qiao_switch_45.positive_rail = False
        ban_qiao_switch_45.negative_rail = ban_qiao_30AG.id
        ban_qiao_switch_45.header_rail = False
        ban_qiao_switch_45.positive_switch = ban_qiao_switch_47.id
        ban_qiao_switch_45.negative_switch = False
        ban_qiao_switch_45.header_switch = ban_qiao_switch_41.id
        ban_qiao_switch_45.x_pos = 1064
        ban_qiao_switch_45.y_pos = 575

        # ban_qiao_switch_47
        ban_qiao_switch_47.positive_rail = ban_qiao_29AG.id
        ban_qiao_switch_47.negative_rail = False
        ban_qiao_switch_47.header_rail = False
        ban_qiao_switch_47.positive_switch = False
        ban_qiao_switch_47.negative_switch = ban_qiao_switch_49.id
        ban_qiao_switch_47.header_switch = ban_qiao_switch_45.id
        ban_qiao_switch_47.x_pos = 1103
        ban_qiao_switch_47.y_pos = 575

        # ban_qiao_switch_49
        ban_qiao_switch_49.positive_rail = ban_qiao_28AG.id
        ban_qiao_switch_49.negative_rail = ban_qiao_27AG.id
        ban_qiao_switch_49.header_rail = False
        ban_qiao_switch_49.positive_switch = False
        ban_qiao_switch_49.negative_switch = False
        ban_qiao_switch_49.header_switch = ban_qiao_switch_47.id
        ban_qiao_switch_49.x_pos = 1152
        ban_qiao_switch_49.y_pos = 531

        # ban_qiao_switch_51
        ban_qiao_switch_51.positive_rail = False
        ban_qiao_switch_51.negative_rail = False
        ban_qiao_switch_51.header_rail = ban_qiao_21_51WG.id
        ban_qiao_switch_51.positive_switch = ban_qiao_switch_55.id
        ban_qiao_switch_51.negative_switch = ban_qiao_switch_53.id
        ban_qiao_switch_51.header_switch = False
        ban_qiao_switch_51.x_pos = 1000
        ban_qiao_switch_51.y_pos = 334

        # ban_qiao_switch_53
        ban_qiao_switch_53.positive_rail = ban_qiao_25AG.id
        ban_qiao_switch_53.negative_rail = ban_qiao_26AG.id
        ban_qiao_switch_53.header_rail = False
        ban_qiao_switch_53.positive_switch = False
        ban_qiao_switch_53.negative_switch = False
        ban_qiao_switch_53.header_switch = ban_qiao_switch_51.id
        ban_qiao_switch_53.x_pos = 1126
        ban_qiao_switch_53.y_pos = 416

        # ban_qiao_switch_55
        ban_qiao_switch_55.positive_rail = False
        ban_qiao_switch_55.negative_rail = ban_qiao_24AG.id
        ban_qiao_switch_55.header_rail = False
        ban_qiao_switch_55.positive_switch = ban_qiao_switch_57.id
        ban_qiao_switch_55.negative_switch = False
        ban_qiao_switch_55.header_switch = ban_qiao_switch_51.id
        ban_qiao_switch_55.x_pos = 1078
        ban_qiao_switch_55.y_pos = 334

        # ban_qiao_switch_57
        ban_qiao_switch_57.positive_rail = ban_qiao_23AG.id
        ban_qiao_switch_57.negative_rail = False
        ban_qiao_switch_57.header_rail = False
        ban_qiao_switch_57.positive_switch = False
        ban_qiao_switch_57.negative_switch = ban_qiao_switch_59.id
        ban_qiao_switch_57.header_switch = ban_qiao_switch_55.id
        ban_qiao_switch_57.x_pos = 1121
        ban_qiao_switch_57.y_pos = 334

        # ban_qiao_switch_59
        ban_qiao_switch_59.positive_rail = ban_qiao_22AG.id
        ban_qiao_switch_59.negative_rail = ban_qiao_21AG.id
        ban_qiao_switch_59.header_rail = False
        ban_qiao_switch_59.positive_switch = False
        ban_qiao_switch_59.negative_switch = False
        ban_qiao_switch_59.header_switch = ban_qiao_switch_57.id
        ban_qiao_switch_59.x_pos = 1164
        ban_qiao_switch_59.y_pos = 292

        # ban_qiao_switch_61
        ban_qiao_switch_61.positive_rail = ban_qiao_20G.id
        ban_qiao_switch_61.negative_rail = ban_qiao_19G.id
        ban_qiao_switch_61.header_rail = ban_qiao_23_61WG.id
        ban_qiao_switch_61.positive_switch = False
        ban_qiao_switch_61.negative_switch = False
        ban_qiao_switch_61.header_switch = False
        ban_qiao_switch_61.x_pos = 1138
        ban_qiao_switch_61.y_pos = 213

        # ban_qiao_switch_63
        ban_qiao_switch_63.positive_rail = False
        ban_qiao_switch_63.negative_rail = ban_qiao_1_63WG.id
        ban_qiao_switch_63.header_rail = ban_qiao_D37G.id
        ban_qiao_switch_63.positive_switch = ban_qiao_switch_65.id
        ban_qiao_switch_63.negative_switch = False
        ban_qiao_switch_63.header_switch = False
        ban_qiao_switch_63.x_pos = 189
        ban_qiao_switch_63.y_pos = 854

        # ban_qiao_switch_65
        ban_qiao_switch_65.positive_rail = False
        ban_qiao_switch_65.negative_rail = ban_qiao_65_83WG.id
        ban_qiao_switch_65.header_rail = False
        ban_qiao_switch_65.positive_switch = ban_qiao_switch_67.id
        ban_qiao_switch_65.negative_switch = False
        ban_qiao_switch_65.header_switch = ban_qiao_switch_63.id
        ban_qiao_switch_65.x_pos = 242
        ban_qiao_switch_65.y_pos = 854

        # ban_qiao_switch_67
        ban_qiao_switch_67.positive_rail = False
        ban_qiao_switch_67.negative_rail = False
        ban_qiao_switch_67.header_rail = False
        ban_qiao_switch_67.positive_switch = ban_qiao_switch_79.id
        ban_qiao_switch_67.negative_switch = ban_qiao_switch_69.id
        ban_qiao_switch_67.header_switch = ban_qiao_switch_65.id
        ban_qiao_switch_67.x_pos = 361
        ban_qiao_switch_67.y_pos = 854

        # ban_qiao_switch_69
        ban_qiao_switch_69.positive_rail = False
        ban_qiao_switch_69.negative_rail = False
        ban_qiao_switch_69.header_rail = False
        ban_qiao_switch_69.positive_switch = ban_qiao_switch_75.id
        ban_qiao_switch_69.negative_switch = ban_qiao_switch_71.id
        ban_qiao_switch_69.header_switch = ban_qiao_switch_67.id
        ban_qiao_switch_69.x_pos = 386
        ban_qiao_switch_69.y_pos = 737

        # ban_qiao_switch_71
        ban_qiao_switch_71.positive_rail = ban_qiao_12G.id
        ban_qiao_switch_71.negative_rail = False
        ban_qiao_switch_71.header_rail = False
        ban_qiao_switch_71.positive_switch = False
        ban_qiao_switch_71.negative_switch = ban_qiao_switch_73.id
        ban_qiao_switch_71.header_switch = ban_qiao_switch_69.id
        ban_qiao_switch_71.x_pos = 403
        ban_qiao_switch_71.y_pos = 658

        # ban_qiao_switch_73
        ban_qiao_switch_73.positive_rail = ban_qiao_10G.id
        ban_qiao_switch_73.negative_rail = ban_qiao_11G.id
        ban_qiao_switch_73.header_rail = False
        ban_qiao_switch_73.positive_switch = False
        ban_qiao_switch_73.negative_switch = False
        ban_qiao_switch_73.header_switch = ban_qiao_switch_71.id
        ban_qiao_switch_73.x_pos = 412
        ban_qiao_switch_73.y_pos = 615

        # ban_qiao_switch_75
        ban_qiao_switch_75.positive_rail = False
        ban_qiao_switch_75.negative_rail = ban_qiao_13G.id
        ban_qiao_switch_75.header_rail = False
        ban_qiao_switch_75.positive_switch = ban_qiao_switch_77.id
        ban_qiao_switch_75.negative_switch = False
        ban_qiao_switch_75.header_switch = ban_qiao_switch_69.id
        ban_qiao_switch_75.x_pos = 443
        ban_qiao_switch_75.y_pos = 737

        # ban_qiao_switch_77
        ban_qiao_switch_77.positive_rail = ban_qiao_14G.id
        ban_qiao_switch_77.negative_rail = ban_qiao_15G.id
        ban_qiao_switch_77.header_rail = False
        ban_qiao_switch_77.positive_switch = False
        ban_qiao_switch_77.negative_switch = False
        ban_qiao_switch_77.header_switch = ban_qiao_switch_75.id
        ban_qiao_switch_77.x_pos = 419
        ban_qiao_switch_77.y_pos = 737

        # ban_qiao_switch_79
        ban_qiao_switch_79.positive_rail = False
        ban_qiao_switch_79.negative_rail = ban_qiao_18G.id
        ban_qiao_switch_79.header_rail = False
        ban_qiao_switch_79.positive_switch = ban_qiao_switch_81.id
        ban_qiao_switch_79.negative_switch = False
        ban_qiao_switch_79.header_switch = ban_qiao_switch_67.id
        ban_qiao_switch_79.x_pos = 448
        ban_qiao_switch_79.y_pos = 854

        # ban_qiao_switch_81
        ban_qiao_switch_81.positive_rail = ban_qiao_17G.id
        ban_qiao_switch_81.negative_rail = ban_qiao_16G.id
        ban_qiao_switch_81.header_rail = False
        ban_qiao_switch_81.positive_switch = False
        ban_qiao_switch_81.negative_switch = False
        ban_qiao_switch_81.header_switch = ban_qiao_switch_79.id
        ban_qiao_switch_81.x_pos = 500
        ban_qiao_switch_81.y_pos = 855

        # ban_qiao_switch_83
        ban_qiao_switch_83.positive_rail = ban_qiao_D65G.id
        ban_qiao_switch_83.negative_rail = ban_qiao_65_83WG.id
        ban_qiao_switch_83.header_rail = ban_qiao_D67G.id
        ban_qiao_switch_83.positive_switch = False
        ban_qiao_switch_83.negative_switch = False
        ban_qiao_switch_83.header_switch = False
        ban_qiao_switch_83.x_pos = 455
        ban_qiao_switch_83.y_pos = 971

        # 区段
        # ban_qiao_19G
        ban_qiao_19G.left_rail_id = False
        ban_qiao_19G.right_rail_id = False
        ban_qiao_19G.left_switch_id = ban_qiao_switch_61.id
        ban_qiao_19G.right_switch_id = False
        ban_qiao_19G.left_switch_position = 'negative'
        ban_qiao_19G.right_switch_position = False
        ban_qiao_19G.x_pos = 455
        ban_qiao_19G.y_pos = 971

        # ban_qiao_20G
        ban_qiao_20G.left_rail_id = False
        ban_qiao_20G.right_rail_id = False
        ban_qiao_20G.left_switch_id = ban_qiao_switch_61.id
        ban_qiao_20G.right_switch_id = False
        ban_qiao_20G.left_switch_position = 'positive'
        ban_qiao_20G.right_switch_position = False
        ban_qiao_20G.x_pos = 1369
        ban_qiao_20G.y_pos = 213

        # ban_qiao_21AG
        ban_qiao_21AG.left_rail_id = False
        ban_qiao_21AG.right_rail_id = ban_qiao_21BG.id
        ban_qiao_21AG.left_switch_id = ban_qiao_switch_59.id
        ban_qiao_21AG.right_switch_id = False
        ban_qiao_21AG.left_switch_position = 'negative'
        ban_qiao_21AG.right_switch_position = False
        ban_qiao_21AG.x_pos = 1396
        ban_qiao_21AG.y_pos = 253

        ban_qiao_21BG.left_rail_id = ban_qiao_21AG.id
        ban_qiao_21BG.right_rail_id = False
        ban_qiao_21BG.left_switch_id = False
        ban_qiao_21BG.right_switch_id = False
        ban_qiao_21BG.left_switch_position = False
        ban_qiao_21BG.right_switch_position = False
        ban_qiao_21BG.x_pos = 1713
        ban_qiao_21BG.y_pos = 252

        ban_qiao_22AG.left_rail_id = False
        ban_qiao_22AG.right_rail_id = ban_qiao_22BG.id
        ban_qiao_22AG.left_switch_id = ban_qiao_switch_59.id
        ban_qiao_22AG.right_switch_id = False
        ban_qiao_22AG.left_switch_position = 'positive'
        ban_qiao_22AG.right_switch_position = False
        ban_qiao_22AG.x_pos = 1372
        ban_qiao_22AG.y_pos = 252

        ban_qiao_22BG.left_rail_id = ban_qiao_22AG.id
        ban_qiao_22BG.right_rail_id = False
        ban_qiao_22BG.left_switch_id = False
        ban_qiao_22BG.right_switch_id = False
        ban_qiao_22BG.left_switch_position = False
        ban_qiao_22BG.right_switch_position = False
        ban_qiao_22BG.x_pos = 1685
        ban_qiao_22BG.y_pos = 294

        ban_qiao_23AG.left_rail_id = False
        ban_qiao_23AG.right_rail_id = ban_qiao_23BG.id
        ban_qiao_23AG.left_switch_id = ban_qiao_switch_57.id
        ban_qiao_23AG.right_switch_id = False
        ban_qiao_23AG.left_switch_position = 'positive'
        ban_qiao_23AG.right_switch_position = False
        ban_qiao_23AG.x_pos = 1432
        ban_qiao_23AG.y_pos = 335

        ban_qiao_23BG.left_rail_id = ban_qiao_23AG.id
        ban_qiao_23BG.right_rail_id = False
        ban_qiao_23BG.left_switch_id = False
        ban_qiao_23BG.right_switch_id = False
        ban_qiao_23BG.left_switch_position = False
        ban_qiao_23BG.right_switch_position = False
        ban_qiao_23BG.x_pos = 1726
        ban_qiao_23BG.y_pos = 335

        ban_qiao_24AG.left_rail_id = False
        ban_qiao_24AG.right_rail_id = ban_qiao_24BG.id
        ban_qiao_24AG.left_switch_id = ban_qiao_switch_55.id
        ban_qiao_24AG.right_switch_id = False
        ban_qiao_24AG.left_switch_position = 'negative'
        ban_qiao_24AG.right_switch_position = False
        ban_qiao_24AG.x_pos = 1364
        ban_qiao_24AG.y_pos = 371

        ban_qiao_24BG.left_rail_id = ban_qiao_24AG.id
        ban_qiao_24BG.right_rail_id = False
        ban_qiao_24BG.left_switch_id = False
        ban_qiao_24BG.right_switch_id = False
        ban_qiao_24BG.left_switch_position = False
        ban_qiao_24BG.right_switch_position = False
        ban_qiao_24BG.x_pos = 1679
        ban_qiao_24BG.y_pos = 373

        ban_qiao_25AG.left_rail_id = False
        ban_qiao_25AG.right_rail_id = ban_qiao_25BG.id
        ban_qiao_25AG.left_switch_id = ban_qiao_switch_53.id
        ban_qiao_25AG.right_switch_id = False
        ban_qiao_25AG.left_switch_position = 'positive'
        ban_qiao_25AG.right_switch_position = False
        ban_qiao_25AG.x_pos = 1452
        ban_qiao_25AG.y_pos = 416

        ban_qiao_25BG.left_rail_id = ban_qiao_25AG.id
        ban_qiao_25BG.right_rail_id = False
        ban_qiao_25BG.left_switch_id = False
        ban_qiao_25BG.right_switch_id = False
        ban_qiao_25BG.left_switch_position = False
        ban_qiao_25BG.right_switch_position = False
        ban_qiao_25BG.x_pos = 1736
        ban_qiao_25BG.y_pos = 416

        ban_qiao_26AG.left_rail_id = False
        ban_qiao_26AG.right_rail_id = ban_qiao_26BG.id
        ban_qiao_26AG.left_switch_id = ban_qiao_switch_53.id
        ban_qiao_26AG.right_switch_id = False
        ban_qiao_26AG.left_switch_position = 'negative'
        ban_qiao_26AG.right_switch_position = False
        ban_qiao_26AG.x_pos = 1374
        ban_qiao_26AG.y_pos = 454

        ban_qiao_26BG.left_rail_id = ban_qiao_26AG.id
        ban_qiao_26BG.right_rail_id = False
        ban_qiao_26BG.left_switch_id = False
        ban_qiao_26BG.right_switch_id = False
        ban_qiao_26BG.left_switch_position = False
        ban_qiao_26BG.right_switch_position = False
        ban_qiao_26BG.x_pos = 1693
        ban_qiao_26BG.y_pos = 454

        ban_qiao_D7G.left_rail_id = False
        ban_qiao_D7G.right_rail_id = False
        ban_qiao_D7G.left_switch_id = False
        ban_qiao_D7G.right_switch_id = ban_qiao_switch_9.id
        ban_qiao_D7G.left_switch_position = False
        ban_qiao_D7G.right_switch_position = 'header'
        ban_qiao_D7G.x_pos = 261
        ban_qiao_D7G.y_pos = 212

        ban_qiao_T1714G.left_rail_id = ban_qiao_T1710G.id
        ban_qiao_T1714G.right_rail_id = False
        ban_qiao_T1714G.left_switch_id = False
        ban_qiao_T1714G.right_switch_id = ban_qiao_switch_7.id
        ban_qiao_T1714G.left_switch_position = False
        ban_qiao_T1714G.right_switch_position = 'positive'
        ban_qiao_T1714G.x_pos = 307
        ban_qiao_T1714G.y_pos = 427

        ban_qiao_T1710G.left_rail_id = False
        ban_qiao_T1710G.right_rail_id = ban_qiao_T1714G.id
        ban_qiao_T1710G.left_switch_id = False
        ban_qiao_T1710G.right_switch_id = False
        ban_qiao_T1710G.left_switch_position = False
        ban_qiao_T1710G.right_switch_position = False
        ban_qiao_T1710G.x_pos = 123
        ban_qiao_T1710G.y_pos = 335

        ban_qiao_23_61WG.left_rail_id = False
        ban_qiao_23_61WG.right_rail_id = False
        ban_qiao_23_61WG.left_switch_id = ban_qiao_switch_23.id
        ban_qiao_23_61WG.right_switch_id = ban_qiao_switch_61.id
        ban_qiao_23_61WG.left_switch_position = 'header'
        ban_qiao_23_61WG.right_switch_position = 'header'
        ban_qiao_23_61WG.x_pos = 971
        ban_qiao_23_61WG.y_pos = 212

        ban_qiao_9_23WG.left_rail_id = False
        ban_qiao_9_23WG.right_rail_id = False
        ban_qiao_9_23WG.left_switch_id = ban_qiao_switch_9.id
        ban_qiao_9_23WG.right_switch_id = ban_qiao_switch_23.id
        ban_qiao_9_23WG.left_switch_position = 'positive'
        ban_qiao_9_23WG.right_switch_position = 'positive'
        ban_qiao_9_23WG.x_pos = 642
        ban_qiao_9_23WG.y_pos = 212

        ban_qiao_21_51WG.left_rail_id = False
        ban_qiao_21_51WG.right_rail_id = False
        ban_qiao_21_51WG.left_switch_id = ban_qiao_switch_21.id
        ban_qiao_21_51WG.right_switch_id = ban_qiao_switch_51.id
        ban_qiao_21_51WG.left_switch_position = 'positive'
        ban_qiao_21_51WG.right_switch_position = 'header'
        ban_qiao_21_51WG.x_pos = 642
        ban_qiao_21_51WG.y_pos = 212

        ban_qiao_27AG.left_rail_id = False
        ban_qiao_27AG.right_rail_id = ban_qiao_27BG.id
        ban_qiao_27AG.left_switch_id = ban_qiao_switch_49.id
        ban_qiao_27AG.right_switch_id = False
        ban_qiao_27AG.left_switch_position = 'negative'
        ban_qiao_27AG.right_switch_position = False
        ban_qiao_27AG.x_pos = 1443
        ban_qiao_27AG.y_pos = 496

        ban_qiao_27BG.left_rail_id = ban_qiao_27AG.id
        ban_qiao_27BG.right_rail_id = False
        ban_qiao_27BG.left_switch_id = False
        ban_qiao_27BG.right_switch_id = False
        ban_qiao_27BG.left_switch_position = False
        ban_qiao_27BG.right_switch_position = False
        ban_qiao_27BG.x_pos = 1723
        ban_qiao_27BG.y_pos = 493

        ban_qiao_28AG.left_rail_id = False
        ban_qiao_28AG.right_rail_id = ban_qiao_27BG.id
        ban_qiao_28AG.left_switch_id = ban_qiao_switch_49.id
        ban_qiao_28AG.right_switch_id = False
        ban_qiao_28AG.left_switch_position = 'positive'
        ban_qiao_28AG.right_switch_position = False
        ban_qiao_28AG.x_pos = 1366
        ban_qiao_28AG.y_pos = 533

        ban_qiao_28BG.left_rail_id = ban_qiao_28AG.id
        ban_qiao_28BG.right_rail_id = False
        ban_qiao_28BG.left_switch_id = False
        ban_qiao_28BG.right_switch_id = False
        ban_qiao_28BG.left_switch_position = False
        ban_qiao_28BG.right_switch_position = False
        ban_qiao_28BG.x_pos = 1366
        ban_qiao_28BG.y_pos = 533

        ban_qiao_29AG.left_rail_id = False
        ban_qiao_29AG.right_rail_id = ban_qiao_29BG.id
        ban_qiao_29AG.left_switch_id = ban_qiao_switch_47.id
        ban_qiao_29AG.right_switch_id = False
        ban_qiao_29AG.left_switch_position = 'positive'
        ban_qiao_29AG.right_switch_position = False
        ban_qiao_29AG.x_pos = 1440
        ban_qiao_29AG.y_pos = 577

        ban_qiao_29BG.left_rail_id = ban_qiao_29AG.id
        ban_qiao_29BG.right_rail_id = False
        ban_qiao_29BG.left_switch_id = False
        ban_qiao_29BG.right_switch_id = False
        ban_qiao_29BG.left_switch_position = False
        ban_qiao_29BG.right_switch_position = False
        ban_qiao_29BG.x_pos = 1727
        ban_qiao_29BG.y_pos = 577

        ban_qiao_30AG.left_rail_id = False
        ban_qiao_30AG.right_rail_id = ban_qiao_30BG.id
        ban_qiao_30AG.left_switch_id = ban_qiao_switch_45.id
        ban_qiao_30AG.right_switch_id = False
        ban_qiao_30AG.left_switch_position = 'negative'
        ban_qiao_30AG.right_switch_position = False
        ban_qiao_30AG.x_pos = 1374
        ban_qiao_30AG.y_pos = 619

        ban_qiao_30BG.left_rail_id = ban_qiao_30AG.id
        ban_qiao_30BG.right_rail_id = False
        ban_qiao_30BG.left_switch_id = False
        ban_qiao_30BG.right_switch_id = False
        ban_qiao_30BG.left_switch_position = False
        ban_qiao_30BG.right_switch_position = False
        ban_qiao_30BG.x_pos = 1690
        ban_qiao_30BG.y_pos = 619

        ban_qiao_31AG.left_rail_id = False
        ban_qiao_31AG.right_rail_id = ban_qiao_31BG.id
        ban_qiao_31AG.left_switch_id = ban_qiao_switch_43.id
        ban_qiao_31AG.right_switch_id = False
        ban_qiao_31AG.left_switch_position = 'positive'
        ban_qiao_31AG.right_switch_position = False
        ban_qiao_31AG.x_pos = 1429
        ban_qiao_31AG.y_pos = 655

        ban_qiao_31BG.left_rail_id = ban_qiao_31AG.id
        ban_qiao_31BG.right_rail_id = False
        ban_qiao_31BG.left_switch_id = False
        ban_qiao_31BG.right_switch_id = False
        ban_qiao_31BG.left_switch_position = False
        ban_qiao_31BG.right_switch_position = False
        ban_qiao_31BG.x_pos = 1721
        ban_qiao_31BG.y_pos = 655

        ban_qiao_32AG.left_rail_id = False
        ban_qiao_32AG.right_rail_id = ban_qiao_32BG.id
        ban_qiao_32AG.left_switch_id = ban_qiao_switch_43.id
        ban_qiao_32AG.right_switch_id = False
        ban_qiao_32AG.left_switch_position = 'negative'
        ban_qiao_32AG.right_switch_position = False
        ban_qiao_32AG.x_pos = 1377
        ban_qiao_32AG.y_pos = 694

        ban_qiao_32BG.left_rail_id = False
        ban_qiao_32BG.right_rail_id = ban_qiao_32AG.id
        ban_qiao_32BG.left_switch_id = False
        ban_qiao_32BG.right_switch_id = False
        ban_qiao_32BG.left_switch_position = False
        ban_qiao_32BG.right_switch_position = False
        ban_qiao_32BG.x_pos = 1686
        ban_qiao_32BG.y_pos = 694

        ban_qiao_T1701G.left_rail_id = ban_qiao_T1705G.id
        ban_qiao_T1701G.right_rail_id = False
        ban_qiao_T1701G.left_switch_id = False
        ban_qiao_T1701G.right_switch_id = ban_qiao_switch_11.id
        ban_qiao_T1701G.left_switch_position = False
        ban_qiao_T1701G.right_switch_position = 'positive'
        ban_qiao_T1701G.x_pos = 333
        ban_qiao_T1701G.y_pos = 335

        ban_qiao_T1705G.left_rail_id = False
        ban_qiao_T1705G.right_rail_id = ban_qiao_T1701G.id
        ban_qiao_T1705G.left_switch_id = False
        ban_qiao_T1705G.right_switch_id = False
        ban_qiao_T1705G.left_switch_position = False
        ban_qiao_T1705G.right_switch_position = False
        ban_qiao_T1705G.x_pos = 125
        ban_qiao_T1705G.y_pos = 427

        ban_qiao_25_41WG.left_rail_id = False
        ban_qiao_25_41WG.right_rail_id = False
        ban_qiao_25_41WG.left_switch_id = ban_qiao_switch_25.id
        ban_qiao_25_41WG.right_switch_id = ban_qiao_switch_41.id
        ban_qiao_25_41WG.left_switch_position = 'positive'
        ban_qiao_25_41WG.right_switch_position = 'header'
        ban_qiao_25_41WG.x_pos = 876
        ban_qiao_25_41WG.y_pos = 427

        ban_qiao_33G.left_rail_id = False
        ban_qiao_33G.right_rail_id = False
        ban_qiao_33G.left_switch_id = ban_qiao_switch_39.id
        ban_qiao_33G.right_switch_id = False
        ban_qiao_33G.left_switch_position = 'negative'
        ban_qiao_33G.right_switch_position = False
        ban_qiao_33G.x_pos = 1378
        ban_qiao_33G.y_pos = 735

        ban_qiao_34G.left_rail_id = False
        ban_qiao_34G.right_rail_id = False
        ban_qiao_34G.left_switch_id = ban_qiao_switch_39.id
        ban_qiao_34G.right_switch_id = False
        ban_qiao_34G.left_switch_position = 'positive'
        ban_qiao_34G.right_switch_position = False
        ban_qiao_34G.x_pos = 1378
        ban_qiao_34G.y_pos = 777

        ban_qiao_35G.left_rail_id = False
        ban_qiao_35G.right_rail_id = False
        ban_qiao_35G.left_switch_id = ban_qiao_switch_37.id
        ban_qiao_35G.right_switch_id = False
        ban_qiao_35G.left_switch_position = 'positive'
        ban_qiao_35G.right_switch_position = False
        ban_qiao_35G.x_pos = 1395
        ban_qiao_35G.y_pos = 816

        ban_qiao_36G.left_rail_id = False
        ban_qiao_36G.right_rail_id = False
        ban_qiao_36G.left_switch_id = ban_qiao_switch_35.id
        ban_qiao_36G.right_switch_id = False
        ban_qiao_36G.left_switch_position = 'negative'
        ban_qiao_36G.right_switch_position = False
        ban_qiao_36G.x_pos = 1450
        ban_qiao_36G.y_pos = 845

        ban_qiao_37G.left_rail_id = False
        ban_qiao_37G.right_rail_id = False
        ban_qiao_37G.left_switch_id = ban_qiao_switch_35.id
        ban_qiao_37G.right_switch_id = False
        ban_qiao_37G.left_switch_position = 'positive'
        ban_qiao_37G.right_switch_position = False
        ban_qiao_37G.x_pos = 1372
        ban_qiao_37G.y_pos = 892

        ban_qiao_38G.left_rail_id = False
        ban_qiao_38G.right_rail_id = False
        ban_qiao_38G.left_switch_id = ban_qiao_switch_33.id
        ban_qiao_38G.right_switch_id = False
        ban_qiao_38G.left_switch_position = 'positive'
        ban_qiao_38G.right_switch_position = False
        ban_qiao_38G.x_pos = 1346
        ban_qiao_38G.y_pos = 936

        ban_qiao_39G.left_rail_id = False
        ban_qiao_39G.right_rail_id = False
        ban_qiao_39G.left_switch_id = ban_qiao_switch_31.id
        ban_qiao_39G.right_switch_id = False
        ban_qiao_39G.left_switch_position = 'negative'
        ban_qiao_39G.right_switch_position = False
        ban_qiao_39G.x_pos = 1366
        ban_qiao_39G.y_pos = 977

        ban_qiao_27_29WG.left_rail_id = False
        ban_qiao_27_29WG.right_rail_id = False
        ban_qiao_27_29WG.left_switch_id = ban_qiao_switch_27.id
        ban_qiao_27_29WG.right_switch_id = ban_qiao_switch_29.id
        ban_qiao_27_29WG.left_switch_position = 'header'
        ban_qiao_27_29WG.right_switch_position = 'header'
        ban_qiao_27_29WG.x_pos = 837
        ban_qiao_27_29WG.y_pos = 549

        ban_qiao_D5G.left_rail_id = False
        ban_qiao_D5G.right_rail_id = False
        ban_qiao_D5G.left_switch_id = False
        ban_qiao_D5G.right_switch_id = ban_qiao_switch_3.id
        ban_qiao_D5G.left_switch_position = False
        ban_qiao_D5G.right_switch_position = 'positive'
        ban_qiao_D5G.x_pos = 259
        ban_qiao_D5G.y_pos = 497

        ban_qiao_D1G.left_rail_id = False
        ban_qiao_D1G.right_rail_id = False
        ban_qiao_D1G.left_switch_id = False
        ban_qiao_D1G.right_switch_id = ban_qiao_switch_1.id
        ban_qiao_D1G.left_switch_position = False
        ban_qiao_D1G.right_switch_position = 'negative'
        ban_qiao_D1G.x_pos = 210
        ban_qiao_D1G.y_pos = 582

        ban_qiao_D37G.left_rail_id = False
        ban_qiao_D37G.right_rail_id = False
        ban_qiao_D37G.left_switch_id = False
        ban_qiao_D37G.right_switch_id = ban_qiao_switch_63.id
        ban_qiao_D37G.left_switch_position = False
        ban_qiao_D37G.right_switch_position = 'header'
        ban_qiao_D37G.x_pos = 110
        ban_qiao_D37G.y_pos = 854

        ban_qiao_16G.left_rail_id = False
        ban_qiao_16G.right_rail_id = False
        ban_qiao_16G.left_switch_id = ban_qiao_switch_81.id
        ban_qiao_16G.right_switch_id = False
        ban_qiao_16G.left_switch_position = 'negative'
        ban_qiao_16G.right_switch_position = False
        ban_qiao_16G.x_pos = 652
        ban_qiao_16G.y_pos = 817

        ban_qiao_17G.left_rail_id = False
        ban_qiao_17G.right_rail_id = False
        ban_qiao_17G.left_switch_id = ban_qiao_switch_81.id
        ban_qiao_17G.right_switch_id = False
        ban_qiao_17G.left_switch_position = 'positive'
        ban_qiao_17G.right_switch_position = False
        ban_qiao_17G.x_pos = 110
        ban_qiao_17G.y_pos = 854

        ban_qiao_10G.left_rail_id = False
        ban_qiao_10G.right_rail_id = False
        ban_qiao_10G.left_switch_id = ban_qiao_switch_73.id
        ban_qiao_10G.right_switch_id = False
        ban_qiao_10G.left_switch_position = 'positive'
        ban_qiao_10G.right_switch_position = False
        ban_qiao_10G.x_pos = 654
        ban_qiao_10G.y_pos = 574

        ban_qiao_11G.left_rail_id = False
        ban_qiao_11G.right_rail_id = False
        ban_qiao_11G.left_switch_id = ban_qiao_switch_73.id
        ban_qiao_11G.right_switch_id = False
        ban_qiao_11G.left_switch_position = 'negative'
        ban_qiao_11G.right_switch_position = False
        ban_qiao_11G.x_pos = 661
        ban_qiao_11G.y_pos = 616

        ban_qiao_12G.left_rail_id = False
        ban_qiao_12G.right_rail_id = False
        ban_qiao_12G.left_switch_id = ban_qiao_switch_71.id
        ban_qiao_12G.right_switch_id = False
        ban_qiao_12G.left_switch_position = 'positive'
        ban_qiao_12G.right_switch_position = False
        ban_qiao_12G.x_pos = 652
        ban_qiao_12G.y_pos = 657

        ban_qiao_13G.left_rail_id = False
        ban_qiao_13G.right_rail_id = False
        ban_qiao_13G.left_switch_id = ban_qiao_switch_75.id
        ban_qiao_13G.right_switch_id = False
        ban_qiao_13G.left_switch_position = 'negative'
        ban_qiao_13G.right_switch_position = False
        ban_qiao_13G.x_pos = 651
        ban_qiao_13G.y_pos = 616

        ban_qiao_14G.left_rail_id = False
        ban_qiao_14G.right_rail_id = False
        ban_qiao_14G.left_switch_id = ban_qiao_switch_77.id
        ban_qiao_14G.right_switch_id = False
        ban_qiao_14G.left_switch_position = 'positive'
        ban_qiao_14G.right_switch_position = False
        ban_qiao_14G.x_pos = 650
        ban_qiao_14G.y_pos = 736

        ban_qiao_15G.left_rail_id = False
        ban_qiao_15G.right_rail_id = False
        ban_qiao_15G.left_switch_id = ban_qiao_switch_77.id
        ban_qiao_15G.right_switch_id = False
        ban_qiao_15G.left_switch_position = 'negative'
        ban_qiao_15G.right_switch_position = False
        ban_qiao_15G.x_pos = 661
        ban_qiao_15G.y_pos = 774

        ban_qiao_18G.left_rail_id = False
        ban_qiao_18G.right_rail_id = False
        ban_qiao_18G.left_switch_id = ban_qiao_switch_79.id
        ban_qiao_18G.right_switch_id = False
        ban_qiao_18G.left_switch_position = 'negative'
        ban_qiao_18G.right_switch_position = False
        ban_qiao_18G.x_pos = 644
        ban_qiao_18G.y_pos = 897

        ban_qiao_5_27WG.left_rail_id = False
        ban_qiao_5_27WG.right_rail_id = False
        ban_qiao_5_27WG.left_switch_id = ban_qiao_switch_5.id
        ban_qiao_5_27WG.right_switch_id = ban_qiao_switch_27.id
        ban_qiao_5_27WG.left_switch_position = 'positive'
        ban_qiao_5_27WG.right_switch_position = 'positive'
        ban_qiao_5_27WG.x_pos = 624
        ban_qiao_5_27WG.y_pos = 497

        ban_qiao_1_63WG.left_rail_id = False
        ban_qiao_1_63WG.right_rail_id = False
        ban_qiao_1_63WG.left_switch_id = ban_qiao_switch_63.id
        ban_qiao_1_63WG.right_switch_id = ban_qiao_switch_1.id
        ban_qiao_1_63WG.left_switch_position = 'negative'
        ban_qiao_1_63WG.right_switch_position = 'positive'
        ban_qiao_1_63WG.x_pos = 293
        ban_qiao_1_63WG.y_pos = 636

        ban_qiao_65_83WG.left_rail_id = False
        ban_qiao_65_83WG.right_rail_id = False
        ban_qiao_65_83WG.left_switch_id = ban_qiao_switch_65.id
        ban_qiao_65_83WG.right_switch_id = ban_qiao_switch_83.id
        ban_qiao_65_83WG.left_switch_position = 'negative'
        ban_qiao_65_83WG.right_switch_position = 'negative'
        ban_qiao_65_83WG.x_pos = 371
        ban_qiao_65_83WG.y_pos = 935

        ban_qiao_D67G.left_rail_id = False
        ban_qiao_D67G.right_rail_id = False
        ban_qiao_D67G.left_switch_id = ban_qiao_switch_83.id
        ban_qiao_D67G.right_switch_id = False
        ban_qiao_D67G.left_switch_position = 'header'
        ban_qiao_D67G.right_switch_position = False
        ban_qiao_D67G.x_pos = 371
        ban_qiao_D67G.y_pos = 935

        ban_qiao_D65G.left_rail_id = False
        ban_qiao_D65G.right_rail_id = False
        ban_qiao_D65G.left_switch_id = False
        ban_qiao_D65G.right_switch_id = ban_qiao_switch_83.id
        ban_qiao_D65G.left_switch_position = False
        ban_qiao_D65G.right_switch_position = 'positive'
        ban_qiao_D65G.x_pos = 676
        ban_qiao_D65G.y_pos = 971

        gao_da_lu_switch_2 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_2')
        gao_da_lu_switch_4 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_4')
        gao_da_lu_switch_6 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_6')
        gao_da_lu_switch_8 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_8')
        gao_da_lu_switch_10 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_10')
        gao_da_lu_switch_12 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_12')
        gao_da_lu_switch_14 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_14')
        gao_da_lu_switch_16 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_16')
        gao_da_lu_switch_18 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_18')
        gao_da_lu_switch_20 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_20')
        gao_da_lu_switch_22 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_22')
        gao_da_lu_switch_24 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_24')
        gao_da_lu_switch_26 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_26')
        gao_da_lu_switch_28 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_28')
        gao_da_lu_switch_30 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_30')
        gao_da_lu_switch_32 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_32')
        gao_da_lu_switch_34 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_34')
        gao_da_lu_switch_36 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_36')
        gao_da_lu_switch_38 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_38')
        gao_da_lu_switch_40 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_40')
        gao_da_lu_switch_42 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_42')
        gao_da_lu_switch_44 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_44')
        gao_da_lu_switch_46 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_46')
        gao_da_lu_switch_48 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_48')
        gao_da_lu_switch_50 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_50')
        gao_da_lu_switch_52 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_52')
        gao_da_lu_switch_54 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_54')
        gao_da_lu_switch_56 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_56')
        gao_da_lu_switch_58 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_58')
        gao_da_lu_switch_60 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_60')
        gao_da_lu_switch_62 = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_switch_62')

        # 所有的区段
        gao_da_lu_rail_1G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_1G')
        gao_da_lu_rail_2G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_2G')
        gao_da_lu_rail_3G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_3G')
        gao_da_lu_rail_4G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_4G')

        gao_da_lu_rail_5AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_5AG')
        gao_da_lu_rail_5BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_5BG')
        gao_da_lu_rail_6AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_6AG')
        gao_da_lu_rail_6BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_6BG')
        gao_da_lu_rail_7AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_7AG')
        gao_da_lu_rail_7BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_7BG')
        gao_da_lu_rail_8AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_8AG')
        gao_da_lu_rail_8BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_8BG')
        gao_da_lu_rail_9AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_9AG')
        gao_da_lu_rail_9BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_9BG')
        gao_da_lu_rail_10AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_10AG')
        gao_da_lu_rail_10BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_10BG')
        gao_da_lu_rail_11AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_11AG')
        gao_da_lu_rail_11BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_11BG')
        gao_da_lu_rail_12AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_12AG')
        gao_da_lu_rail_12BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_12BG')
        gao_da_lu_rail_13AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_13AG')
        gao_da_lu_rail_13BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_13BG')
        gao_da_lu_rail_14AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_14AG')
        gao_da_lu_rail_14BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_14BG')
        gao_da_lu_rail_15AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_15AG')
        gao_da_lu_rail_15BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_15BG')
        gao_da_lu_rail_16AG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_16AG')
        gao_da_lu_rail_16BG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_16BG')

        gao_da_lu_rail_23G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_23G')
        gao_da_lu_rail_24G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_24G')
        gao_da_lu_rail_25G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_25G')

        gao_da_lu_rail_D2G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_D2G')
        gao_da_lu_rail_D4G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_D4G')
        gao_da_lu_rail_D22G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_D22G')

        gao_da_lu_rail_D26WG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_D26WG')
        gao_da_lu_rail_2_34WG = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_2/34WG')

        gao_da_lu_rail_T2602G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_T2602G')
        gao_da_lu_rail_T2617G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_T2617G')
        gao_da_lu_rail_T2604G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_T2604G')
        gao_da_lu_rail_T2615G = self.env.ref(
            'metro_park_base_data_10.gao_da_lu_rail_T2615G')

        # gao_da_lu_switch_2
        gao_da_lu_switch_2.positive_rail = gao_da_lu_rail_2_34WG.id
        gao_da_lu_switch_2.negative_rail = False
        gao_da_lu_switch_2.header_rail = gao_da_lu_rail_D2G.id
        gao_da_lu_switch_2.positive_switch = False
        gao_da_lu_switch_2.negative_switch = gao_da_lu_switch_4.id
        gao_da_lu_switch_2.header_switch = False
        gao_da_lu_switch_2.x_pos = 360
        gao_da_lu_switch_2.y_pos = 582

        # gao_da_lu_switch_4
        gao_da_lu_switch_4.positive_rail = gao_da_lu_rail_T2617G.id
        gao_da_lu_switch_4.negative_rail = False
        gao_da_lu_switch_4.header_rail = False
        gao_da_lu_switch_4.positive_switch = False
        gao_da_lu_switch_4.negative_switch = gao_da_lu_switch_2.id
        gao_da_lu_switch_4.header_switch = gao_da_lu_switch_14.id
        gao_da_lu_switch_4.x_pos = 360
        gao_da_lu_switch_4.y_pos = 582

        # gao_da_lu_switch_6
        gao_da_lu_switch_6.positive_rail = False
        gao_da_lu_switch_6.negative_rail = False
        gao_da_lu_switch_6.header_rail = gao_da_lu_rail_T2602G.id
        gao_da_lu_switch_6.positive_switch = gao_da_lu_switch_12.id
        gao_da_lu_switch_6.negative_switch = gao_da_lu_switch_8.id
        gao_da_lu_switch_6.header_switch = False
        gao_da_lu_switch_6.x_pos = 360
        gao_da_lu_switch_6.y_pos = 582

        # gao_da_lu_switch_8
        gao_da_lu_switch_8.positive_rail = False
        gao_da_lu_switch_8.negative_rail = False
        gao_da_lu_switch_8.header_rail = False
        gao_da_lu_switch_8.positive_switch = gao_da_lu_switch_10.id
        gao_da_lu_switch_8.negative_switch = gao_da_lu_switch_6.id
        gao_da_lu_switch_8.header_switch = gao_da_lu_switch_22.id
        gao_da_lu_switch_8.x_pos = 360
        gao_da_lu_switch_8.y_pos = 582

        # gao_da_lu_switch_10
        gao_da_lu_switch_10.positive_rail = False
        gao_da_lu_switch_10.negative_rail = False
        gao_da_lu_switch_10.header_rail = gao_da_lu_rail_D4G.id
        gao_da_lu_switch_10.positive_switch = gao_da_lu_switch_8.id
        gao_da_lu_switch_10.negative_switch = gao_da_lu_switch_12.id
        gao_da_lu_switch_10.header_switch = False
        gao_da_lu_switch_10.x_pos = 360
        gao_da_lu_switch_10.y_pos = 582

        # gao_da_lu_switch_12
        gao_da_lu_switch_12.positive_rail = False
        gao_da_lu_switch_12.negative_rail = False
        gao_da_lu_switch_12.header_rail = False
        gao_da_lu_switch_12.positive_switch = gao_da_lu_switch_6.id
        gao_da_lu_switch_12.negative_switch = gao_da_lu_switch_10.id
        gao_da_lu_switch_12.header_switch = gao_da_lu_switch_18.id
        gao_da_lu_switch_12.x_pos = 360
        gao_da_lu_switch_12.y_pos = 582

        # gao_da_lu_switch_14
        gao_da_lu_switch_14.positive_rail = False
        gao_da_lu_switch_14.negative_rail = False
        gao_da_lu_switch_14.header_rail = False
        gao_da_lu_switch_14.positive_switch = gao_da_lu_switch_20.id
        gao_da_lu_switch_14.negative_switch = gao_da_lu_switch_16.id
        gao_da_lu_switch_14.header_switch = gao_da_lu_switch_4.id
        gao_da_lu_switch_14.x_pos = 360
        gao_da_lu_switch_14.y_pos = 582

        # gao_da_lu_switch_16
        gao_da_lu_switch_16.positive_rail = False
        gao_da_lu_switch_16.negative_rail = False
        gao_da_lu_switch_16.header_rail = False
        gao_da_lu_switch_16.positive_switch = gao_da_lu_switch_18.id
        gao_da_lu_switch_16.negative_switch = gao_da_lu_switch_14.id
        gao_da_lu_switch_16.header_switch = gao_da_lu_switch_28.id
        gao_da_lu_switch_16.x_pos = 360
        gao_da_lu_switch_16.y_pos = 582

        # gao_da_lu_switch_18
        gao_da_lu_switch_18.positive_rail = False
        gao_da_lu_switch_18.negative_rail = False
        gao_da_lu_switch_18.header_rail = False
        gao_da_lu_switch_18.positive_switch = gao_da_lu_switch_16.id
        gao_da_lu_switch_18.negative_switch = gao_da_lu_switch_20.id
        gao_da_lu_switch_18.header_switch = gao_da_lu_switch_12.id
        gao_da_lu_switch_18.x_pos = 360
        gao_da_lu_switch_18.y_pos = 582

        # gao_da_lu_switch_20
        gao_da_lu_switch_20.positive_rail = False
        gao_da_lu_switch_20.negative_rail = False
        gao_da_lu_switch_20.header_rail = False
        gao_da_lu_switch_20.positive_switch = gao_da_lu_switch_14.id
        gao_da_lu_switch_20.negative_switch = gao_da_lu_switch_18.id
        gao_da_lu_switch_20.header_switch = gao_da_lu_switch_30.id
        gao_da_lu_switch_20.x_pos = 360
        gao_da_lu_switch_20.y_pos = 582

        # gao_da_lu_switch_22
        gao_da_lu_switch_22.positive_rail = False
        gao_da_lu_switch_22.negative_rail = False
        gao_da_lu_switch_22.header_rail = False
        gao_da_lu_switch_22.positive_switch = gao_da_lu_switch_26.id
        gao_da_lu_switch_22.negative_switch = gao_da_lu_switch_24.id
        gao_da_lu_switch_22.header_switch = gao_da_lu_switch_8.id
        gao_da_lu_switch_22.x_pos = 360
        gao_da_lu_switch_22.y_pos = 582

        # gao_da_lu_switch_24
        gao_da_lu_switch_24.positive_rail = gao_da_lu_rail_24G.id
        gao_da_lu_switch_24.negative_rail = gao_da_lu_rail_23G.id
        gao_da_lu_switch_24.header_rail = False
        gao_da_lu_switch_24.positive_switch = False
        gao_da_lu_switch_24.negative_switch = False
        gao_da_lu_switch_24.header_switch = gao_da_lu_switch_22.id
        gao_da_lu_switch_24.x_pos = 360
        gao_da_lu_switch_24.y_pos = 582

        # gao_da_lu_switch_26
        gao_da_lu_switch_26.positive_rail = False
        gao_da_lu_switch_26.negative_rail = gao_da_lu_rail_25G.id
        gao_da_lu_switch_26.header_rail = False
        gao_da_lu_switch_26.positive_switch = False
        gao_da_lu_switch_26.negative_switch = False
        gao_da_lu_switch_26.header_switch = gao_da_lu_switch_22.id
        gao_da_lu_switch_26.x_pos = 360
        gao_da_lu_switch_26.y_pos = 582

        # gao_da_lu_switch_28
        gao_da_lu_switch_28.positive_rail = False
        gao_da_lu_switch_28.negative_rail = False
        gao_da_lu_switch_28.header_rail = False
        gao_da_lu_switch_28.positive_switch = gao_da_lu_switch_36.id
        gao_da_lu_switch_28.negative_switch = False
        gao_da_lu_switch_28.header_switch = gao_da_lu_switch_16.id
        gao_da_lu_switch_28.x_pos = 360
        gao_da_lu_switch_28.y_pos = 582

        # gao_da_lu_switch_30
        gao_da_lu_switch_30.positive_rail = False
        gao_da_lu_switch_30.negative_rail = False
        gao_da_lu_switch_30.header_rail = False
        gao_da_lu_switch_30.positive_switch = gao_da_lu_switch_38.id
        gao_da_lu_switch_30.negative_switch = gao_da_lu_switch_32.id
        gao_da_lu_switch_30.header_switch = gao_da_lu_switch_20.id
        gao_da_lu_switch_30.x_pos = 360
        gao_da_lu_switch_30.y_pos = 582

        # gao_da_lu_switch_32
        gao_da_lu_switch_32.positive_rail = gao_da_lu_rail_D26WG.id
        gao_da_lu_switch_32.negative_rail = False
        gao_da_lu_switch_32.header_rail = False
        gao_da_lu_switch_32.positive_switch = False
        gao_da_lu_switch_32.negative_switch = gao_da_lu_switch_34.id
        gao_da_lu_switch_32.header_switch = gao_da_lu_switch_30.id
        gao_da_lu_switch_32.x_pos = 360
        gao_da_lu_switch_32.y_pos = 582

        # gao_da_lu_switch_34
        gao_da_lu_switch_34.positive_rail = gao_da_lu_rail_2_34WG.id
        gao_da_lu_switch_34.negative_rail = False
        gao_da_lu_switch_34.header_rail = gao_da_lu_rail_D22G.id
        gao_da_lu_switch_34.positive_switch = False
        gao_da_lu_switch_34.negative_switch = gao_da_lu_switch_32.id
        gao_da_lu_switch_34.header_switch = False
        gao_da_lu_switch_34.x_pos = 360
        gao_da_lu_switch_34.y_pos = 582

        # gao_da_lu_switch_36
        gao_da_lu_switch_36.positive_rail = False
        gao_da_lu_switch_36.negative_rail = False
        gao_da_lu_switch_36.header_rail = False
        gao_da_lu_switch_36.positive_switch = gao_da_lu_switch_54.id
        gao_da_lu_switch_36.negative_switch = False
        gao_da_lu_switch_36.header_switch = gao_da_lu_switch_28.id
        gao_da_lu_switch_36.x_pos = 360
        gao_da_lu_switch_36.y_pos = 582

        # gao_da_lu_switch_38
        gao_da_lu_switch_38.positive_rail = False
        gao_da_lu_switch_38.negative_rail = False
        gao_da_lu_switch_38.header_rail = False
        gao_da_lu_switch_38.positive_switch = gao_da_lu_switch_44.id
        gao_da_lu_switch_38.negative_switch = gao_da_lu_switch_40.id
        gao_da_lu_switch_38.header_switch = gao_da_lu_switch_30.id
        gao_da_lu_switch_38.x_pos = 360
        gao_da_lu_switch_38.y_pos = 582

        # gao_da_lu_switch_40
        gao_da_lu_switch_40.positive_rail = False
        gao_da_lu_switch_40.negative_rail = gao_da_lu_rail_2G.id
        gao_da_lu_switch_40.header_rail = False
        gao_da_lu_switch_40.positive_switch = gao_da_lu_switch_42.id
        gao_da_lu_switch_40.negative_switch = False
        gao_da_lu_switch_40.header_switch = gao_da_lu_switch_38.id
        gao_da_lu_switch_40.x_pos = 360
        gao_da_lu_switch_40.y_pos = 582

        # gao_da_lu_switch_42
        gao_da_lu_switch_42.positive_rail = gao_da_lu_rail_3G.id
        gao_da_lu_switch_42.negative_rail = gao_da_lu_rail_4G.id
        gao_da_lu_switch_42.header_rail = False
        gao_da_lu_switch_42.positive_switch = False
        gao_da_lu_switch_42.negative_switch = False
        gao_da_lu_switch_42.header_switch = gao_da_lu_switch_40.id
        gao_da_lu_switch_42.x_pos = 360
        gao_da_lu_switch_42.y_pos = 582

        # gao_da_lu_switch_44
        gao_da_lu_switch_44.positive_rail = False
        gao_da_lu_switch_44.negative_rail = False
        gao_da_lu_switch_44.header_rail = False
        gao_da_lu_switch_44.positive_switch = gao_da_lu_switch_50.id
        gao_da_lu_switch_44.negative_switch = gao_da_lu_switch_46.id
        gao_da_lu_switch_44.header_switch = gao_da_lu_switch_38.id
        gao_da_lu_switch_44.x_pos = 360
        gao_da_lu_switch_44.y_pos = 582

        # gao_da_lu_switch_46
        gao_da_lu_switch_46.positive_rail = gao_da_lu_rail_7AG.id
        gao_da_lu_switch_46.negative_rail = False
        gao_da_lu_switch_46.header_rail = False
        gao_da_lu_switch_46.positive_switch = False
        gao_da_lu_switch_46.negative_switch = gao_da_lu_switch_48.id
        gao_da_lu_switch_46.header_switch = gao_da_lu_switch_44.id
        gao_da_lu_switch_46.x_pos = 360
        gao_da_lu_switch_46.y_pos = 582

        # gao_da_lu_switch_48
        gao_da_lu_switch_48.positive_rail = gao_da_lu_rail_5AG.id
        gao_da_lu_switch_48.negative_rail = gao_da_lu_rail_6AG.id
        gao_da_lu_switch_48.header_rail = False
        gao_da_lu_switch_48.positive_switch = False
        gao_da_lu_switch_48.negative_switch = False
        gao_da_lu_switch_48.header_switch = gao_da_lu_switch_46.id
        gao_da_lu_switch_48.x_pos = 360
        gao_da_lu_switch_48.y_pos = 582

        # gao_da_lu_switch_50
        gao_da_lu_switch_50.positive_rail = gao_da_lu_rail_10AG.id
        gao_da_lu_switch_50.negative_rail = False
        gao_da_lu_switch_50.header_rail = False
        gao_da_lu_switch_50.positive_switch = False
        gao_da_lu_switch_50.negative_switch = gao_da_lu_switch_52.id
        gao_da_lu_switch_50.header_switch = gao_da_lu_switch_44.id
        gao_da_lu_switch_50.x_pos = 360
        gao_da_lu_switch_50.y_pos = 582

        # gao_da_lu_switch_52
        gao_da_lu_switch_52.positive_rail = gao_da_lu_rail_8AG.id
        gao_da_lu_switch_52.negative_rail = gao_da_lu_rail_9AG.id
        gao_da_lu_switch_52.header_rail = False
        gao_da_lu_switch_52.positive_switch = False
        gao_da_lu_switch_52.negative_switch = False
        gao_da_lu_switch_52.header_switch = gao_da_lu_switch_50.id
        gao_da_lu_switch_52.x_pos = 360
        gao_da_lu_switch_52.y_pos = 582

        # gao_da_lu_switch_54
        gao_da_lu_switch_54.positive_rail = False
        gao_da_lu_switch_54.negative_rail = False
        gao_da_lu_switch_54.header_rail = False
        gao_da_lu_switch_54.positive_switch = gao_da_lu_switch_60.id
        gao_da_lu_switch_54.negative_switch = gao_da_lu_switch_56.id
        gao_da_lu_switch_54.header_switch = gao_da_lu_switch_36.id
        gao_da_lu_switch_54.x_pos = 360
        gao_da_lu_switch_54.y_pos = 582

        # gao_da_lu_switch_56
        gao_da_lu_switch_56.positive_rail = False
        gao_da_lu_switch_56.negative_rail = gao_da_lu_rail_16AG.id
        gao_da_lu_switch_56.header_rail = False
        gao_da_lu_switch_56.positive_switch = gao_da_lu_switch_58.id
        gao_da_lu_switch_56.negative_switch = False
        gao_da_lu_switch_56.header_switch = gao_da_lu_switch_54.id
        gao_da_lu_switch_56.x_pos = 360
        gao_da_lu_switch_56.y_pos = 582

        # gao_da_lu_switch_58
        gao_da_lu_switch_58.positive_rail = gao_da_lu_rail_14AG.id
        gao_da_lu_switch_58.negative_rail = gao_da_lu_rail_15AG.id
        gao_da_lu_switch_58.header_rail = False
        gao_da_lu_switch_58.positive_switch = False
        gao_da_lu_switch_58.negative_switch = False
        gao_da_lu_switch_58.header_switch = gao_da_lu_switch_56.id
        gao_da_lu_switch_58.x_pos = 360
        gao_da_lu_switch_58.y_pos = 582

        # gao_da_lu_switch_60
        gao_da_lu_switch_60.positive_rail = gao_da_lu_rail_11AG.id
        gao_da_lu_switch_60.negative_rail = False
        gao_da_lu_switch_60.header_rail = False
        gao_da_lu_switch_60.positive_switch = False
        gao_da_lu_switch_60.negative_switch = gao_da_lu_switch_62.id
        gao_da_lu_switch_60.header_switch = gao_da_lu_switch_54.id
        gao_da_lu_switch_60.x_pos = 360
        gao_da_lu_switch_60.y_pos = 582

        # gao_da_lu_switch_62
        gao_da_lu_switch_62.positive_rail = gao_da_lu_rail_13AG.id
        gao_da_lu_switch_62.negative_rail = gao_da_lu_rail_12AG.id
        gao_da_lu_switch_62.header_rail = False
        gao_da_lu_switch_62.positive_switch = False
        gao_da_lu_switch_62.negative_switch = False
        gao_da_lu_switch_62.header_switch = gao_da_lu_switch_60.id
        gao_da_lu_switch_62.x_pos = 360
        gao_da_lu_switch_62.y_pos = 582

        # gao_da_lu_rail_1G
        gao_da_lu_rail_1G.left_rail_id = gao_da_lu_rail_D26WG.id
        gao_da_lu_rail_1G.right_rail_id = False
        gao_da_lu_rail_1G.left_switch_id = False
        gao_da_lu_rail_1G.right_switch_id = False
        gao_da_lu_rail_1G.left_switch_position = False
        gao_da_lu_rail_1G.right_switch_position = False
        gao_da_lu_rail_1G.x_pos = 1396
        gao_da_lu_rail_1G.y_pos = 253

        # gao_da_lu_rail_2G
        gao_da_lu_rail_2G.left_rail_id = False
        gao_da_lu_rail_2G.right_rail_id = False
        gao_da_lu_rail_2G.left_switch_id = gao_da_lu_switch_40.id
        gao_da_lu_rail_2G.right_switch_id = False
        gao_da_lu_rail_2G.left_switch_position = 'negative'
        gao_da_lu_rail_2G.right_switch_position = False
        gao_da_lu_rail_2G.x_pos = 1396
        gao_da_lu_rail_2G.y_pos = 253

        # gao_da_lu_rail_3G
        gao_da_lu_rail_3G.left_rail_id = False
        gao_da_lu_rail_3G.right_rail_id = False
        gao_da_lu_rail_3G.left_switch_id = gao_da_lu_switch_42.id
        gao_da_lu_rail_3G.right_switch_id = False
        gao_da_lu_rail_3G.left_switch_position = 'positive'
        gao_da_lu_rail_3G.right_switch_position = False
        gao_da_lu_rail_3G.x_pos = 1396
        gao_da_lu_rail_3G.y_pos = 253

        # gao_da_lu_rail_2_34WG
        gao_da_lu_rail_2_34WG.left_rail_id = False
        gao_da_lu_rail_2_34WG.right_rail_id = False
        gao_da_lu_rail_2_34WG.left_switch_id = gao_da_lu_switch_2.id
        gao_da_lu_rail_2_34WG.right_switch_id = gao_da_lu_switch_34.id
        gao_da_lu_rail_2_34WG.left_switch_position = 'positive'
        gao_da_lu_rail_2_34WG.right_switch_position = 'positive'
        gao_da_lu_rail_2_34WG.x_pos = 1396
        gao_da_lu_rail_2_34WG.y_pos = 253

        # gao_da_lu_rail_D2G
        gao_da_lu_rail_D2G.left_rail_id = False
        gao_da_lu_rail_D2G.right_rail_id = False
        gao_da_lu_rail_D2G.left_switch_id = False
        gao_da_lu_rail_D2G.right_switch_id = gao_da_lu_switch_2.id
        gao_da_lu_rail_D2G.left_switch_position = False
        gao_da_lu_rail_D2G.right_switch_position = 'header'
        gao_da_lu_rail_D2G.x_pos = 1396
        gao_da_lu_rail_D2G.y_pos = 253

        # gao_da_lu_rail_D22G
        gao_da_lu_rail_D22G.left_rail_id = False
        gao_da_lu_rail_D22G.right_rail_id = False
        gao_da_lu_rail_D22G.left_switch_id = gao_da_lu_switch_34.id
        gao_da_lu_rail_D22G.right_switch_id = False
        gao_da_lu_rail_D22G.left_switch_position = 'header'
        gao_da_lu_rail_D22G.right_switch_position = False
        gao_da_lu_rail_D22G.x_pos = 1396
        gao_da_lu_rail_D22G.y_pos = 253

        # gao_da_lu_rail_D26WG
        gao_da_lu_rail_D26WG.left_rail_id = False
        gao_da_lu_rail_D26WG.right_rail_id = gao_da_lu_rail_1G.id
        gao_da_lu_rail_D26WG.left_switch_id = gao_da_lu_switch_32.id
        gao_da_lu_rail_D26WG.right_switch_id = False
        gao_da_lu_rail_D26WG.left_switch_position = 'positive'
        gao_da_lu_rail_D26WG.right_switch_position = False
        gao_da_lu_rail_D26WG.x_pos = 1396
        gao_da_lu_rail_D26WG.y_pos = 253

        # gao_da_lu_rail_5AG
        gao_da_lu_rail_5AG.left_rail_id = False
        gao_da_lu_rail_5AG.right_rail_id = gao_da_lu_rail_5BG.id
        gao_da_lu_rail_5AG.left_switch_id = gao_da_lu_switch_48.id
        gao_da_lu_rail_5AG.right_switch_id = False
        gao_da_lu_rail_5AG.left_switch_position = 'positive'
        gao_da_lu_rail_5AG.right_switch_position = False
        gao_da_lu_rail_5AG.x_pos = 1396
        gao_da_lu_rail_5AG.y_pos = 253

        # gao_da_lu_rail_5BG
        gao_da_lu_rail_5BG.left_rail_id = gao_da_lu_rail_5AG.id
        gao_da_lu_rail_5BG.right_rail_id = False
        gao_da_lu_rail_5BG.left_switch_id = False
        gao_da_lu_rail_5BG.right_switch_id = False
        gao_da_lu_rail_5BG.left_switch_position = False
        gao_da_lu_rail_5BG.right_switch_position = False
        gao_da_lu_rail_5BG.x_pos = 1396
        gao_da_lu_rail_5BG.y_pos = 253

        # gao_da_lu_rail_6AG
        gao_da_lu_rail_6AG.left_rail_id = False
        gao_da_lu_rail_6AG.right_rail_id = gao_da_lu_rail_6BG.id
        gao_da_lu_rail_6AG.left_switch_id = gao_da_lu_switch_48.id
        gao_da_lu_rail_6AG.right_switch_id = False
        gao_da_lu_rail_6AG.left_switch_position = 'negative'
        gao_da_lu_rail_6AG.right_switch_position = False
        gao_da_lu_rail_6AG.x_pos = 1396
        gao_da_lu_rail_6AG.y_pos = 253

        # gao_da_lu_rail_6BG
        gao_da_lu_rail_6BG.left_rail_id = False
        gao_da_lu_rail_6BG.right_rail_id = gao_da_lu_rail_6AG.id
        gao_da_lu_rail_6BG.left_switch_id = False
        gao_da_lu_rail_6BG.right_switch_id = False
        gao_da_lu_rail_6BG.left_switch_position = False
        gao_da_lu_rail_6BG.right_switch_position = False
        gao_da_lu_rail_6BG.x_pos = 1396
        gao_da_lu_rail_6BG.y_pos = 253

        # gao_da_lu_rail_7AG
        gao_da_lu_rail_7AG.left_rail_id = False
        gao_da_lu_rail_7AG.right_rail_id = gao_da_lu_rail_7BG.id
        gao_da_lu_rail_7AG.left_switch_id = gao_da_lu_switch_46.id
        gao_da_lu_rail_7AG.right_switch_id = False
        gao_da_lu_rail_7AG.left_switch_position = 'positive'
        gao_da_lu_rail_7AG.right_switch_position = False
        gao_da_lu_rail_7AG.x_pos = 1396
        gao_da_lu_rail_7AG.y_pos = 253

        # gao_da_lu_rail_7BG
        gao_da_lu_rail_7BG.left_rail_id = gao_da_lu_rail_7AG.id
        gao_da_lu_rail_7BG.right_rail_id = False
        gao_da_lu_rail_7BG.left_switch_id = False
        gao_da_lu_rail_7BG.right_switch_id = False
        gao_da_lu_rail_7BG.left_switch_position = False
        gao_da_lu_rail_7BG.right_switch_position = False
        gao_da_lu_rail_7BG.x_pos = 1396
        gao_da_lu_rail_7BG.y_pos = 253

        # gao_da_lu_rail_8AG
        gao_da_lu_rail_8AG.left_rail_id = False
        gao_da_lu_rail_8AG.right_rail_id = gao_da_lu_rail_8BG.id
        gao_da_lu_rail_8AG.left_switch_id = gao_da_lu_switch_52.id
        gao_da_lu_rail_8AG.right_switch_id = False
        gao_da_lu_rail_8AG.left_switch_position = 'positive'
        gao_da_lu_rail_8AG.right_switch_position = False
        gao_da_lu_rail_8AG.x_pos = 1396
        gao_da_lu_rail_8AG.y_pos = 253

        # gao_da_lu_rail_8BG
        gao_da_lu_rail_8BG.left_rail_id = gao_da_lu_rail_8AG.id
        gao_da_lu_rail_8BG.right_rail_id = False
        gao_da_lu_rail_8BG.left_switch_id = False
        gao_da_lu_rail_8BG.right_switch_id = False
        gao_da_lu_rail_8BG.left_switch_position = False
        gao_da_lu_rail_8BG.right_switch_position = False
        gao_da_lu_rail_8BG.x_pos = 1396
        gao_da_lu_rail_8BG.y_pos = 253

        # gao_da_lu_rail_9AG
        gao_da_lu_rail_9AG.left_rail_id = False
        gao_da_lu_rail_9AG.right_rail_id = gao_da_lu_rail_9BG.id
        gao_da_lu_rail_9AG.left_switch_id = gao_da_lu_switch_52.id
        gao_da_lu_rail_9AG.right_switch_id = False
        gao_da_lu_rail_9AG.left_switch_position = 'negative'
        gao_da_lu_rail_9AG.right_switch_position = False
        gao_da_lu_rail_9AG.x_pos = 1396
        gao_da_lu_rail_9AG.y_pos = 253

        # gao_da_lu_rail_9BG
        gao_da_lu_rail_9BG.left_rail_id = gao_da_lu_rail_9AG.id
        gao_da_lu_rail_9BG.right_rail_id = False
        gao_da_lu_rail_9BG.left_switch_id = False
        gao_da_lu_rail_9BG.right_switch_id = False
        gao_da_lu_rail_9BG.left_switch_position = False
        gao_da_lu_rail_9BG.right_switch_position = False
        gao_da_lu_rail_9BG.x_pos = 1396
        gao_da_lu_rail_9BG.y_pos = 253

        # gao_da_lu_rail_10AG
        gao_da_lu_rail_10AG.left_rail_id = False
        gao_da_lu_rail_10AG.right_rail_id = gao_da_lu_rail_10BG.id
        gao_da_lu_rail_10AG.left_switch_id = gao_da_lu_switch_50.id
        gao_da_lu_rail_10AG.right_switch_id = False
        gao_da_lu_rail_10AG.left_switch_position = 'positive'
        gao_da_lu_rail_10AG.right_switch_position = False
        gao_da_lu_rail_10AG.x_pos = 1396
        gao_da_lu_rail_10AG.y_pos = 253

        # gao_da_lu_rail_10BG
        gao_da_lu_rail_10BG.left_rail_id = gao_da_lu_rail_10AG.id
        gao_da_lu_rail_10BG.right_rail_id = False
        gao_da_lu_rail_10BG.left_switch_id = False
        gao_da_lu_rail_10BG.right_switch_id = False
        gao_da_lu_rail_10BG.left_switch_position = False
        gao_da_lu_rail_10BG.right_switch_position = False
        gao_da_lu_rail_10BG.x_pos = 1396
        gao_da_lu_rail_10BG.y_pos = 253

        # gao_da_lu_rail_11AG
        gao_da_lu_rail_11AG.left_rail_id = False
        gao_da_lu_rail_11AG.right_rail_id = gao_da_lu_rail_11BG.id
        gao_da_lu_rail_11AG.left_switch_id = gao_da_lu_switch_60.id
        gao_da_lu_rail_11AG.right_switch_id = False
        gao_da_lu_rail_11AG.left_switch_position = 'positive'
        gao_da_lu_rail_11AG.right_switch_position = False
        gao_da_lu_rail_11AG.x_pos = 1396
        gao_da_lu_rail_11AG.y_pos = 253

        # gao_da_lu_rail_11BG
        gao_da_lu_rail_11BG.left_rail_id = gao_da_lu_rail_11AG.id
        gao_da_lu_rail_11BG.right_rail_id = False
        gao_da_lu_rail_11BG.left_switch_id = False
        gao_da_lu_rail_11BG.right_switch_id = False
        gao_da_lu_rail_11BG.left_switch_position = False
        gao_da_lu_rail_11BG.right_switch_position = False
        gao_da_lu_rail_11BG.x_pos = 1396
        gao_da_lu_rail_11BG.y_pos = 253

        # gao_da_lu_rail_12AG
        gao_da_lu_rail_12AG.left_rail_id = False
        gao_da_lu_rail_12AG.right_rail_id = gao_da_lu_rail_12BG.id
        gao_da_lu_rail_12AG.left_switch_id = gao_da_lu_switch_62.id
        gao_da_lu_rail_12AG.right_switch_id = False
        gao_da_lu_rail_12AG.left_switch_position = 'negative'
        gao_da_lu_rail_12AG.right_switch_position = False
        gao_da_lu_rail_12AG.x_pos = 1396
        gao_da_lu_rail_12AG.y_pos = 253

        # gao_da_lu_rail_13AG
        gao_da_lu_rail_13AG.left_rail_id = False
        gao_da_lu_rail_13AG.right_rail_id = gao_da_lu_rail_13BG.id
        gao_da_lu_rail_13AG.left_switch_id = gao_da_lu_switch_62.id
        gao_da_lu_rail_13AG.right_switch_id = False
        gao_da_lu_rail_13AG.left_switch_position = 'positive'
        gao_da_lu_rail_13AG.right_switch_position = False
        gao_da_lu_rail_13AG.x_pos = 1396
        gao_da_lu_rail_13AG.y_pos = 253

        # gao_da_lu_rail_14AG
        gao_da_lu_rail_14AG.left_rail_id = False
        gao_da_lu_rail_14AG.right_rail_id = gao_da_lu_rail_14BG.id
        gao_da_lu_rail_14AG.left_switch_id = gao_da_lu_switch_58.id
        gao_da_lu_rail_14AG.right_switch_id = False
        gao_da_lu_rail_14AG.left_switch_position = 'positive'
        gao_da_lu_rail_14AG.right_switch_position = False
        gao_da_lu_rail_14AG.x_pos = 1396
        gao_da_lu_rail_14AG.y_pos = 253

        # gao_da_lu_rail_15AG
        gao_da_lu_rail_15AG.left_rail_id = False
        gao_da_lu_rail_15AG.right_rail_id = gao_da_lu_rail_15BG.id
        gao_da_lu_rail_15AG.left_switch_id = gao_da_lu_switch_58.id
        gao_da_lu_rail_15AG.right_switch_id = False
        gao_da_lu_rail_15AG.left_switch_position = 'negative'
        gao_da_lu_rail_15AG.right_switch_position = False
        gao_da_lu_rail_15AG.x_pos = 1396
        gao_da_lu_rail_15AG.y_pos = 253

        # gao_da_lu_rail_15BG
        gao_da_lu_rail_15BG.left_rail_id = gao_da_lu_rail_15AG.id
        gao_da_lu_rail_15BG.right_rail_id = False
        gao_da_lu_rail_15BG.left_switch_id = False
        gao_da_lu_rail_15BG.right_switch_id = False
        gao_da_lu_rail_15BG.left_switch_position = False
        gao_da_lu_rail_15BG.right_switch_position = False
        gao_da_lu_rail_15BG.x_pos = 1396
        gao_da_lu_rail_15BG.y_pos = 253

        # gao_da_lu_rail_16AG
        gao_da_lu_rail_16AG.left_rail_id = False
        gao_da_lu_rail_16AG.right_rail_id = gao_da_lu_rail_16BG.id
        gao_da_lu_rail_16AG.left_switch_id = gao_da_lu_switch_56.id
        gao_da_lu_rail_16AG.right_switch_id = False
        gao_da_lu_rail_16AG.left_switch_position = 'negative'
        gao_da_lu_rail_16AG.right_switch_position = False
        gao_da_lu_rail_16AG.x_pos = 1396
        gao_da_lu_rail_16AG.y_pos = 253

        # gao_da_lu_rail_16BG
        gao_da_lu_rail_16BG.left_rail_id = gao_da_lu_rail_16AG.id
        gao_da_lu_rail_16BG.right_rail_id = False
        gao_da_lu_rail_16BG.left_switch_id = False
        gao_da_lu_rail_16BG.right_switch_id = False
        gao_da_lu_rail_16BG.left_switch_position = False
        gao_da_lu_rail_16BG.right_switch_position = False
        gao_da_lu_rail_16BG.x_pos = 1396
        gao_da_lu_rail_16BG.y_pos = 253

        # gao_da_lu_rail_12BG
        gao_da_lu_rail_12BG.left_rail_id = gao_da_lu_rail_12AG.id
        gao_da_lu_rail_12BG.right_rail_id = False
        gao_da_lu_rail_12BG.left_switch_id = False
        gao_da_lu_rail_12BG.right_switch_id = False
        gao_da_lu_rail_12BG.left_switch_position = False
        gao_da_lu_rail_12BG.right_switch_position = False
        gao_da_lu_rail_12BG.x_pos = 1396
        gao_da_lu_rail_12BG.y_pos = 253

        # gao_da_lu_rail_13BG
        gao_da_lu_rail_13BG.left_rail_id = gao_da_lu_rail_13AG.id
        gao_da_lu_rail_13BG.right_rail_id = False
        gao_da_lu_rail_13BG.left_switch_id = False
        gao_da_lu_rail_13BG.right_switch_id = False
        gao_da_lu_rail_13BG.left_switch_position = False
        gao_da_lu_rail_13BG.right_switch_position = False
        gao_da_lu_rail_13BG.x_pos = 1396
        gao_da_lu_rail_13BG.y_pos = 253

        # gao_da_lu_rail_14BG
        gao_da_lu_rail_14BG.left_rail_id = gao_da_lu_rail_14AG.id
        gao_da_lu_rail_14BG.right_rail_id = False
        gao_da_lu_rail_14BG.left_switch_id = False
        gao_da_lu_rail_14BG.right_switch_id = False
        gao_da_lu_rail_14BG.left_switch_position = False
        gao_da_lu_rail_14BG.right_switch_position = False
        gao_da_lu_rail_14BG.x_pos = 1396
        gao_da_lu_rail_14BG.y_pos = 253

        # gao_da_lu_rail_D4G
        gao_da_lu_rail_D4G.left_rail_id = False
        gao_da_lu_rail_D4G.right_rail_id = False
        gao_da_lu_rail_D4G.left_switch_id = False
        gao_da_lu_rail_D4G.right_switch_id = gao_da_lu_switch_10.id
        gao_da_lu_rail_D4G.left_switch_position = False
        gao_da_lu_rail_D4G.right_switch_position = 'header'
        gao_da_lu_rail_D4G.x_pos = 1396
        gao_da_lu_rail_D4G.y_pos = 253

        # gao_da_lu_rail_T2602G
        gao_da_lu_rail_T2602G.left_rail_id = gao_da_lu_rail_T2604G.id
        gao_da_lu_rail_T2602G.right_rail_id = False
        gao_da_lu_rail_T2602G.left_switch_id = False
        gao_da_lu_rail_T2602G.right_switch_id = gao_da_lu_switch_6.id
        gao_da_lu_rail_T2602G.left_switch_position = False
        gao_da_lu_rail_T2602G.right_switch_position = 'header'
        gao_da_lu_rail_T2602G.x_pos = 1396
        gao_da_lu_rail_T2602G.y_pos = 253

        # gao_da_lu_rail_T2604G
        gao_da_lu_rail_T2604G.left_rail_id = False
        gao_da_lu_rail_T2604G.right_rail_id = gao_da_lu_rail_T2602G.id
        gao_da_lu_rail_T2604G.left_switch_id = False
        gao_da_lu_rail_T2604G.right_switch_id = False
        gao_da_lu_rail_T2604G.left_switch_position = False
        gao_da_lu_rail_T2604G.right_switch_position = False
        gao_da_lu_rail_T2604G.x_pos = 1396
        gao_da_lu_rail_T2604G.y_pos = 253

        # gao_da_lu_rail_23G
        gao_da_lu_rail_23G.left_rail_id = False
        gao_da_lu_rail_23G.right_rail_id = False
        gao_da_lu_rail_23G.left_switch_id = gao_da_lu_switch_24.id
        gao_da_lu_rail_23G.right_switch_id = False
        gao_da_lu_rail_23G.left_switch_position = 'negative'
        gao_da_lu_rail_23G.right_switch_position = False
        gao_da_lu_rail_23G.x_pos = 1396
        gao_da_lu_rail_23G.y_pos = 253

        # gao_da_lu_rail_24G
        gao_da_lu_rail_24G.left_rail_id = False
        gao_da_lu_rail_24G.right_rail_id = False
        gao_da_lu_rail_24G.left_switch_id = gao_da_lu_switch_24.id
        gao_da_lu_rail_24G.right_switch_id = False
        gao_da_lu_rail_24G.left_switch_position = 'positive'
        gao_da_lu_rail_24G.right_switch_position = False
        gao_da_lu_rail_24G.x_pos = 1396
        gao_da_lu_rail_24G.y_pos = 253

        # gao_da_lu_rail_25G
        gao_da_lu_rail_25G.left_rail_id = False
        gao_da_lu_rail_25G.right_rail_id = False
        gao_da_lu_rail_25G.left_switch_id = gao_da_lu_switch_26.id
        gao_da_lu_rail_25G.right_switch_id = False
        gao_da_lu_rail_25G.left_switch_position = 'negative'
        gao_da_lu_rail_25G.right_switch_position = False
        gao_da_lu_rail_25G.x_pos = 1396
        gao_da_lu_rail_25G.y_pos = 253

        # gao_da_lu_rail_T2617G
        gao_da_lu_rail_T2617G.left_rail_id = gao_da_lu_rail_T2615G.id
        gao_da_lu_rail_T2617G.right_rail_id = False
        gao_da_lu_rail_T2617G.left_switch_id = False
        gao_da_lu_rail_T2617G.right_switch_id = gao_da_lu_switch_4.id
        gao_da_lu_rail_T2617G.left_switch_position = False
        gao_da_lu_rail_T2617G.right_switch_position = 'positive'
        gao_da_lu_rail_T2617G.x_pos = 1396
        gao_da_lu_rail_T2617G.y_pos = 253

        # gao_da_lu_rail_T2615G
        gao_da_lu_rail_T2615G.left_rail_id = False
        gao_da_lu_rail_T2615G.right_rail_id = gao_da_lu_rail_T2617G.id
        gao_da_lu_rail_T2615G.left_switch_id = False
        gao_da_lu_rail_T2615G.right_switch_id = False
        gao_da_lu_rail_T2615G.left_switch_position = False
        gao_da_lu_rail_T2615G.right_switch_position = False
        gao_da_lu_rail_T2615G.x_pos = 1396
        gao_da_lu_rail_T2615G.y_pos = 253
