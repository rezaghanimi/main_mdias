# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitRailAndSwitches(models.TransientModel):
    '''
    初始化轨道和道岔信息
    '''
    _name = 'metro_park_base_data_6.init_rail_and_switches'

    name = fields.Char(string='name')

    @api.model
    def init_switches(self):
        '''
        建立道岔位置关系, 一定要先把道岔和轨道建立了才行
        :return:
        '''

        hui_long_switch_1 = self.env.ref('metro_park_base.hui_long_switch_1')
        hui_long_switch_3 = self.env.ref('metro_park_base.hui_long_switch_3')
        hui_long_switch_5 = self.env.ref('metro_park_base.hui_long_switch_5')
        hui_long_switch_7 = self.env.ref('metro_park_base.hui_long_switch_7')
        hui_long_switch_9 = self.env.ref('metro_park_base.hui_long_switch_9')
        hui_long_switch_11 = self.env.ref('metro_park_base.hui_long_switch_11')
        hui_long_switch_13 = self.env.ref('metro_park_base.hui_long_switch_13')
        hui_long_switch_15 = self.env.ref('metro_park_base.hui_long_switch_15')
        hui_long_switch_17 = self.env.ref('metro_park_base.hui_long_switch_17')
        hui_long_switch_19 = self.env.ref('metro_park_base.hui_long_switch_19')
        hui_long_switch_21 = self.env.ref('metro_park_base.hui_long_switch_21')
        hui_long_switch_23 = self.env.ref('metro_park_base.hui_long_switch_23')
        hui_long_switch_25 = self.env.ref('metro_park_base.hui_long_switch_25')
        hui_long_switch_27 = self.env.ref('metro_park_base.hui_long_switch_27')
        hui_long_switch_29 = self.env.ref('metro_park_base.hui_long_switch_29')
        hui_long_switch_31 = self.env.ref('metro_park_base.hui_long_switch_31')
        hui_long_switch_33 = self.env.ref('metro_park_base.hui_long_switch_33')
        hui_long_switch_35 = self.env.ref('metro_park_base.hui_long_switch_35')
        hui_long_switch_37 = self.env.ref('metro_park_base.hui_long_switch_37')
        hui_long_switch_39 = self.env.ref('metro_park_base.hui_long_switch_39')
        hui_long_switch_41 = self.env.ref('metro_park_base.hui_long_switch_41')
        hui_long_switch_43 = self.env.ref('metro_park_base.hui_long_switch_43')
        hui_long_switch_45 = self.env.ref('metro_park_base.hui_long_switch_45')
        hui_long_switch_47 = self.env.ref('metro_park_base.hui_long_switch_47')
        hui_long_switch_49 = self.env.ref('metro_park_base.hui_long_switch_49')
        hui_long_switch_51 = self.env.ref('metro_park_base.hui_long_switch_51')
        hui_long_switch_53 = self.env.ref('metro_park_base.hui_long_switch_53')
        hui_long_switch_55 = self.env.ref('metro_park_base.hui_long_switch_55')
        hui_long_switch_57 = self.env.ref('metro_park_base.hui_long_switch_57')
        hui_long_switch_59 = self.env.ref('metro_park_base.hui_long_switch_59')
        hui_long_switch_61 = self.env.ref('metro_park_base.hui_long_switch_61')
        hui_long_switch_63 = self.env.ref('metro_park_base.hui_long_switch_63')
        hui_long_switch_65 = self.env.ref('metro_park_base.hui_long_switch_65')
        hui_long_switch_67 = self.env.ref('metro_park_base.hui_long_switch_67')
        hui_long_switch_69 = self.env.ref('metro_park_base.hui_long_switch_69')
        hui_long_switch_71 = self.env.ref('metro_park_base.hui_long_switch_71')
        hui_long_switch_73 = self.env.ref('metro_park_base.hui_long_switch_73')

        # 所有的区段

        hui_long_rail_D1G = self.env.ref('metro_park_base.hui_long_rail_D1G')
        hui_long_rail_3_5DG = self.env.ref(
            'metro_park_base.hui_long_rail_3-5DG')
        hui_long_rail_3_19WG = self.env.ref(
            'metro_park_base.hui_long_rail_3/19WG')
        hui_long_rail_19_21WG = self.env.ref(
            'metro_park_base.hui_long_rail_19/21WG')
        hui_long_rail_21_25DG = self.env.ref(
            'metro_park_base.hui_long_rail_21-25DG')
        hui_long_rail_1G = self.env.ref('metro_park_base.hui_long_rail_1G')
        hui_long_rail_2G = self.env.ref('metro_park_base.hui_long_rail_2G')
        hui_long_rail_3G = self.env.ref('metro_park_base.hui_long_rail_3G')
        hui_long_rail_T6604G = self.env.ref(
            'metro_park_base.hui_long_rail_T6604G')
        hui_long_rail_T6602G = self.env.ref(
            'metro_park_base.hui_long_rail_T6602G')
        hui_long_rail_1_7DG = self.env.ref(
            'metro_park_base.hui_long_rail_1-7DG')
        hui_long_rail_9_15DG = self.env.ref(
            'metro_park_base.hui_long_rail_9-15DG')
        hui_long_rail_17_31DG = self.env.ref(
            'metro_park_base.hui_long_rail_17-31DG')
        hui_long_rail_29_33DG = self.env.ref(
            'metro_park_base.hui_long_rail_29-33DG')
        hui_long_rail_39DG = self.env.ref('metro_park_base.hui_long_rail_39DG')
        hui_long_rail_41DG = self.env.ref('metro_park_base.hui_long_rail_41DG')
        hui_long_rail_43_47DG = self.env.ref(
            'metro_park_base.hui_long_rail_43-47DG')
        hui_long_rail_4AG = self.env.ref('metro_park_base.hui_long_rail_4AG')
        hui_long_rail_5AG = self.env.ref('metro_park_base.hui_long_rail_5AG')
        hui_long_rail_6AG = self.env.ref('metro_park_base.hui_long_rail_6AG')
        hui_long_rail_7AG = self.env.ref('metro_park_base.hui_long_rail_7AG')
        hui_long_rail_8AG = self.env.ref('metro_park_base.hui_long_rail_8AG')
        hui_long_rail_9AG = self.env.ref('metro_park_base.hui_long_rail_9AG')
        hui_long_rail_10AG = self.env.ref('metro_park_base.hui_long_rail_10AG')
        hui_long_rail_11AG = self.env.ref('metro_park_base.hui_long_rail_11AG')
        hui_long_rail_12AG = self.env.ref('metro_park_base.hui_long_rail_12AG')
        hui_long_rail_13AG = self.env.ref('metro_park_base.hui_long_rail_13AG')
        hui_long_rail_14AG = self.env.ref('metro_park_base.hui_long_rail_14AG')
        hui_long_rail_15AG = self.env.ref('metro_park_base.hui_long_rail_15AG')
        hui_long_rail_4BG = self.env.ref('metro_park_base.hui_long_rail_4BG')
        hui_long_rail_5BG = self.env.ref('metro_park_base.hui_long_rail_5BG')
        hui_long_rail_6BG = self.env.ref('metro_park_base.hui_long_rail_6BG')
        hui_long_rail_7BG = self.env.ref('metro_park_base.hui_long_rail_7BG')
        hui_long_rail_8BG = self.env.ref('metro_park_base.hui_long_rail_8BG')
        hui_long_rail_9BG = self.env.ref('metro_park_base.hui_long_rail_9BG')
        hui_long_rail_10BG = self.env.ref('metro_park_base.hui_long_rail_10BG')
        hui_long_rail_11BG = self.env.ref('metro_park_base.hui_long_rail_11BG')
        hui_long_rail_12BG = self.env.ref('metro_park_base.hui_long_rail_12BG')
        hui_long_rail_13BG = self.env.ref('metro_park_base.hui_long_rail_13BG')
        hui_long_rail_14BG = self.env.ref('metro_park_base.hui_long_rail_14BG')
        hui_long_rail_15BG = self.env.ref('metro_park_base.hui_long_rail_15BG')
        hui_long_rail_T6615G = self.env.ref(
            'metro_park_base.hui_long_rail_T6615G')
        hui_long_rail_T6617G = self.env.ref(
            'metro_park_base.hui_long_rail_T6617G')
        hui_long_rail_D9G = self.env.ref('metro_park_base.hui_long_rail_D9G')
        hui_long_rail_11_13DG = self.env.ref(
            'metro_park_base.hui_long_rail_11-13DG')
        hui_long_rail_49_61DG = self.env.ref(
            'metro_park_base.hui_long_rail_49-61DG')
        hui_long_rail_69_73DG = self.env.ref(
            'metro_park_base.hui_long_rail_69-73DG')
        hui_long_rail_57DG = self.env.ref('metro_park_base.hui_long_rail_57DG')
        hui_long_rail_51_53DG = self.env.ref(
            'metro_park_base.hui_long_rail_51-53DG')
        hui_long_rail_D23G = self.env.ref('metro_park_base.hui_long_rail_D23G')
        hui_long_rail_67DG = self.env.ref('metro_park_base.hui_long_rail_67DG')
        hui_long_rail_25G = self.env.ref('metro_park_base.hui_long_rail_25G')
        hui_long_rail_26G = self.env.ref('metro_park_base.hui_long_rail_26G')
        hui_long_rail_27G = self.env.ref('metro_park_base.hui_long_rail_27G')
        hui_long_rail_28G = self.env.ref('metro_park_base.hui_long_rail_28G')
        hui_long_rail_29G = self.env.ref('metro_park_base.hui_long_rail_29G')
        hui_long_rail_16AG = self.env.ref('metro_park_base.hui_long_rail_16AG')
        hui_long_rail_17AG = self.env.ref('metro_park_base.hui_long_rail_17AG')
        hui_long_rail_18AG = self.env.ref('metro_park_base.hui_long_rail_18AG')
        hui_long_rail_19AG = self.env.ref('metro_park_base.hui_long_rail_19AG')
        hui_long_rail_20AG = self.env.ref('metro_park_base.hui_long_rail_20AG')
        hui_long_rail_21AG = self.env.ref('metro_park_base.hui_long_rail_21AG')
        hui_long_rail_22AG = self.env.ref('metro_park_base.hui_long_rail_22AG')
        hui_long_rail_23AG = self.env.ref('metro_park_base.hui_long_rail_23AG')
        hui_long_rail_24AG = self.env.ref('metro_park_base.hui_long_rail_24AG')
        hui_long_rail_16BG = self.env.ref('metro_park_base.hui_long_rail_16BG')
        hui_long_rail_17BG = self.env.ref('metro_park_base.hui_long_rail_17BG')
        hui_long_rail_18BG = self.env.ref('metro_park_base.hui_long_rail_18BG')
        hui_long_rail_19BG = self.env.ref('metro_park_base.hui_long_rail_19BG')
        hui_long_rail_20BG = self.env.ref('metro_park_base.hui_long_rail_20BG')
        hui_long_rail_21BG = self.env.ref('metro_park_base.hui_long_rail_21BG')
        hui_long_rail_22BG = self.env.ref('metro_park_base.hui_long_rail_22BG')
        hui_long_rail_23BG = self.env.ref('metro_park_base.hui_long_rail_23BG')
        hui_long_rail_24BG = self.env.ref('metro_park_base.hui_long_rail_24BG')
        hui_long_rail_L0515DGJF = self.env.ref(
            'metro_park_base.hui_long_rail_L0515DGJF')
        # 从标以仿真程序在1920 * 1280上面的位置为准
        # hui_long_switch_1

        hui_long_switch_1.positive_rail = False
        hui_long_switch_1.negative_rail = False
        hui_long_switch_1.header_rail = hui_long_rail_T6602G.id
        hui_long_switch_1.positive_switch = hui_long_switch_7.id
        hui_long_switch_1.negative_switch = hui_long_switch_3.id
        hui_long_switch_1.header_switch = False
        hui_long_switch_1.x_pos = 360
        hui_long_switch_1.y_pos = 582

        # hui_long_switch_3
        hui_long_switch_3.positive_rail = False
        hui_long_switch_3.negative_rail = False
        hui_long_switch_3.header_rail = False
        hui_long_switch_3.positive_switch = hui_long_switch_5.id
        hui_long_switch_3.negative_switch = hui_long_switch_1.id
        hui_long_switch_3.header_switch = hui_long_switch_19.id
        hui_long_switch_3.x_pos = 379
        hui_long_switch_3.y_pos = 469

        # hui_long_switch_5
        hui_long_switch_5.positive_rail = hui_long_rail_27G.id
        hui_long_switch_5.negative_rail = False
        hui_long_switch_5.header_rail = False
        hui_long_switch_5.positive_switch = False
        hui_long_switch_5.negative_switch = hui_long_switch_7.id
        hui_long_switch_5.header_switch = hui_long_switch_3.id
        hui_long_switch_5.x_pos = 482
        hui_long_switch_5.y_pos = 469

        # hui_long_switch_7
        hui_long_switch_7.positive_rail = False
        hui_long_switch_7.negative_rail = False
        hui_long_switch_7.header_rail = False
        hui_long_switch_7.positive_switch = hui_long_switch_1.id
        hui_long_switch_7.negative_switch = hui_long_switch_5.id
        hui_long_switch_7.header_switch = hui_long_switch_9.id
        hui_long_switch_7.x_pos = 506
        hui_long_switch_7.y_pos = 428

        # hui_long_switch_9
        hui_long_switch_9.positive_rail = False
        hui_long_switch_9.negative_rail = False
        hui_long_switch_9.header_rail = False
        hui_long_switch_9.positive_switch = hui_long_switch_15.id
        hui_long_switch_9.negative_switch = hui_long_switch_11.id
        hui_long_switch_9.header_switch = hui_long_switch_7.id
        hui_long_switch_9.x_pos = 451
        hui_long_switch_9.y_pos = 212

        # hui_long_switch_11
        hui_long_switch_11.positive_rail = False
        hui_long_switch_11.negative_rail = False
        hui_long_switch_11.header_rail = False
        hui_long_switch_11.positive_switch = hui_long_switch_13.id
        hui_long_switch_11.negative_switch = hui_long_switch_9.id
        hui_long_switch_11.header_switch = hui_long_switch_49.id
        hui_long_switch_11.x_pos = 491
        hui_long_switch_11.y_pos = 334

        # hui_long_switch_13
        hui_long_switch_13.positive_rail = False
        hui_long_switch_13.negative_rail = False
        hui_long_switch_13.header_rail = hui_long_rail_D9G.id
        hui_long_switch_13.positive_switch = hui_long_switch_11.id
        hui_long_switch_13.negative_switch = hui_long_switch_15.id
        hui_long_switch_13.header_switch = False
        hui_long_switch_13.x_pos = 578
        hui_long_switch_13.y_pos = 428

        # hui_long_switch_15
        hui_long_switch_15.positive_rail = False
        hui_long_switch_15.negative_rail = False
        hui_long_switch_15.header_rail = False
        hui_long_switch_15.positive_switch = hui_long_switch_9.id
        hui_long_switch_15.negative_switch = hui_long_switch_13.id
        hui_long_switch_15.header_switch = hui_long_switch_17.id
        hui_long_switch_15.x_pos = 636
        hui_long_switch_15.y_pos = 334

        # hui_long_switch_17
        hui_long_switch_17.positive_rail = False
        hui_long_switch_17.negative_rail = False
        hui_long_switch_17.header_rail = False
        hui_long_switch_17.positive_switch = hui_long_switch_27.id
        hui_long_switch_17.negative_switch = hui_long_switch_19.id
        hui_long_switch_17.header_switch = hui_long_switch_15.id
        hui_long_switch_17.x_pos = 578  # 和13对齐
        hui_long_switch_17.y_pos = 334

        # hui_long_switch_19
        hui_long_switch_19.positive_rail = hui_long_rail_3_19WG.id
        hui_long_switch_19.negative_rail = False
        hui_long_switch_19.header_rail = hui_long_rail_19_21WG.id
        hui_long_switch_19.positive_switch = False
        hui_long_switch_19.negative_switch = hui_long_switch_17.id
        hui_long_switch_19.header_switch = False
        hui_long_switch_19.x_pos = 636
        hui_long_switch_19.y_pos = 428

        # hui_long_switch_21
        hui_long_switch_21.positive_rail = hui_long_switch_23.id
        hui_long_switch_21.negative_rail = False
        hui_long_switch_21.header_rail = False
        hui_long_switch_21.positive_switch = hui_long_rail_19_21WG.id
        hui_long_switch_21.negative_switch = False
        hui_long_switch_21.header_switch = False
        hui_long_switch_21.x_pos = 790
        hui_long_switch_21.y_pos = 334

        # hui_long_switch_23
        hui_long_switch_23.positive_rail = hui_long_rail_1G.id
        hui_long_switch_23.negative_rail = False
        hui_long_switch_23.header_rail = False
        hui_long_switch_23.positive_switch = False
        hui_long_switch_23.negative_switch = hui_long_switch_25.id
        hui_long_switch_23.header_switch = hui_long_switch_21.id
        hui_long_switch_23.x_pos = 844
        hui_long_switch_23.y_pos = 212

        # hui_long_switch_25
        hui_long_switch_25.positive_rail = hui_long_rail_2G.id
        hui_long_switch_25.negative_rail = hui_long_rail_3G.id
        hui_long_switch_25.header_rail = False
        hui_long_switch_25.positive_switch = False
        hui_long_switch_25.negative_switch = False
        hui_long_switch_25.header_switch = hui_long_switch_23.id
        hui_long_switch_25.x_pos = 755
        hui_long_switch_25.y_pos = 428

        # hui_long_switch_27
        hui_long_switch_27.positive_rail = False
        hui_long_switch_27.negative_rail = False
        hui_long_switch_27.header_rail = False
        hui_long_switch_27.positive_switch = hui_long_switch_35.id
        hui_long_switch_27.negative_switch = hui_long_switch_29.id
        hui_long_switch_27.header_switch = hui_long_switch_17.id
        hui_long_switch_27.x_pos = 755
        hui_long_switch_27.y_pos = 428

        # hui_long_switch_29
        hui_long_switch_29.positive_rail = False
        hui_long_switch_29.negative_rail = False
        hui_long_switch_29.header_rail = False
        hui_long_switch_29.positive_switch = hui_long_switch_33.id
        hui_long_switch_29.negative_switch = hui_long_switch_31.id
        hui_long_switch_29.header_switch = hui_long_switch_27.id
        hui_long_switch_29.x_pos = 1009
        hui_long_switch_29.y_pos = 814

        # hui_long_switch_31
        hui_long_switch_31.positive_rail = hui_long_rail_5AG.id
        hui_long_switch_31.negative_rail = hui_long_rail_4AG.id
        hui_long_switch_31.header_rail = False
        hui_long_switch_31.positive_switch = False
        hui_long_switch_31.negative_switch = False
        hui_long_switch_31.header_switch = hui_long_switch_29.id
        hui_long_switch_31.x_pos = 1087
        hui_long_switch_31.y_pos = 938

        # hui_long_switch_33
        hui_long_switch_33.positive_rail = hui_long_rail_7AG.id
        hui_long_switch_33.negative_rail = hui_long_rail_6AG.id
        hui_long_switch_33.header_rail = False
        hui_long_switch_33.positive_switch = False
        hui_long_switch_33.negative_switch = False
        hui_long_switch_33.header_switch = hui_long_switch_29.id
        hui_long_switch_33.x_pos = 1129
        hui_long_switch_33.y_pos = 938

        # hui_long_switch_35
        hui_long_switch_35.positive_rail = False
        hui_long_switch_35.negative_rail = False
        hui_long_switch_35.header_rail = False
        hui_long_switch_35.positive_switch = hui_long_switch_43.id
        hui_long_switch_35.negative_switch = hui_long_switch_37.id
        hui_long_switch_35.header_switch = hui_long_switch_27.id
        hui_long_switch_35.x_pos = 1180
        hui_long_switch_35.y_pos = 891

        # hui_long_switch_37
        hui_long_switch_37.positive_rail = False
        hui_long_switch_37.negative_rail = False
        hui_long_switch_37.header_rail = False
        hui_long_switch_37.positive_switch = hui_long_switch_41.id
        hui_long_switch_37.negative_switch = hui_long_switch_39.id
        hui_long_switch_37.header_switch = hui_long_switch_35.id
        hui_long_switch_37.x_pos = 1121
        hui_long_switch_37.y_pos = 814

        # hui_long_switch_39
        hui_long_switch_39.positive_rail = hui_long_rail_9AG.id
        hui_long_switch_39.negative_rail = hui_long_rail_8AG.id
        hui_long_switch_39.header_rail = False
        hui_long_switch_39.positive_switch = False
        hui_long_switch_39.negative_switch = False
        hui_long_switch_39.header_switch = hui_long_switch_37.id
        hui_long_switch_39.x_pos = 1172
        hui_long_switch_39.y_pos = 774

        # hui_long_switch_41
        hui_long_switch_41.positive_rail = hui_long_rail_10AG.id
        hui_long_switch_41.negative_rail = hui_long_rail_11AG.id
        hui_long_switch_41.header_rail = False
        hui_long_switch_41.positive_switch = False
        hui_long_switch_41.negative_switch = False
        hui_long_switch_41.header_switch = hui_long_switch_37.id
        hui_long_switch_41.x_pos = 1000
        hui_long_switch_41.y_pos = 575

        # hui_long_switch_43
        hui_long_switch_43.positive_rail = False
        hui_long_switch_43.negative_rail = False
        hui_long_switch_43.header_rail = False
        hui_long_switch_43.positive_switch = hui_long_switch_47.id
        hui_long_switch_43.negative_switch = hui_long_switch_45.id
        hui_long_switch_43.header_switch = hui_long_switch_35.id
        hui_long_switch_43.x_pos = 1136
        hui_long_switch_43.y_pos = 456

        # hui_long_switch_45
        hui_long_switch_45.positive_rail = hui_long_rail_13AG.id
        hui_long_switch_45.negative_rail = hui_long_rail_12AG.id
        hui_long_switch_45.header_rail = False
        hui_long_switch_45.positive_switch = False
        hui_long_switch_45.negative_switch = False
        hui_long_switch_45.header_switch = hui_long_switch_43.id
        hui_long_switch_45.x_pos = 1064
        hui_long_switch_45.y_pos = 575

        # hui_long_switch_47
        hui_long_switch_47.positive_rail = hui_long_rail_15AG.id
        hui_long_switch_47.negative_rail = hui_long_rail_14AG.id
        hui_long_switch_47.header_rail = False
        hui_long_switch_47.positive_switch = False
        hui_long_switch_47.negative_switch = False
        hui_long_switch_47.header_switch = hui_long_switch_43.id
        hui_long_switch_47.x_pos = 1103
        hui_long_switch_47.y_pos = 575

        # hui_long_switch_49
        hui_long_switch_49.positive_rail = False
        hui_long_switch_49.negative_rail = False
        hui_long_switch_49.header_rail = False
        hui_long_switch_49.positive_switch = hui_long_switch_55.id
        hui_long_switch_49.negative_switch = hui_long_switch_51.id
        hui_long_switch_49.header_switch = hui_long_switch_11.id
        hui_long_switch_49.x_pos = 1152
        hui_long_switch_49.y_pos = 531

        # hui_long_switch_51
        hui_long_switch_51.positive_rail = False
        hui_long_switch_51.negative_rail = hui_long_rail_D23G.id
        hui_long_switch_51.header_rail = False
        hui_long_switch_51.positive_switch = hui_long_switch_53.id
        hui_long_switch_51.negative_switch = False
        hui_long_switch_51.header_switch = hui_long_switch_49.id
        hui_long_switch_51.x_pos = 1000
        hui_long_switch_51.y_pos = 334

        # hui_long_switch_53
        hui_long_switch_53.positive_rail = hui_long_rail_28G.id
        hui_long_switch_53.negative_rail = hui_long_rail_27G.id
        hui_long_switch_53.header_rail = False
        hui_long_switch_53.positive_switch = False
        hui_long_switch_53.negative_switch = False
        hui_long_switch_53.header_switch = hui_long_switch_51.id
        hui_long_switch_53.x_pos = 1126
        hui_long_switch_53.y_pos = 416

        # hui_long_switch_55
        hui_long_switch_55.positive_rail = False
        hui_long_switch_55.negative_rail = False
        hui_long_switch_55.header_rail = False
        hui_long_switch_55.positive_switch = hui_long_switch_59.id
        hui_long_switch_55.negative_switch = hui_long_switch_57.id
        hui_long_switch_55.header_switch = hui_long_switch_49.id
        hui_long_switch_55.x_pos = 1078
        hui_long_switch_55.y_pos = 334

        # hui_long_switch_57
        hui_long_switch_57.positive_rail = hui_long_rail_25G.id
        hui_long_switch_57.negative_rail = hui_long_rail_26G.id
        hui_long_switch_57.header_rail = False
        hui_long_switch_57.positive_switch = False
        hui_long_switch_57.negative_switch = False
        hui_long_switch_57.header_switch = hui_long_switch_55.id
        hui_long_switch_57.x_pos = 1121
        hui_long_switch_57.y_pos = 334

        # hui_long_switch_59
        hui_long_switch_59.positive_rail = False
        hui_long_switch_59.negative_rail = False
        hui_long_switch_59.header_rail = False
        hui_long_switch_59.positive_switch = hui_long_switch_69.id
        hui_long_switch_59.negative_switch = hui_long_switch_61.id
        hui_long_switch_59.header_switch = hui_long_switch_55.id
        hui_long_switch_59.x_pos = 1164
        hui_long_switch_59.y_pos = 292

        # hui_long_switch_61
        hui_long_switch_61.positive_rail = False
        hui_long_switch_61.negative_rail = False
        hui_long_switch_61.header_rail = False
        hui_long_switch_61.positive_switch = hui_long_switch_67.id
        hui_long_switch_61.negative_switch = hui_long_switch_63.id
        hui_long_switch_61.header_switch = hui_long_switch_59.id
        hui_long_switch_61.x_pos = 1138
        hui_long_switch_61.y_pos = 213

        # hui_long_switch_63
        hui_long_switch_63.positive_rail = hui_long_rail_22AG.id
        hui_long_switch_63.negative_rail = False
        hui_long_switch_63.header_rail = False
        hui_long_switch_63.positive_switch = False
        hui_long_switch_63.negative_switch = hui_long_switch_65.id
        hui_long_switch_63.header_switch = hui_long_switch_61.id
        hui_long_switch_63.x_pos = 189
        hui_long_switch_63.y_pos = 854

        # hui_long_switch_65
        hui_long_switch_65.positive_rail = hui_long_rail_24AG.id
        hui_long_switch_65.negative_rail = hui_long_rail_23AG.id
        hui_long_switch_65.header_rail = False
        hui_long_switch_65.positive_switch = False
        hui_long_switch_65.negative_switch = False
        hui_long_switch_65.header_switch = hui_long_switch_63.id
        hui_long_switch_65.x_pos = 242
        hui_long_switch_65.y_pos = 854

        # hui_long_switch_67
        hui_long_switch_67.positive_rail = hui_long_rail_21AG.id
        hui_long_switch_67.negative_rail = hui_long_rail_20AG.id
        hui_long_switch_67.header_rail = False
        hui_long_switch_67.positive_switch = False
        hui_long_switch_67.negative_switch = False
        hui_long_switch_67.header_switch = hui_long_switch_61.id
        hui_long_switch_67.x_pos = 361
        hui_long_switch_67.y_pos = 854

        # hui_long_switch_69
        hui_long_switch_69.positive_rail = False
        hui_long_switch_69.negative_rail = False
        hui_long_switch_69.header_rail = False
        hui_long_switch_69.positive_switch = hui_long_switch_69.id
        hui_long_switch_69.negative_switch = hui_long_switch_73.id
        hui_long_switch_69.header_switch = hui_long_switch_59.id
        hui_long_switch_69.x_pos = 386
        hui_long_switch_69.y_pos = 737

        # hui_long_switch_71
        hui_long_switch_69.positive_rail = hui_long_rail_18AG.id
        hui_long_switch_69.negative_rail = hui_long_rail_19AG.id
        hui_long_switch_69.header_rail = False
        hui_long_switch_69.positive_switch = False
        hui_long_switch_69.negative_switch = False
        hui_long_switch_69.header_switch = hui_long_switch_69.id
        hui_long_switch_69.x_pos = 403
        hui_long_switch_69.y_pos = 658

        # hui_long_switch_73
        hui_long_switch_73.positive_rail = hui_long_rail_16AG.id
        hui_long_switch_73.negative_rail = hui_long_rail_17AG.id
        hui_long_switch_73.header_rail = False
        hui_long_switch_73.positive_switch = False
        hui_long_switch_73.negative_switch = False
        hui_long_switch_73.header_switch = hui_long_switch_69.id
        hui_long_switch_73.x_pos = 412
        hui_long_switch_73.y_pos = 615

        # 区段
        # hui_long_rail_19_21WG
        hui_long_rail_19_21WG.left_rail_id = False
        hui_long_rail_19_21WG.right_rail_id = False
        hui_long_rail_19_21WG.left_switch_id = hui_long_switch_19.id
        hui_long_rail_19_21WG.right_switch_id = hui_long_switch_21.id
        hui_long_rail_19_21WG.left_switch_position = 'positive'
        hui_long_rail_19_21WG.right_switch_position = 'positive'
        hui_long_rail_19_21WG.x_pos = 455
        hui_long_rail_19_21WG.y_pos = 971

        # hui_long_rail_D9G negative
        hui_long_rail_D9G.left_rail_id = hui_long_rail_T6617G.id
        hui_long_rail_D9G.right_rail_id = False
        hui_long_rail_D9G.left_switch_id = False
        hui_long_rail_D9G.right_switch_id = hui_long_switch_13.id
        hui_long_rail_D9G.left_switch_position = False
        hui_long_rail_D9G.right_switch_position = 'positive'
        hui_long_rail_D9G.x_pos = 455
        hui_long_rail_D9G.y_pos = 971

        # hui_long_rail_D1G
        hui_long_rail_D1G.left_rail_id = False
        hui_long_rail_D1G.right_rail_id = False
        hui_long_rail_D1G.left_switch_id = False
        hui_long_rail_D1G.right_switch_id = hui_long_switch_5.id
        hui_long_rail_D1G.left_switch_position = False
        hui_long_rail_D1G.right_switch_position = 'positive'
        hui_long_rail_D1G.x_pos = 455
        hui_long_rail_D1G.y_pos = 971

        # hui_long_rail_3_19WG
        hui_long_rail_3_19WG.left_rail_id = False
        hui_long_rail_3_19WG.right_rail_id = False
        hui_long_rail_3_19WG.left_switch_id = hui_long_switch_3.id
        hui_long_rail_3_19WG.right_switch_id = hui_long_switch_19.id
        hui_long_rail_3_19WG.left_switch_position = 'positive'
        hui_long_rail_3_19WG.right_switch_position = 'positive'
        hui_long_rail_3_19WG.x_pos = 455
        hui_long_rail_3_19WG.y_pos = 971

        # hui_long_rail_D23G
        hui_long_rail_D23G.left_rail_id = False
        hui_long_rail_D23G.right_rail_id = hui_long_rail_29G.id
        hui_long_rail_D23G.left_switch_id = hui_long_switch_51.id
        hui_long_rail_D23G.right_switch_id = False
        hui_long_rail_D23G.left_switch_position = 'negative'
        hui_long_rail_D23G.right_switch_position = False
        hui_long_rail_D23G.x_pos = 455
        hui_long_rail_D23G.y_pos = 971

        # hui_long_rail_4AG
        hui_long_rail_4AG.left_rail_id = False
        hui_long_rail_4AG.right_rail_id = hui_long_rail_4BG.id
        hui_long_rail_4AG.left_switch_id = hui_long_switch_31.id
        hui_long_rail_4AG.right_switch_id = False
        hui_long_rail_4AG.left_switch_position = 'negative'
        hui_long_rail_4AG.right_switch_position = False
        hui_long_rail_4AG.x_pos = 455
        hui_long_rail_4AG.y_pos = 971

        # hui_long_rail_5AG
        hui_long_rail_5AG.left_rail_id = False
        hui_long_rail_5AG.right_rail_id = hui_long_rail_5BG.id
        hui_long_rail_5AG.left_switch_id = hui_long_switch_31.id
        hui_long_rail_5AG.right_switch_id = False
        hui_long_rail_5AG.left_switch_position = 'positive'
        hui_long_rail_5AG.right_switch_position = False
        hui_long_rail_5AG.x_pos = 455
        hui_long_rail_5AG.y_pos = 971

        # hui_long_rail_6AG
        hui_long_rail_6AG.left_rail_id = False
        hui_long_rail_6AG.right_rail_id = hui_long_rail_6BG.id
        hui_long_rail_6AG.left_switch_id = hui_long_switch_33.id
        hui_long_rail_6AG.right_switch_id = False
        hui_long_rail_6AG.left_switch_position = 'negative'
        hui_long_rail_6AG.right_switch_position = False
        hui_long_rail_6AG.x_pos = 455
        hui_long_rail_6AG.y_pos = 971

        # hui_long_rail_7AG
        hui_long_rail_7AG.left_rail_id = False
        hui_long_rail_7AG.right_rail_id = hui_long_rail_7BG.id
        hui_long_rail_7AG.left_switch_id = hui_long_switch_33.id
        hui_long_rail_7AG.right_switch_id = False
        hui_long_rail_7AG.left_switch_position = 'positive'
        hui_long_rail_7AG.right_switch_position = False
        hui_long_rail_7AG.x_pos = 455
        hui_long_rail_7AG.y_pos = 971

        # hui_long_rail_8AG
        hui_long_rail_8AG.left_rail_id = False
        hui_long_rail_8AG.right_rail_id = hui_long_rail_8BG.id
        hui_long_rail_8AG.left_switch_id = hui_long_switch_39.id
        hui_long_rail_8AG.right_switch_id = False
        hui_long_rail_8AG.left_switch_position = 'negative'
        hui_long_rail_8AG.right_switch_position = False
        hui_long_rail_8AG.x_pos = 455
        hui_long_rail_8AG.y_pos = 971

        # hui_long_rail_9AG
        hui_long_rail_9AG.left_rail_id = False
        hui_long_rail_9AG.right_rail_id = hui_long_rail_9BG.id
        hui_long_rail_9AG.left_switch_id = hui_long_switch_39.id
        hui_long_rail_9AG.right_switch_id = False
        hui_long_rail_9AG.left_switch_position = 'positive'
        hui_long_rail_9AG.right_switch_position = False
        hui_long_rail_9AG.x_pos = 455
        hui_long_rail_9AG.y_pos = 971

        # hui_long_rail_10AG
        hui_long_rail_10AG.left_rail_id = False
        hui_long_rail_10AG.right_rail_id = hui_long_rail_10BG.id
        hui_long_rail_10AG.left_switch_id = hui_long_switch_41.id
        hui_long_rail_10AG.right_switch_id = False
        hui_long_rail_10AG.left_switch_position = 'positive'
        hui_long_rail_10AG.right_switch_position = False
        hui_long_rail_10AG.x_pos = 455
        hui_long_rail_10AG.y_pos = 971

        # hui_long_rail_11AG
        hui_long_rail_11AG.left_rail_id = False
        hui_long_rail_11AG.right_rail_id = hui_long_rail_11BG.id
        hui_long_rail_11AG.left_switch_id = hui_long_switch_41.id
        hui_long_rail_11AG.right_switch_id = False
        hui_long_rail_11AG.left_switch_position = 'positive'
        hui_long_rail_11AG.right_switch_position = False
        hui_long_rail_11AG.x_pos = 455
        hui_long_rail_11AG.y_pos = 971

        # hui_long_rail_12AG
        hui_long_rail_12AG.left_rail_id = False
        hui_long_rail_12AG.right_rail_id = hui_long_rail_12BG.id
        hui_long_rail_12AG.left_switch_id = hui_long_switch_45.id
        hui_long_rail_12AG.right_switch_id = False
        hui_long_rail_12AG.left_switch_position = 'negative'
        hui_long_rail_12AG.right_switch_position = False
        hui_long_rail_12AG.x_pos = 455
        hui_long_rail_12AG.y_pos = 971

        # hui_long_rail_13AG
        hui_long_rail_13AG.left_rail_id = False
        hui_long_rail_13AG.right_rail_id = hui_long_rail_13BG.id
        hui_long_rail_13AG.left_switch_id = hui_long_switch_45.id
        hui_long_rail_13AG.right_switch_id = False
        hui_long_rail_13AG.left_switch_position = 'positive'
        hui_long_rail_13AG.right_switch_position = False
        hui_long_rail_13AG.x_pos = 455
        hui_long_rail_13AG.y_pos = 971

        # hui_long_rail_14AG
        hui_long_rail_14AG.left_rail_id = False
        hui_long_rail_14AG.right_rail_id = hui_long_rail_14BG.id
        hui_long_rail_14AG.left_switch_id = hui_long_switch_47.id
        hui_long_rail_14AG.right_switch_id = False
        hui_long_rail_14AG.left_switch_position = 'negative'
        hui_long_rail_14AG.right_switch_position = False
        hui_long_rail_14AG.x_pos = 455
        hui_long_rail_14AG.y_pos = 971

        # hui_long_rail_15AG
        hui_long_rail_15AG.left_rail_id = False
        hui_long_rail_15AG.right_rail_id = hui_long_rail_15BG.id
        hui_long_rail_15AG.left_switch_id = hui_long_switch_47.id
        hui_long_rail_15AG.right_switch_id = False
        hui_long_rail_15AG.left_switch_position = 'positive'
        hui_long_rail_15AG.right_switch_position = False
        hui_long_rail_15AG.x_pos = 455
        hui_long_rail_15AG.y_pos = 971

        # hui_long_rail_16AG
        hui_long_rail_16AG.left_rail_id = False
        hui_long_rail_16AG.right_rail_id = hui_long_rail_16BG.id
        hui_long_rail_16AG.left_switch_id = hui_long_switch_73.id
        hui_long_rail_16AG.right_switch_id = False
        hui_long_rail_16AG.left_switch_position = 'positive'
        hui_long_rail_16AG.right_switch_position = False
        hui_long_rail_16AG.x_pos = 455
        hui_long_rail_16AG.y_pos = 971

        # hui_long_rail_17AG
        hui_long_rail_17AG.left_rail_id = False
        hui_long_rail_17AG.right_rail_id = hui_long_rail_17BG.id
        hui_long_rail_17AG.left_switch_id = hui_long_switch_73.id
        hui_long_rail_17AG.right_switch_id = False
        hui_long_rail_17AG.left_switch_position = 'negative'
        hui_long_rail_17AG.right_switch_position = False
        hui_long_rail_17AG.x_pos = 455
        hui_long_rail_17AG.y_pos = 971

        # hui_long_rail_18AG
        hui_long_rail_18AG.left_rail_id = False
        hui_long_rail_18AG.right_rail_id = hui_long_rail_18BG.id
        hui_long_rail_18AG.left_switch_id = hui_long_switch_71.id
        hui_long_rail_18AG.right_switch_id = False
        hui_long_rail_18AG.left_switch_position = 'positive'
        hui_long_rail_18AG.right_switch_position = False
        hui_long_rail_18AG.x_pos = 455
        hui_long_rail_18AG.y_pos = 971

        # hui_long_rail_19AG
        hui_long_rail_19AG.left_rail_id = False
        hui_long_rail_19AG.right_rail_id = hui_long_rail_19BG.id
        hui_long_rail_19AG.left_switch_id = hui_long_switch_71.id
        hui_long_rail_19AG.right_switch_id = False
        hui_long_rail_19AG.left_switch_position = 'negative'
        hui_long_rail_19AG.right_switch_position = False
        hui_long_rail_19AG.x_pos = 455
        hui_long_rail_19AG.y_pos = 971

        # hui_long_rail_20AG
        hui_long_rail_20AG.left_rail_id = False
        hui_long_rail_20AG.right_rail_id = hui_long_rail_20BG.id
        hui_long_rail_20AG.left_switch_id = hui_long_switch_67.id
        hui_long_rail_20AG.right_switch_id = False
        hui_long_rail_20AG.left_switch_position = 'negative'
        hui_long_rail_20AG.right_switch_position = False
        hui_long_rail_20AG.x_pos = 455
        hui_long_rail_20AG.y_pos = 971

        # hui_long_rail_21AG
        hui_long_rail_21AG.left_rail_id = False
        hui_long_rail_21AG.right_rail_id = hui_long_rail_21BG.id
        hui_long_rail_21AG.left_switch_id = hui_long_switch_67.id
        hui_long_rail_21AG.right_switch_id = False
        hui_long_rail_21AG.left_switch_position = 'positive'
        hui_long_rail_21AG.right_switch_position = False
        hui_long_rail_21AG.x_pos = 455
        hui_long_rail_21AG.y_pos = 971

        # hui_long_rail_22AG
        hui_long_rail_22AG.left_rail_id = False
        hui_long_rail_22AG.right_rail_id = hui_long_rail_22BG.id
        hui_long_rail_22AG.left_switch_id = hui_long_switch_63.id
        hui_long_rail_22AG.right_switch_id = False
        hui_long_rail_22AG.left_switch_position = 'positive'
        hui_long_rail_22AG.right_switch_position = False
        hui_long_rail_22AG.x_pos = 455
        hui_long_rail_22AG.y_pos = 971

        # hui_long_rail_23AG
        hui_long_rail_23AG.left_rail_id = False
        hui_long_rail_23AG.right_rail_id = hui_long_rail_23BG.id
        hui_long_rail_23AG.left_switch_id = hui_long_switch_65.id
        hui_long_rail_23AG.right_switch_id = False
        hui_long_rail_23AG.left_switch_position = 'negative'
        hui_long_rail_23AG.right_switch_position = False
        hui_long_rail_23AG.x_pos = 455
        hui_long_rail_23AG.y_pos = 971

        # hui_long_rail_24AG
        hui_long_rail_24AG.left_rail_id = False
        hui_long_rail_24AG.right_rail_id = hui_long_rail_23BG.id
        hui_long_rail_24AG.left_switch_id = hui_long_switch_65.id
        hui_long_rail_24AG.right_switch_id = False
        hui_long_rail_24AG.left_switch_position = 'positive'
        hui_long_rail_24AG.right_switch_position = False
        hui_long_rail_24AG.x_pos = 455
        hui_long_rail_24AG.y_pos = 971

        # hui_long_rail_4BG
        hui_long_rail_4BG.left_rail_id = hui_long_rail_4AG.id
        hui_long_rail_4BG.right_rail_id = False
        hui_long_rail_4BG.left_switch_id = False
        hui_long_rail_4BG.right_switch_id = False
        hui_long_rail_4BG.left_switch_position = False
        hui_long_rail_4BG.right_switch_position = False
        hui_long_rail_4BG.x_pos = 455
        hui_long_rail_4BG.y_pos = 971

        # hui_long_rail_5BG
        hui_long_rail_5BG.left_rail_id = hui_long_rail_5AG.id
        hui_long_rail_5BG.right_rail_id = False
        hui_long_rail_5BG.left_switch_id = False
        hui_long_rail_5BG.right_switch_id = False
        hui_long_rail_5BG.left_switch_position = False
        hui_long_rail_5BG.right_switch_position = False
        hui_long_rail_5BG.x_pos = 455
        hui_long_rail_5BG.y_pos = 971

        # hui_long_rail_6BG
        hui_long_rail_6BG.left_rail_id = hui_long_rail_6AG.id
        hui_long_rail_6BG.right_rail_id = False
        hui_long_rail_6BG.left_switch_id = False
        hui_long_rail_6BG.right_switch_id = False
        hui_long_rail_6BG.left_switch_position = False
        hui_long_rail_6BG.right_switch_position = False
        hui_long_rail_6BG.x_pos = 455
        hui_long_rail_6BG.y_pos = 971

        # hui_long_rail_7BG
        hui_long_rail_7BG.left_rail_id = hui_long_rail_7AG.id
        hui_long_rail_7BG.right_rail_id = False
        hui_long_rail_7BG.left_switch_id = False
        hui_long_rail_7BG.right_switch_id = False
        hui_long_rail_7BG.left_switch_position = False
        hui_long_rail_7BG.right_switch_position = False
        hui_long_rail_7BG.x_pos = 455
        hui_long_rail_7BG.y_pos = 971

        # hui_long_rail_8BG
        hui_long_rail_8BG.left_rail_id = hui_long_rail_8AG.id
        hui_long_rail_8BG.right_rail_id = False
        hui_long_rail_8BG.left_switch_id = False
        hui_long_rail_8BG.right_switch_id = False
        hui_long_rail_8BG.left_switch_position = False
        hui_long_rail_8BG.right_switch_position = False
        hui_long_rail_8BG.x_pos = 455
        hui_long_rail_8BG.y_pos = 971

        # hui_long_rail_9BG
        hui_long_rail_9BG.left_rail_id = hui_long_rail_9AG.id
        hui_long_rail_9BG.right_rail_id = False
        hui_long_rail_9BG.left_switch_id = False
        hui_long_rail_9BG.right_switch_id = False
        hui_long_rail_9BG.left_switch_position = False
        hui_long_rail_9BG.right_switch_position = False
        hui_long_rail_9BG.x_pos = 455
        hui_long_rail_9BG.y_pos = 971

        # hui_long_rail_10BG
        hui_long_rail_10BG.left_rail_id = hui_long_rail_10AG.id
        hui_long_rail_10BG.right_rail_id = False
        hui_long_rail_10BG.left_switch_id = False
        hui_long_rail_10BG.right_switch_id = False
        hui_long_rail_10BG.left_switch_position = False
        hui_long_rail_10BG.right_switch_position = False
        hui_long_rail_10BG.x_pos = 455
        hui_long_rail_10BG.y_pos = 971

        # hui_long_rail_11BG
        hui_long_rail_11BG.left_rail_id = hui_long_rail_11AG.id
        hui_long_rail_11BG.right_rail_id = False
        hui_long_rail_11BG.left_switch_id = False
        hui_long_rail_11BG.right_switch_id = False
        hui_long_rail_11BG.left_switch_position = False
        hui_long_rail_11BG.right_switch_position = False
        hui_long_rail_11BG.x_pos = 455
        hui_long_rail_11BG.y_pos = 971

        # hui_long_rail_12BG
        hui_long_rail_12BG.left_rail_id = hui_long_rail_12AG.id
        hui_long_rail_12BG.right_rail_id = False
        hui_long_rail_12BG.left_switch_id = False
        hui_long_rail_12BG.right_switch_id = False
        hui_long_rail_12BG.left_switch_position = False
        hui_long_rail_12BG.right_switch_position = False
        hui_long_rail_12BG.x_pos = 455
        hui_long_rail_12BG.y_pos = 971

        # hui_long_rail_13BG
        hui_long_rail_13BG.left_rail_id = hui_long_rail_13AG.id
        hui_long_rail_13BG.right_rail_id = False
        hui_long_rail_13BG.left_switch_id = False
        hui_long_rail_13BG.right_switch_id = False
        hui_long_rail_13BG.left_switch_position = False
        hui_long_rail_13BG.right_switch_position = False
        hui_long_rail_13BG.x_pos = 455
        hui_long_rail_13BG.y_pos = 971

        # hui_long_rail_14BG
        hui_long_rail_14BG.left_rail_id = hui_long_rail_14AG.id
        hui_long_rail_14BG.right_rail_id = False
        hui_long_rail_14BG.left_switch_id = False
        hui_long_rail_14BG.right_switch_id = False
        hui_long_rail_14BG.left_switch_position = False
        hui_long_rail_14BG.right_switch_position = False
        hui_long_rail_14BG.x_pos = 455
        hui_long_rail_14BG.y_pos = 971

        # hui_long_rail_15BG
        hui_long_rail_15BG.left_rail_id = hui_long_rail_15AG.id
        hui_long_rail_15BG.right_rail_id = False
        hui_long_rail_15BG.left_switch_id = False
        hui_long_rail_15BG.right_switch_id = False
        hui_long_rail_15BG.left_switch_position = False
        hui_long_rail_15BG.right_switch_position = False
        hui_long_rail_15BG.x_pos = 455
        hui_long_rail_15BG.y_pos = 971

        # hui_long_rail_16BG
        hui_long_rail_16BG.left_rail_id = hui_long_rail_16AG.id
        hui_long_rail_16BG.right_rail_id = False
        hui_long_rail_16BG.left_switch_id = False
        hui_long_rail_16BG.right_switch_id = False
        hui_long_rail_16BG.left_switch_position = False
        hui_long_rail_16BG.right_switch_position = False
        hui_long_rail_16BG.x_pos = 455
        hui_long_rail_16BG.y_pos = 971

        # hui_long_rail_17BG
        hui_long_rail_17BG.left_rail_id = hui_long_rail_17AG.id
        hui_long_rail_17BG.right_rail_id = False
        hui_long_rail_17BG.left_switch_id = False
        hui_long_rail_17BG.right_switch_id = False
        hui_long_rail_17BG.left_switch_position = False
        hui_long_rail_17BG.right_switch_position = False
        hui_long_rail_17BG.x_pos = 455
        hui_long_rail_17BG.y_pos = 971

        # hui_long_rail_18BG
        hui_long_rail_18BG.left_rail_id = hui_long_rail_18AG.id
        hui_long_rail_18BG.right_rail_id = False
        hui_long_rail_18BG.left_switch_id = False
        hui_long_rail_18BG.right_switch_id = False
        hui_long_rail_18BG.left_switch_position = False
        hui_long_rail_18BG.right_switch_position = False
        hui_long_rail_18BG.x_pos = 455
        hui_long_rail_18BG.y_pos = 971

        # hui_long_rail_19BG
        hui_long_rail_19BG.left_rail_id = hui_long_rail_19AG.id
        hui_long_rail_19BG.right_rail_id = False
        hui_long_rail_19BG.left_switch_id = False
        hui_long_rail_19BG.right_switch_id = False
        hui_long_rail_19BG.left_switch_position = False
        hui_long_rail_19BG.right_switch_position = False
        hui_long_rail_19BG.x_pos = 455
        hui_long_rail_19BG.y_pos = 971

        # hui_long_rail_20BG
        hui_long_rail_20BG.left_rail_id = hui_long_rail_20AG.id
        hui_long_rail_20BG.right_rail_id = False
        hui_long_rail_20BG.left_switch_id = False
        hui_long_rail_20BG.right_switch_id = False
        hui_long_rail_20BG.left_switch_position = False
        hui_long_rail_20BG.right_switch_position = False
        hui_long_rail_20BG.x_pos = 455
        hui_long_rail_20BG.y_pos = 971

        # hui_long_rail_21BG
        hui_long_rail_21BG.left_rail_id = hui_long_rail_21AG.id
        hui_long_rail_21BG.right_rail_id = False
        hui_long_rail_21BG.left_switch_id = False
        hui_long_rail_21BG.right_switch_id = False
        hui_long_rail_21BG.left_switch_position = False
        hui_long_rail_21BG.right_switch_position = False
        hui_long_rail_21BG.x_pos = 455
        hui_long_rail_21BG.y_pos = 971

        # hui_long_rail_22BG
        hui_long_rail_22BG.left_rail_id = hui_long_rail_22AG.id
        hui_long_rail_22BG.right_rail_id = False
        hui_long_rail_22BG.left_switch_id = False
        hui_long_rail_22BG.right_switch_id = False
        hui_long_rail_22BG.left_switch_position = False
        hui_long_rail_22BG.right_switch_position = False
        hui_long_rail_22BG.x_pos = 455
        hui_long_rail_22BG.y_pos = 971

        # hui_long_rail_23BG
        hui_long_rail_23BG.left_rail_id = hui_long_rail_23AG.id
        hui_long_rail_23BG.right_rail_id = False
        hui_long_rail_23BG.left_switch_id = False
        hui_long_rail_23BG.right_switch_id = False
        hui_long_rail_23BG.left_switch_position = False
        hui_long_rail_23BG.right_switch_position = False
        hui_long_rail_23BG.x_pos = 455
        hui_long_rail_23BG.y_pos = 971

        # hui_long_rail_24BG
        hui_long_rail_24BG.left_rail_id = hui_long_rail_24AG.id
        hui_long_rail_24BG.right_rail_id = False
        hui_long_rail_24BG.left_switch_id = False
        hui_long_rail_24BG.right_switch_id = False
        hui_long_rail_24BG.left_switch_position = False
        hui_long_rail_24BG.right_switch_position = False
        hui_long_rail_24BG.x_pos = 455
        hui_long_rail_24BG.y_pos = 971

        # hui_long_rail_T6602G
        hui_long_rail_T6602G.left_rail_id = hui_long_rail_T6604G.id
        hui_long_rail_T6602G.right_rail_id = False
        hui_long_rail_T6602G.left_switch_id = False
        hui_long_rail_T6602G.right_switch_id = hui_long_switch_1.id
        hui_long_rail_T6602G.left_switch_position = False
        hui_long_rail_T6602G.right_switch_position = 'positive'
        hui_long_rail_T6602G.x_pos = 455
        hui_long_rail_T6602G.y_pos = 971

        # hui_long_rail_T6617G
        hui_long_rail_T6617G.left_rail_id = hui_long_rail_T6615G.id
        hui_long_rail_T6617G.right_rail_id = hui_long_rail_D9G.id
        hui_long_rail_T6617G.left_switch_id = False
        hui_long_rail_T6617G.right_switch_id = False
        hui_long_rail_T6617G.left_switch_position = False
        hui_long_rail_T6617G.right_switch_position = False
        hui_long_rail_T6617G.x_pos = 455
        hui_long_rail_T6617G.y_pos = 971

        # hui_long_rail_29G
        hui_long_rail_29G.left_rail_id = False
        hui_long_rail_29G.right_rail_id = hui_long_rail_D23G.id
        hui_long_rail_29G.left_switch_id = False
        hui_long_rail_29G.right_switch_id = False
        hui_long_rail_29G.left_switch_position = False
        hui_long_rail_29G.right_switch_position = False
        hui_long_rail_29G.x_pos = 455
        hui_long_rail_29G.y_pos = 971

        # hui_long_rail_L0515DGJF
        hui_long_rail_L0515DGJF.left_rail_id = False
        hui_long_rail_L0515DGJF.right_rail_id = False
        hui_long_rail_L0515DGJF.left_switch_id = hui_long_switch_21
        hui_long_rail_L0515DGJF.right_switch_id = False
        hui_long_rail_L0515DGJF.left_switch_position = 'negative'
        hui_long_rail_L0515DGJF.right_switch_position = False
        hui_long_rail_L0515DGJF.x_pos = 455
        hui_long_rail_L0515DGJF.y_pos = 971

        # hui_long_rail_T6604G
        hui_long_rail_T6604G.left_rail_id = False
        hui_long_rail_T6604G.right_rail_id = hui_long_rail_T6602G.id
        hui_long_rail_T6604G.left_switch_id = False
        hui_long_rail_T6604G.right_switch_id = False
        hui_long_rail_T6604G.left_switch_position = False
        hui_long_rail_T6604G.right_switch_position = False
        hui_long_rail_T6604G.x_pos = 455
        hui_long_rail_T6604G.y_pos = 971

        # hui_long_rail_T6615G
        hui_long_rail_T6615G.left_rail_id = False
        hui_long_rail_T6615G.right_rail_id = hui_long_rail_T6617G.id
        hui_long_rail_T6615G.left_switch_id = False
        hui_long_rail_T6615G.right_switch_id = False
        hui_long_rail_T6615G.left_switch_position = False
        hui_long_rail_T6615G.right_switch_position = False
        hui_long_rail_T6615G.x_pos = 455
        hui_long_rail_T6615G.y_pos = 971

        # hui_long_rail_25G
        hui_long_rail_25G.left_rail_id = False
        hui_long_rail_25G.right_rail_id = False
        hui_long_rail_25G.left_switch_id = hui_long_switch_57.id
        hui_long_rail_25G.right_switch_id = False
        hui_long_rail_25G.left_switch_position = 'positive'
        hui_long_rail_25G.right_switch_position = False
        hui_long_rail_25G.x_pos = 455
        hui_long_rail_25G.y_pos = 971

        # hui_long_rail_26G
        hui_long_rail_26G.left_rail_id = False
        hui_long_rail_26G.right_rail_id = False
        hui_long_rail_26G.left_switch_id = hui_long_switch_57.id
        hui_long_rail_26G.right_switch_id = False
        hui_long_rail_26G.left_switch_position = 'negative'
        hui_long_rail_26G.right_switch_position = False
        hui_long_rail_26G.x_pos = 455
        hui_long_rail_26G.y_pos = 971

        # hui_long_rail_27G
        hui_long_rail_27G.left_rail_id = False
        hui_long_rail_27G.right_rail_id = False
        hui_long_rail_27G.left_switch_id = hui_long_switch_53.id
        hui_long_rail_27G.right_switch_id = False
        hui_long_rail_27G.left_switch_position = 'negative'
        hui_long_rail_27G.right_switch_position = False
        hui_long_rail_27G.x_pos = 455
        hui_long_rail_27G.y_pos = 971

        # hui_long_rail_28G
        hui_long_rail_28G.left_rail_id = False
        hui_long_rail_28G.right_rail_id = False
        hui_long_rail_28G.left_switch_id = hui_long_switch_53.id
        hui_long_rail_28G.right_switch_id = False
        hui_long_rail_28G.left_switch_position = 'positive'
        hui_long_rail_28G.right_switch_position = False
        hui_long_rail_28G.x_pos = 455
        hui_long_rail_28G.y_pos = 971

        # hui_long_rail_1G
        hui_long_rail_1G.left_rail_id = False
        hui_long_rail_1G.right_rail_id = False
        hui_long_rail_1G.left_switch_id = hui_long_switch_23.id
        hui_long_rail_1G.right_switch_id = False
        hui_long_rail_1G.left_switch_position = 'positive'
        hui_long_rail_1G.right_switch_position = False
        hui_long_rail_1G.x_pos = 455
        hui_long_rail_1G.y_pos = 971

        # hui_long_rail_2G
        hui_long_rail_2G.left_rail_id = False
        hui_long_rail_2G.right_rail_id = False
        hui_long_rail_2G.left_switch_id = hui_long_switch_25.id
        hui_long_rail_2G.right_switch_id = False
        hui_long_rail_2G.left_switch_position = 'positive'
        hui_long_rail_2G.right_switch_position = False
        hui_long_rail_2G.x_pos = 455
        hui_long_rail_2G.y_pos = 971

        # hui_long_rail_3G
        hui_long_rail_3G.left_rail_id = False
        hui_long_rail_3G.right_rail_id = False
        hui_long_rail_3G.left_switch_id = hui_long_switch_25.id
        hui_long_rail_3G.right_switch_id = False
        hui_long_rail_3G.left_switch_position = 'negative'
        hui_long_rail_3G.right_switch_position = False
        hui_long_rail_3G.x_pos = 455
        hui_long_rail_3G.y_pos = 971

        pi_tong_switch_2 = self.env.ref('metro_park_base.pi_tong_switch_2')
        pi_tong_switch_4 = self.env.ref('metro_park_base.pi_tong_switch_4')
        pi_tong_switch_6 = self.env.ref('metro_park_base.pi_tong_switch_6')
        pi_tong_switch_8 = self.env.ref('metro_park_base.pi_tong_switch_8')
        pi_tong_switch_10 = self.env.ref('metro_park_base.pi_tong_switch_10')
        pi_tong_switch_12 = self.env.ref('metro_park_base.pi_tong_switch_12')
        pi_tong_switch_14 = self.env.ref('metro_park_base.pi_tong_switch_14')
        pi_tong_switch_16 = self.env.ref('metro_park_base.pi_tong_switch_16')
        pi_tong_switch_18 = self.env.ref('metro_park_base.pi_tong_switch_18')
        pi_tong_switch_20 = self.env.ref('metro_park_base.pi_tong_switch_20')
        pi_tong_switch_22 = self.env.ref('metro_park_base.pi_tong_switch_22')
        pi_tong_switch_24 = self.env.ref('metro_park_base.pi_tong_switch_24')
        pi_tong_switch_26 = self.env.ref('metro_park_base.pi_tong_switch_26')
        pi_tong_switch_28 = self.env.ref('metro_park_base.pi_tong_switch_28')
        pi_tong_switch_30 = self.env.ref('metro_park_base.pi_tong_switch_30')
        pi_tong_switch_32 = self.env.ref('metro_park_base.pi_tong_switch_32')
        pi_tong_switch_34 = self.env.ref('metro_park_base.pi_tong_switch_34')
        pi_tong_switch_36 = self.env.ref('metro_park_base.pi_tong_switch_36')
        pi_tong_switch_38 = self.env.ref('metro_park_base.pi_tong_switch_38')
        pi_tong_switch_40 = self.env.ref('metro_park_base.pi_tong_switch_40')
        pi_tong_switch_42 = self.env.ref('metro_park_base.pi_tong_switch_42')
        pi_tong_switch_44 = self.env.ref('metro_park_base.pi_tong_switch_44')
        pi_tong_switch_46 = self.env.ref('metro_park_base.pi_tong_switch_46')
        pi_tong_switch_48 = self.env.ref('metro_park_base.pi_tong_switch_48')
        pi_tong_switch_50 = self.env.ref('metro_park_base.pi_tong_switch_50')
        pi_tong_switch_52 = self.env.ref('metro_park_base.pi_tong_switch_52')
        pi_tong_switch_54 = self.env.ref('metro_park_base.pi_tong_switch_54')
        pi_tong_switch_56 = self.env.ref('metro_park_base.pi_tong_switch_56')
        pi_tong_switch_58 = self.env.ref('metro_park_base.pi_tong_switch_58')
        pi_tong_switch_60 = self.env.ref('metro_park_base.pi_tong_switch_60')
        pi_tong_switch_62 = self.env.ref('metro_park_base.pi_tong_switch_62')
        pi_tong_switch_64 = self.env.ref('metro_park_base.pi_tong_switch_64')
        pi_tong_switch_66 = self.env.ref('metro_park_base.pi_tong_switch_66')
        pi_tong_switch_68 = self.env.ref('metro_park_base.pi_tong_switch_68')
        pi_tong_switch_70 = self.env.ref('metro_park_base.pi_tong_switch_70')
        pi_tong_switch_72 = self.env.ref('metro_park_base.pi_tong_switch_72')
        pi_tong_switch_74 = self.env.ref('metro_park_base.pi_tong_switch_74')
        pi_tong_switch_76 = self.env.ref('metro_park_base.pi_tong_switch_76')
        pi_tong_switch_78 = self.env.ref('metro_park_base.pi_tong_switch_78')
        pi_tong_switch_80 = self.env.ref('metro_park_base.pi_tong_switch_80')
        pi_tong_switch_82 = self.env.ref('metro_park_base.pi_tong_switch_82')
        pi_tong_switch_84 = self.env.ref('metro_park_base.pi_tong_switch_84')
        pi_tong_switch_86 = self.env.ref('metro_park_base.pi_tong_switch_86')
        pi_tong_switch_88 = self.env.ref('metro_park_base.pi_tong_switch_88')
        pi_tong_switch_90 = self.env.ref('metro_park_base.pi_tong_switch_90')
        pi_tong_switch_92 = self.env.ref('metro_park_base.pi_tong_switch_92')
        pi_tong_switch_94 = self.env.ref('metro_park_base.pi_tong_switch_94')
        pi_tong_switch_96 = self.env.ref('metro_park_base.pi_tong_switch_96')
        pi_tong_switch_98 = self.env.ref('metro_park_base.pi_tong_switch_98')
        pi_tong_switch_100 = self.env.ref('metro_park_base.pi_tong_switch_100')
        pi_tong_switch_102 = self.env.ref('metro_park_base.pi_tong_switch_102')
        pi_tong_switch_104 = self.env.ref('metro_park_base.pi_tong_switch_104')
        pi_tong_switch_106 = self.env.ref('metro_park_base.pi_tong_switch_106')
        pi_tong_switch_108 = self.env.ref('metro_park_base.pi_tong_switch_108')
        pi_tong_switch_110 = self.env.ref('metro_park_base.pi_tong_switch_110')
        pi_tong_switch_112 = self.env.ref('metro_park_base.pi_tong_switch_112')
        pi_tong_switch_114 = self.env.ref('metro_park_base.pi_tong_switch_114')
        pi_tong_switch_116 = self.env.ref('metro_park_base.pi_tong_switch_116')
        pi_tong_switch_118 = self.env.ref('metro_park_base.pi_tong_switch_118')
        pi_tong_switch_120 = self.env.ref('metro_park_base.pi_tong_switch_120')
        pi_tong_switch_122 = self.env.ref('metro_park_base.pi_tong_switch_122')
        pi_tong_switch_124 = self.env.ref('metro_park_base.pi_tong_switch_124')
        pi_tong_switch_126 = self.env.ref('metro_park_base.pi_tong_switch_126')
        pi_tong_switch_128 = self.env.ref('metro_park_base.pi_tong_switch_128')
        pi_tong_switch_130 = self.env.ref('metro_park_base.pi_tong_switch_130')

        # 所有的区段
        pi_tong_1G = self.env.ref('metro_park_base.pi_tong_1G')
        pi_tong_2G = self.env.ref('metro_park_base.pi_tong_2G')
        pi_tong_3G = self.env.ref('metro_park_base.pi_tong_3G')
        pi_tong_4G = self.env.ref('metro_park_base.pi_tong_4G')
        pi_tong_5G = self.env.ref('metro_park_base.pi_tong_5G')
        pi_tong_6G = self.env.ref('metro_park_base.pi_tong_6G')
        pi_tong_7G = self.env.ref('metro_park_base.pi_tong_7G')
        pi_tong_8G = self.env.ref('metro_park_base.pi_tong_8G')
        pi_tong_9G = self.env.ref('metro_park_base.pi_tong_9G')
        pi_tong_10G = self.env.ref('metro_park_base.pi_tong_10G')
        pi_tong_11G = self.env.ref('metro_park_base.pi_tong_11G')
        pi_tong_12G = self.env.ref('metro_park_base.pi_tong_12G')
        pi_tong_13G = self.env.ref('metro_park_base.pi_tong_13G')
        pi_tong_14G = self.env.ref('metro_park_base.pi_tong_14G')
        pi_tong_15G = self.env.ref('metro_park_base.pi_tong_15G')
        pi_tong_16G = self.env.ref('metro_park_base.pi_tong_16G')
        pi_tong_17G = self.env.ref('metro_park_base.pi_tong_17G')
        pi_tong_18G = self.env.ref('metro_park_base.pi_tong_18G')
        pi_tong_19G = self.env.ref('metro_park_base.pi_tong_19G')
        pi_tong_20G = self.env.ref('metro_park_base.pi_tong_20G')
        pi_tong_21G = self.env.ref('metro_park_base.pi_tong_21G')
        pi_tong_22G = self.env.ref('metro_park_base.pi_tong_22G')
        pi_tong_23G = self.env.ref('metro_park_base.pi_tong_23G')
        pi_tong_24G = self.env.ref('metro_park_base.pi_tong_24G')
        pi_tong_25G = self.env.ref('metro_park_base.pi_tong_25G')
        pi_tong_26G = self.env.ref('metro_park_base.pi_tong_26G')
        pi_tong_27G = self.env.ref('metro_park_base.pi_tong_27G')
        pi_tong_28G = self.env.ref('metro_park_base.pi_tong_28G')
        pi_tong_29G = self.env.ref('metro_park_base.pi_tong_29G')
        pi_tong_30G = self.env.ref('metro_park_base.pi_tong_30G')
        pi_tong_31G = self.env.ref('metro_park_base.pi_tong_31G')
        pi_tong_32G = self.env.ref('metro_park_base.pi_tong_32G')
        pi_tong_33G = self.env.ref('metro_park_base.pi_tong_33G')
        pi_tong_34G = self.env.ref('metro_park_base.pi_tong_34G')
        pi_tong_35G = self.env.ref('metro_park_base.pi_tong_35G')
        pi_tong_36G = self.env.ref('metro_park_base.pi_tong_36G')
        pi_tong_37G = self.env.ref('metro_park_base.pi_tong_37G')
        pi_tong_38G = self.env.ref('metro_park_base.pi_tong_38G')
        pi_tong_39G = self.env.ref('metro_park_base.pi_tong_39G')
        pi_tong_40G = self.env.ref('metro_park_base.pi_tong_40G')
        pi_tong_41G = self.env.ref('metro_park_base.pi_tong_41G')
        pi_tong_42G = self.env.ref('metro_park_base.pi_tong_42G')
        pi_tong_43G = self.env.ref('metro_park_base.pi_tong_43G')
        pi_tong_44G = self.env.ref('metro_park_base.pi_tong_44G')
        pi_tong_45G = self.env.ref('metro_park_base.pi_tong_45G')
        pi_tong_46G = self.env.ref('metro_park_base.pi_tong_46G')
        pi_tong_47G = self.env.ref('metro_park_base.pi_tong_47G')
        pi_tong_48G = self.env.ref('metro_park_base.pi_tong_48G')
        pi_tong_49G = self.env.ref('metro_park_base.pi_tong_49G')
        pi_tong_50G = self.env.ref('metro_park_base.pi_tong_50G')
        pi_tong_51G = self.env.ref('metro_park_base.pi_tong_51G')
        pi_tong_52G = self.env.ref('metro_park_base.pi_tong_52G')
        pi_tong_53G = self.env.ref('metro_park_base.pi_tong_53G')
        pi_tong_54G = self.env.ref('metro_park_base.pi_tong_54G')
        pi_tong_55G = self.env.ref('metro_park_base.pi_tong_55G')
        pi_tong_56G = self.env.ref('metro_park_base.pi_tong_56G')
        pi_tong_57G = self.env.ref('metro_park_base.pi_tong_57G')
        pi_tong_58G = self.env.ref('metro_park_base.pi_tong_58G')
        pi_tong_61G = self.env.ref('metro_park_base.pi_tong_61G')

        pi_tong_D2G = self.env.ref('metro_park_base.pi_tong_D2G')
        pi_tong_D4G = self.env.ref('metro_park_base.pi_tong_D4G')
        pi_tong_D22G = self.env.ref('metro_park_base.pi_tong_D22G')
        pi_tong_D30G = self.env.ref('metro_park_base.pi_tong_D30G')

        pi_tong_16_D50WG = self.env.ref('metro_park_base.pi_tong_16/D50WG')
        pi_tong_100_102WG = self.env.ref('metro_park_base.pi_tong_100/102WG')
        pi_tong_100_106WG = self.env.ref('metro_park_base.pi_tong_100/106WG')
        pi_tong_114_116WG = self.env.ref('metro_park_base.pi_tong_114/116WG')
        pi_tong_114_D36WG = self.env.ref('metro_park_base.pi_tong_114/D36WG')
        pi_tong_124_D34WG = self.env.ref('metro_park_base.pi_tong_124/D34WG')
        pi_tong_126_128WG = self.env.ref('metro_park_base.pi_tong_126/128WG')

        pi_tong_T1126G = self.env.ref('metro_park_base.pi_tong_T1126G')
        pi_tong_T1124G = self.env.ref('metro_park_base.pi_tong_T1124G')
        pi_tong_T1101G = self.env.ref('metro_park_base.pi_tong_T1101G')
        pi_tong_T1103G = self.env.ref('metro_park_base.pi_tong_T1103G')

        pi_tong_2_126DG = self.env.ref('metro_park_base.pi_tong_2-126DG')
        pi_tong_4DG = self.env.ref('metro_park_base.pi_tong_4DG')
        pi_tong_6DG = self.env.ref('metro_park_base.pi_tong_6DG')
        pi_tong_8_14DG = self.env.ref('metro_park_base.pi_tong_8-14DG')
        pi_tong_10_12DG = self.env.ref('metro_park_base.pi_tong_10-12DG')
        pi_tong_16DG = self.env.ref('metro_park_base.pi_tong_16DG')
        pi_tong_18_48DG = self.env.ref('metro_park_base.pi_tong_18-48DG')
        pi_tong_22DG = self.env.ref('metro_park_base.pi_tong_22DG')
        pi_tong_24_26DG = self.env.ref('metro_park_base.pi_tong_24-26DG')
        pi_tong_28_30DG = self.env.ref('metro_park_base.pi_tong_28-30DG')
        pi_tong_32_34DG = self.env.ref('metro_park_base.pi_tong_32-34DG')
        pi_tong_38_42DG = self.env.ref('metro_park_base.pi_tong_38-42DG')
        pi_tong_44_46DG = self.env.ref('metro_park_base.pi_tong_44-46DG')
        pi_tong_50_52DG = self.env.ref('metro_park_base.pi_tong_50-52DG')
        pi_tong_54_56DG = self.env.ref('metro_park_base.pi_tong_54-56DG')
        pi_tong_58_100DG = self.env.ref('metro_park_base.pi_tong_58-100DG')
        pi_tong_62_64DG = self.env.ref('metro_park_base.pi_tong_62-64DG')
        pi_tong_66_68DG = self.env.ref('metro_park_base.pi_tong_66-68DG')
        pi_tong_70_72DG = self.env.ref('metro_park_base.pi_tong_70-72DG')
        pi_tong_74_76DG = self.env.ref('metro_park_base.pi_tong_74-76DG')
        pi_tong_78_90DG = self.env.ref('metro_park_base.pi_tong_78-90DG')
        pi_tong_82_84DG = self.env.ref('metro_park_base.pi_tong_82-84DG')
        pi_tong_86_88DG = self.env.ref('metro_park_base.pi_tong_86-88DG')
        pi_tong_92_94DG = self.env.ref('metro_park_base.pi_tong_92-94DG')
        pi_tong_96_98DG = self.env.ref('metro_park_base.pi_tong_96-98DG')
        pi_tong_102_104DG = self.env.ref('metro_park_base.pi_tong_102-104DG')
        pi_tong_106_110DG = self.env.ref('metro_park_base.pi_tong_106-110DG')
        pi_tong_114DG = self.env.ref('metro_park_base.pi_tong_114DG')
        pi_tong_116_122DG = self.env.ref('metro_park_base.pi_tong_116-122DG')
        pi_tong_128DG = self.env.ref('metro_park_base.pi_tong_128DG')
        pi_tong_130DG = self.env.ref('metro_park_base.pi_tong_130DG')

        # 从标以仿真程序在1920 * 1280上面的位置为准
        # pi_tong_switch_2
        pi_tong_switch_2.positive_rail = False
        pi_tong_switch_2.negative_rail = False
        pi_tong_switch_2.header_rail = pi_tong_D2G.id
        pi_tong_switch_2.positive_switch = pi_tong_switch_112.id
        pi_tong_switch_2.negative_switch = pi_tong_switch_4.id
        pi_tong_switch_2.header_switch = False
        pi_tong_switch_2.x_pos = 0
        pi_tong_switch_2.y_pos = 0

        # pi_tong_switch_4
        pi_tong_switch_4.positive_rail = pi_tong_T1101G.id
        pi_tong_switch_4.negative_rail = False
        pi_tong_switch_4.header_rail = False
        pi_tong_switch_4.positive_switch = False
        pi_tong_switch_4.negative_switch = pi_tong_switch_2.id
        pi_tong_switch_4.header_switch = pi_tong_switch_12.id
        pi_tong_switch_4.x_pos = 0
        pi_tong_switch_4.y_pos = 0

        # pi_tong_switch_6
        pi_tong_switch_6.positive_rail = pi_tong_T1126G.id
        pi_tong_switch_6.negative_rail = pi_tong_D4G.id
        pi_tong_switch_6.header_rail = False
        pi_tong_switch_6.positive_switch = False
        pi_tong_switch_6.negative_switch = False
        pi_tong_switch_6.header_switch = pi_tong_switch_8.id
        pi_tong_switch_6.x_pos = 0
        pi_tong_switch_6.y_pos = 0

        # pi_tong_switch_8
        pi_tong_switch_8.positive_rail = False
        pi_tong_switch_8.negative_rail = False
        pi_tong_switch_8.header_rail = False
        pi_tong_switch_8.positive_switch = pi_tong_switch_14.id
        pi_tong_switch_8.negative_switch = pi_tong_switch_10.id
        pi_tong_switch_8.header_switch = pi_tong_switch_6.id
        pi_tong_switch_8.x_pos = 0
        pi_tong_switch_8.y_pos = 0

        # pi_tong_switch_10
        pi_tong_switch_10.positive_rail = False
        pi_tong_switch_10.negative_rail = False
        pi_tong_switch_10.header_rail = False
        pi_tong_switch_10.positive_switch = pi_tong_switch_12.id
        pi_tong_switch_10.negative_switch = pi_tong_switch_8.id
        pi_tong_switch_10.header_switch = pi_tong_switch_58.id
        pi_tong_switch_10.x_pos = 0
        pi_tong_switch_10.y_pos = 0

        # pi_tong_switch_12
        pi_tong_switch_12.positive_rail = False
        pi_tong_switch_12.negative_rail = False
        pi_tong_switch_12.header_rail = False
        pi_tong_switch_12.positive_switch = pi_tong_switch_10.id
        pi_tong_switch_12.negative_switch = pi_tong_switch_14.id
        pi_tong_switch_12.header_switch = pi_tong_switch_4.id
        pi_tong_switch_12.x_pos = 0
        pi_tong_switch_12.y_pos = 0

        # pi_tong_switch_14
        pi_tong_switch_14.positive_rail = False
        pi_tong_switch_14.negative_rail = False
        pi_tong_switch_14.header_rail = False
        pi_tong_switch_14.positive_switch = pi_tong_switch_8.id
        pi_tong_switch_14.negative_switch = pi_tong_switch_12.id
        pi_tong_switch_14.header_switch = pi_tong_switch_16.id
        pi_tong_switch_14.x_pos = 0  # 和13对齐
        pi_tong_switch_14.y_pos = 0

        # pi_tong_switch_16
        pi_tong_switch_16.positive_rail = False
        pi_tong_switch_16.negative_rail = pi_tong_16_D50WG.id
        pi_tong_switch_16.header_rail = False
        pi_tong_switch_16.positive_switch = pi_tong_switch_18.id
        pi_tong_switch_16.negative_switch = False
        pi_tong_switch_16.header_switch = pi_tong_switch_14.id
        pi_tong_switch_16.x_pos = 0
        pi_tong_switch_16.y_pos = 0

        # pi_tong_switch_18
        pi_tong_switch_18.positive_rail = False
        pi_tong_switch_18.negative_rail = False
        pi_tong_switch_18.header_rail = False
        pi_tong_switch_18.positive_switch = pi_tong_switch_36.id
        pi_tong_switch_18.negative_switch = pi_tong_switch_20.id
        pi_tong_switch_18.header_switch = pi_tong_switch_16.id
        pi_tong_switch_18.x_pos = 0
        pi_tong_switch_18.y_pos = 0

        # pi_tong_switch_20
        pi_tong_switch_20.positive_rail = False
        pi_tong_switch_20.negative_rail = False
        pi_tong_switch_20.header_rail = False
        pi_tong_switch_20.positive_switch = pi_tong_switch_32.id
        pi_tong_switch_20.negative_switch = pi_tong_switch_22.id
        pi_tong_switch_20.header_switch = pi_tong_switch_18.id
        pi_tong_switch_20.x_pos = 0
        pi_tong_switch_20.y_pos = 0

        # pi_tong_switch_22
        pi_tong_switch_22.positive_rail = False
        pi_tong_switch_22.negative_rail = False
        pi_tong_switch_22.header_rail = False
        pi_tong_switch_22.positive_switch = pi_tong_switch_28.id
        pi_tong_switch_22.negative_switch = pi_tong_switch_24.id
        pi_tong_switch_22.header_switch = pi_tong_switch_20.id
        pi_tong_switch_22.x_pos = 0
        pi_tong_switch_22.y_pos = 0

        # pi_tong_switch_24
        pi_tong_switch_24.positive_rail = False
        pi_tong_switch_24.negative_rail = pi_tong_2G.id
        pi_tong_switch_24.header_rail = False
        pi_tong_switch_24.positive_switch = pi_tong_switch_26.id
        pi_tong_switch_24.negative_switch = False
        pi_tong_switch_24.header_switch = pi_tong_switch_22.id
        pi_tong_switch_24.x_pos = 0
        pi_tong_switch_24.y_pos = 0

        # pi_tong_switch_26
        pi_tong_switch_26.positive_rail = pi_tong_4G.id
        pi_tong_switch_26.negative_rail = pi_tong_3G.id
        pi_tong_switch_26.header_rail = False
        pi_tong_switch_26.positive_switch = False
        pi_tong_switch_26.negative_switch = False
        pi_tong_switch_26.header_switch = pi_tong_switch_24.id
        pi_tong_switch_26.x_pos = 0
        pi_tong_switch_26.y_pos = 0

        # pi_tong_switch_28
        pi_tong_switch_28.positive_rail = False
        pi_tong_switch_28.negative_rail = pi_tong_5G.id
        pi_tong_switch_28.header_rail = False
        pi_tong_switch_28.positive_switch = pi_tong_switch_30.id
        pi_tong_switch_28.negative_switch = False
        pi_tong_switch_28.header_switch = pi_tong_switch_22.id
        pi_tong_switch_28.x_pos = 0
        pi_tong_switch_28.y_pos = 0

        # pi_tong_switch_30
        pi_tong_switch_30.positive_rail = pi_tong_7G.id
        pi_tong_switch_30.negative_rail = pi_tong_6G.id
        pi_tong_switch_30.header_rail = False
        pi_tong_switch_30.positive_switch = False
        pi_tong_switch_30.negative_switch = False
        pi_tong_switch_30.header_switch = pi_tong_switch_28.id
        pi_tong_switch_30.x_pos = 0
        pi_tong_switch_30.y_pos = 0

        # pi_tong_switch_32
        pi_tong_switch_32.positive_rail = pi_tong_10G.id
        pi_tong_switch_32.negative_rail = False
        pi_tong_switch_32.header_rail = False
        pi_tong_switch_32.positive_switch = False
        pi_tong_switch_32.negative_switch = pi_tong_switch_34.id
        pi_tong_switch_32.header_switch = pi_tong_switch_20.id
        pi_tong_switch_32.x_pos = 0
        pi_tong_switch_32.y_pos = 0

        # pi_tong_switch_34
        pi_tong_switch_34.positive_rail = pi_tong_9G.id
        pi_tong_switch_34.negative_rail = pi_tong_8G.id
        pi_tong_switch_34.header_rail = False
        pi_tong_switch_34.positive_switch = False
        pi_tong_switch_34.negative_switch = False
        pi_tong_switch_34.header_switch = pi_tong_switch_32.id
        pi_tong_switch_34.x_pos = 0
        pi_tong_switch_34.y_pos = 0

        # pi_tong_switch_36
        pi_tong_switch_36.positive_rail = False
        pi_tong_switch_36.negative_rail = False
        pi_tong_switch_36.header_rail = False
        pi_tong_switch_36.positive_switch = pi_tong_switch_38.id
        pi_tong_switch_36.negative_switch = pi_tong_switch_48.id
        pi_tong_switch_36.header_switch = pi_tong_switch_18.id
        pi_tong_switch_36.x_pos = 0
        pi_tong_switch_36.y_pos = 0

        # pi_tong_switch_38
        pi_tong_switch_38.positive_rail = False
        pi_tong_switch_38.negative_rail = False
        pi_tong_switch_38.header_rail = False
        pi_tong_switch_38.positive_switch = pi_tong_switch_44.id
        pi_tong_switch_38.negative_switch = pi_tong_switch_40.id
        pi_tong_switch_38.header_switch = pi_tong_switch_36.id
        pi_tong_switch_38.x_pos = 0
        pi_tong_switch_38.y_pos = 0

        # pi_tong_switch_40
        pi_tong_switch_40.positive_rail = False
        pi_tong_switch_40.negative_rail = pi_tong_11G.id
        pi_tong_switch_40.header_rail = False
        pi_tong_switch_40.positive_switch = pi_tong_switch_42.id
        pi_tong_switch_40.negative_switch = False
        pi_tong_switch_40.header_switch = pi_tong_switch_38.id
        pi_tong_switch_40.x_pos = 0
        pi_tong_switch_40.y_pos = 0

        # pi_tong_switch_42
        pi_tong_switch_42.positive_rail = pi_tong_13G.id
        pi_tong_switch_42.negative_rail = pi_tong_12G.id
        pi_tong_switch_42.header_rail = False
        pi_tong_switch_42.positive_switch = False
        pi_tong_switch_42.negative_switch = False
        pi_tong_switch_42.header_switch = pi_tong_switch_40.id
        pi_tong_switch_42.x_pos = 0
        pi_tong_switch_42.y_pos = 0

        # pi_tong_switch_44
        pi_tong_switch_44.positive_rail = pi_tong_16G.id
        pi_tong_switch_44.negative_rail = False
        pi_tong_switch_44.header_rail = False
        pi_tong_switch_44.positive_switch = False
        pi_tong_switch_44.negative_switch = pi_tong_switch_46.id
        pi_tong_switch_44.header_switch = pi_tong_switch_38.id
        pi_tong_switch_44.x_pos = 0
        pi_tong_switch_44.y_pos = 0

        # pi_tong_switch_46
        pi_tong_switch_46.positive_rail = pi_tong_14G.id
        pi_tong_switch_46.negative_rail = pi_tong_15G.id
        pi_tong_switch_46.header_rail = False
        pi_tong_switch_46.positive_switch = False
        pi_tong_switch_46.negative_switch = False
        pi_tong_switch_46.header_switch = pi_tong_switch_44.id
        pi_tong_switch_46.x_pos = 0
        pi_tong_switch_46.y_pos = 0

        # pi_tong_switch_48
        pi_tong_switch_48.positive_rail = False
        pi_tong_switch_48.negative_rail = False
        pi_tong_switch_48.header_rail = False
        pi_tong_switch_48.positive_switch = pi_tong_switch_50.id
        pi_tong_switch_48.negative_switch = pi_tong_switch_54.id
        pi_tong_switch_48.header_switch = pi_tong_switch_36.id
        pi_tong_switch_48.x_pos = 0
        pi_tong_switch_48.y_pos = 0

        # pi_tong_switch_50
        pi_tong_switch_50.positive_rail = False
        pi_tong_switch_50.negative_rail = pi_tong_17G.id
        pi_tong_switch_50.header_rail = False
        pi_tong_switch_50.positive_switch = pi_tong_switch_52.id
        pi_tong_switch_50.negative_switch = False
        pi_tong_switch_50.header_switch = pi_tong_switch_48.id
        pi_tong_switch_50.x_pos = 0
        pi_tong_switch_50.y_pos = 0

        # pi_tong_switch_52
        pi_tong_switch_52.positive_rail = pi_tong_19G.id
        pi_tong_switch_52.negative_rail = pi_tong_18G.id
        pi_tong_switch_52.header_rail = pi_tong_switch_50.id
        pi_tong_switch_52.positive_switch = False
        pi_tong_switch_52.negative_switch = False
        pi_tong_switch_52.header_switch = False
        pi_tong_switch_52.x_pos = 0
        pi_tong_switch_52.y_pos = 0

        # pi_tong_switch_54
        pi_tong_switch_54.positive_rail = pi_tong_22G.id
        pi_tong_switch_54.negative_rail = False
        pi_tong_switch_54.header_rail = False
        pi_tong_switch_54.positive_switch = False
        pi_tong_switch_54.negative_switch = pi_tong_switch_56.id
        pi_tong_switch_54.header_switch = pi_tong_switch_48.id
        pi_tong_switch_54.x_pos = 0
        pi_tong_switch_54.y_pos = 0

        # pi_tong_switch_56
        pi_tong_switch_56.positive_rail = pi_tong_20G.id
        pi_tong_switch_56.negative_rail = pi_tong_21G.id
        pi_tong_switch_56.header_rail = False
        pi_tong_switch_56.positive_switch = False
        pi_tong_switch_56.negative_switch = False
        pi_tong_switch_56.header_switch = pi_tong_switch_54.id
        pi_tong_switch_56.x_pos = 0
        pi_tong_switch_56.y_pos = 0

        # pi_tong_switch_58
        pi_tong_switch_58.positive_rail = False
        pi_tong_switch_58.negative_rail = False
        pi_tong_switch_58.header_rail = False
        pi_tong_switch_58.positive_switch = pi_tong_switch_60.id
        pi_tong_switch_58.negative_switch = pi_tong_switch_100.id
        pi_tong_switch_58.header_switch = pi_tong_switch_10.id
        pi_tong_switch_58.x_pos = 0
        pi_tong_switch_58.y_pos = 0

        # pi_tong_switch_60
        pi_tong_switch_60.positive_rail = False
        pi_tong_switch_60.negative_rail = False
        pi_tong_switch_60.header_rail = False
        pi_tong_switch_60.positive_switch = pi_tong_switch_62.id
        pi_tong_switch_60.negative_switch = pi_tong_switch_78.id
        pi_tong_switch_60.header_switch = pi_tong_switch_58.id
        pi_tong_switch_60.x_pos = 0
        pi_tong_switch_60.y_pos = 0

        # pi_tong_switch_62
        pi_tong_switch_62.positive_rail = False
        pi_tong_switch_62.negative_rail = False
        pi_tong_switch_62.header_rail = False
        pi_tong_switch_62.positive_switch = pi_tong_switch_64.id
        pi_tong_switch_62.negative_switch = pi_tong_switch_74.id
        pi_tong_switch_62.header_switch = pi_tong_switch_60.id
        pi_tong_switch_62.x_pos = 0
        pi_tong_switch_62.y_pos = 0

        # pi_tong_switch_64
        pi_tong_switch_64.positive_rail = False
        pi_tong_switch_64.negative_rail = False
        pi_tong_switch_64.header_rail = False
        pi_tong_switch_64.positive_switch = pi_tong_switch_66.id
        pi_tong_switch_64.negative_switch = pi_tong_switch_70.id
        pi_tong_switch_64.header_switch = pi_tong_switch_62.id
        pi_tong_switch_64.x_pos = 0
        pi_tong_switch_64.y_pos = 0

        # pi_tong_switch_66
        pi_tong_switch_66.positive_rail = False
        pi_tong_switch_66.negative_rail = pi_tong_25G.id
        pi_tong_switch_66.header_rail = False
        pi_tong_switch_66.positive_switch = pi_tong_switch_68.id
        pi_tong_switch_66.negative_switch = False
        pi_tong_switch_66.header_switch = pi_tong_switch_64.id
        pi_tong_switch_66.x_pos = 0
        pi_tong_switch_66.y_pos = 0

        # pi_tong_switch_68
        pi_tong_switch_68.positive_rail = pi_tong_23G.id
        pi_tong_switch_68.negative_rail = pi_tong_24G.id
        pi_tong_switch_68.header_rail = False
        pi_tong_switch_68.positive_switch = False
        pi_tong_switch_68.negative_switch = False
        pi_tong_switch_68.header_switch = pi_tong_switch_66.id
        pi_tong_switch_68.x_pos = 0
        pi_tong_switch_68.y_pos = 0

        # pi_tong_switch_70
        pi_tong_switch_70.positive_rail = False
        pi_tong_switch_70.negative_rail = pi_tong_28G.id
        pi_tong_switch_70.header_rail = False
        pi_tong_switch_70.positive_switch = pi_tong_switch_72.id
        pi_tong_switch_70.negative_switch = False
        pi_tong_switch_70.header_switch = pi_tong_switch_64.id
        pi_tong_switch_70.x_pos = 0
        pi_tong_switch_70.y_pos = 0

        # pi_tong_switch_72
        pi_tong_switch_72.positive_rail = pi_tong_27G.id
        pi_tong_switch_72.negative_rail = pi_tong_26G.id
        pi_tong_switch_72.header_rail = False
        pi_tong_switch_72.positive_switch = False
        pi_tong_switch_72.negative_switch = False
        pi_tong_switch_72.header_switch = pi_tong_switch_70.id
        pi_tong_switch_72.x_pos = 0
        pi_tong_switch_72.y_pos = 0

        # pi_tong_switch_74
        pi_tong_switch_74.positive_rail = False
        pi_tong_switch_74.negative_rail = pi_tong_31G.id
        pi_tong_switch_74.header_rail = False
        pi_tong_switch_74.positive_switch = pi_tong_switch_76.id
        pi_tong_switch_74.negative_switch = False
        pi_tong_switch_74.header_switch = pi_tong_switch_62.id
        pi_tong_switch_74.x_pos = 0
        pi_tong_switch_74.y_pos = 0

        # pi_tong_switch_76
        pi_tong_switch_76.positive_rail = pi_tong_29G.id
        pi_tong_switch_76.negative_rail = pi_tong_30G.id
        pi_tong_switch_76.header_rail = False
        pi_tong_switch_76.positive_switch = False
        pi_tong_switch_76.negative_switch = False
        pi_tong_switch_76.header_switch = pi_tong_switch_74.id
        pi_tong_switch_76.x_pos = 0
        pi_tong_switch_76.y_pos = 0

        # pi_tong_switch_78
        pi_tong_switch_78.positive_rail = False
        pi_tong_switch_78.negative_rail = False
        pi_tong_switch_78.header_rail = False
        pi_tong_switch_78.positive_switch = pi_tong_switch_80.id
        pi_tong_switch_78.negative_switch = pi_tong_switch_90.id
        pi_tong_switch_78.header_switch = pi_tong_switch_60.id
        pi_tong_switch_78.x_pos = 0
        pi_tong_switch_78.y_pos = 0

        # pi_tong_switch_80
        pi_tong_switch_80.positive_rail = False
        pi_tong_switch_80.negative_rail = False
        pi_tong_switch_80.header_rail = False
        pi_tong_switch_80.positive_switch = pi_tong_switch_82.id
        pi_tong_switch_80.negative_switch = pi_tong_switch_86.id
        pi_tong_switch_80.header_switch = pi_tong_switch_78.id
        pi_tong_switch_80.x_pos = 0
        pi_tong_switch_80.y_pos = 0

        # pi_tong_switch_82
        pi_tong_switch_82.positive_rail = False
        pi_tong_switch_82.negative_rail = pi_tong_34G.id
        pi_tong_switch_82.header_rail = False
        pi_tong_switch_82.positive_switch = pi_tong_switch_84.id
        pi_tong_switch_82.negative_switch = False
        pi_tong_switch_82.header_switch = pi_tong_switch_80.id
        pi_tong_switch_82.x_pos = 0
        pi_tong_switch_82.y_pos = 0

        # pi_tong_switch_84
        pi_tong_switch_84.positive_rail = pi_tong_33G.id
        pi_tong_switch_84.negative_rail = pi_tong_32G.id
        pi_tong_switch_84.header_rail = False
        pi_tong_switch_84.positive_switch = False
        pi_tong_switch_84.negative_switch = False
        pi_tong_switch_84.header_switch = pi_tong_switch_82.id
        pi_tong_switch_84.x_pos = 0
        pi_tong_switch_84.y_pos = 0

        # pi_tong_switch_86
        pi_tong_switch_86.positive_rail = False
        pi_tong_switch_86.negative_rail = pi_tong_37G.id
        pi_tong_switch_86.header_rail = False
        pi_tong_switch_86.positive_switch = pi_tong_switch_88.id
        pi_tong_switch_86.negative_switch = False
        pi_tong_switch_86.header_switch = pi_tong_switch_80.id
        pi_tong_switch_86.x_pos = 0
        pi_tong_switch_86.y_pos = 0

        # pi_tong_switch_88
        pi_tong_switch_88.positive_rail = pi_tong_35G.id
        pi_tong_switch_88.negative_rail = pi_tong_36G.id
        pi_tong_switch_88.header_rail = False
        pi_tong_switch_88.positive_switch = False
        pi_tong_switch_88.negative_switch = False
        pi_tong_switch_88.header_switch = pi_tong_switch_86.id
        pi_tong_switch_88.x_pos = 0
        pi_tong_switch_88.y_pos = 0

        # pi_tong_switch_90
        pi_tong_switch_90.positive_rail = False
        pi_tong_switch_90.negative_rail = False
        pi_tong_switch_90.header_rail = False
        pi_tong_switch_90.positive_switch = pi_tong_switch_92.id
        pi_tong_switch_90.negative_switch = pi_tong_switch_96.id
        pi_tong_switch_90.header_switch = pi_tong_switch_78.id
        pi_tong_switch_90.x_pos = 0
        pi_tong_switch_90.y_pos = 0

        # pi_tong_switch_92
        pi_tong_switch_92.positive_rail = False
        pi_tong_switch_92.negative_rail = pi_tong_40G.id
        pi_tong_switch_92.header_rail = False
        pi_tong_switch_92.positive_switch = pi_tong_switch_94.id
        pi_tong_switch_92.negative_switch = False
        pi_tong_switch_92.header_switch = pi_tong_switch_90.id
        pi_tong_switch_92.x_pos = 0
        pi_tong_switch_92.y_pos = 0

        # pi_tong_switch_94
        pi_tong_switch_84.positive_rail = pi_tong_38G.id
        pi_tong_switch_84.negative_rail = pi_tong_39G.id
        pi_tong_switch_84.header_rail = False
        pi_tong_switch_84.positive_switch = False
        pi_tong_switch_84.negative_switch = False
        pi_tong_switch_84.header_switch = pi_tong_switch_92.id
        pi_tong_switch_84.x_pos = 0
        pi_tong_switch_84.y_pos = 0

        # pi_tong_switch_96
        pi_tong_switch_96.positive_rail = False
        pi_tong_switch_96.negative_rail = pi_tong_43G.id
        pi_tong_switch_96.header_rail = False
        pi_tong_switch_96.positive_switch = pi_tong_switch_98.id
        pi_tong_switch_96.negative_switch = False
        pi_tong_switch_96.header_switch = pi_tong_switch_90.id
        pi_tong_switch_96.x_pos = 0
        pi_tong_switch_96.y_pos = 0

        # pi_tong_switch_98
        pi_tong_switch_98.positive_rail = pi_tong_41G.id
        pi_tong_switch_98.negative_rail = pi_tong_42G.id
        pi_tong_switch_98.header_rail = False
        pi_tong_switch_98.positive_switch = False
        pi_tong_switch_98.negative_switch = False
        pi_tong_switch_98.header_switch = pi_tong_switch_96.id
        pi_tong_switch_98.x_pos = 0
        pi_tong_switch_98.y_pos = 0

        # pi_tong_switch_100
        pi_tong_switch_100.positive_rail = pi_tong_100_102WG.id
        pi_tong_switch_100.negative_rail = pi_tong_100_106WG.id
        pi_tong_switch_100.header_rail = False
        pi_tong_switch_100.positive_switch = False
        pi_tong_switch_100.negative_switch = False
        pi_tong_switch_100.header_switch = pi_tong_switch_58.id
        pi_tong_switch_100.x_pos = 0
        pi_tong_switch_100.y_pos = 0

        # pi_tong_switch_102
        pi_tong_switch_102.positive_rail = pi_tong_46G.id
        pi_tong_switch_102.negative_rail = False
        pi_tong_switch_102.header_rail = pi_tong_100_102WG.id
        pi_tong_switch_102.positive_switch = False
        pi_tong_switch_102.negative_switch = pi_tong_switch_104.id
        pi_tong_switch_102.header_switch = False
        pi_tong_switch_102.x_pos = 0
        pi_tong_switch_102.y_pos = 0

        # pi_tong_switch_104
        pi_tong_switch_104.positive_rail = pi_tong_44G.id
        pi_tong_switch_104.negative_rail = pi_tong_45G.id
        pi_tong_switch_104.header_rail = False
        pi_tong_switch_104.positive_switch = False
        pi_tong_switch_104.negative_switch = False
        pi_tong_switch_104.header_switch = pi_tong_switch_102.id
        pi_tong_switch_104.x_pos = 0
        pi_tong_switch_104.y_pos = 0

        # pi_tong_switch_106
        pi_tong_switch_106.positive_rail = False
        pi_tong_switch_106.negative_rail = False
        pi_tong_switch_106.header_rail = pi_tong_100_106WG.id
        pi_tong_switch_106.positive_switch = pi_tong_switch_110.id
        pi_tong_switch_106.negative_switch = pi_tong_switch_108.id
        pi_tong_switch_106.header_switch = False
        pi_tong_switch_106.x_pos = 0
        pi_tong_switch_106.y_pos = 0

        # pi_tong_switch_108
        pi_tong_switch_108.positive_rail = pi_tong_48G.id
        pi_tong_switch_108.negative_rail = pi_tong_47G.id
        pi_tong_switch_108.header_rail = False
        pi_tong_switch_108.positive_switch = False
        pi_tong_switch_108.negative_switch = False
        pi_tong_switch_108.header_switch = pi_tong_switch_106.id
        pi_tong_switch_108.x_pos = 0
        pi_tong_switch_108.y_pos = 0

        # pi_tong_switch_110
        pi_tong_switch_110.positive_rail = pi_tong_49G.id
        pi_tong_switch_110.negative_rail = pi_tong_50G.id
        pi_tong_switch_110.header_rail = False
        pi_tong_switch_110.positive_switch = False
        pi_tong_switch_110.negative_switch = False
        pi_tong_switch_110.header_switch = pi_tong_switch_106.id
        pi_tong_switch_110.x_pos = 0
        pi_tong_switch_110.y_pos = 0

        # pi_tong_switch_112
        pi_tong_switch_112.positive_rail = False
        pi_tong_switch_112.negative_rail = False
        pi_tong_switch_112.header_rail = False
        pi_tong_switch_112.positive_switch = pi_tong_switch_114.id
        pi_tong_switch_112.negative_switch = pi_tong_switch_124.id
        pi_tong_switch_112.header_switch = pi_tong_switch_2.id
        pi_tong_switch_112.x_pos = 0
        pi_tong_switch_112.y_pos = 0

        # pi_tong_switch_114
        pi_tong_switch_114.positive_rail = pi_tong_114_116WG.id
        pi_tong_switch_114.negative_rail = pi_tong_56G.id
        pi_tong_switch_114.header_rail = False
        pi_tong_switch_114.positive_switch = False
        pi_tong_switch_114.negative_switch = False
        pi_tong_switch_114.header_switch = pi_tong_switch_112.id
        pi_tong_switch_114.x_pos = 0
        pi_tong_switch_114.y_pos = 0

        # pi_tong_switch_116
        pi_tong_switch_116.positive_rail = pi_tong_51G.id
        pi_tong_switch_116.negative_rail = False
        pi_tong_switch_116.header_rail = pi_tong_114_116WG.id
        pi_tong_switch_116.positive_switch = False
        pi_tong_switch_116.negative_switch = pi_tong_switch_118.id
        pi_tong_switch_116.header_switch = False
        pi_tong_switch_116.x_pos = 0
        pi_tong_switch_116.y_pos = 0

        # pi_tong_switch_118
        pi_tong_switch_118.positive_rail = False
        pi_tong_switch_118.negative_rail = False
        pi_tong_switch_118.header_rail = False
        pi_tong_switch_118.positive_switch = pi_tong_switch_120.id
        pi_tong_switch_118.negative_switch = pi_tong_switch_122.id
        pi_tong_switch_118.header_switch = pi_tong_switch_116.id
        pi_tong_switch_118.x_pos = 0
        pi_tong_switch_118.y_pos = 0

        # pi_tong_switch_120
        pi_tong_switch_120.positive_rail = pi_tong_53G.id
        pi_tong_switch_120.negative_rail = pi_tong_52G.id
        pi_tong_switch_120.header_rail = False
        pi_tong_switch_120.positive_switch = False
        pi_tong_switch_120.negative_switch = False
        pi_tong_switch_120.header_switch = pi_tong_switch_118.id
        pi_tong_switch_120.x_pos = 0
        pi_tong_switch_120.y_pos = 0

        # pi_tong_switch_122
        pi_tong_switch_122.positive_rail = pi_tong_54G.id
        pi_tong_switch_122.negative_rail = pi_tong_55G.id
        pi_tong_switch_122.header_rail = False
        pi_tong_switch_122.positive_switch = False
        pi_tong_switch_122.negative_switch = False
        pi_tong_switch_122.header_switch = pi_tong_switch_118.id
        pi_tong_switch_122.x_pos = 0
        pi_tong_switch_122.y_pos = 0

        # pi_tong_switch_124
        pi_tong_switch_124.positive_rail = pi_tong_57G.id
        pi_tong_switch_124.negative_rail = False
        pi_tong_switch_124.header_rail = False
        pi_tong_switch_124.positive_switch = False
        pi_tong_switch_124.negative_switch = pi_tong_switch_126.id
        pi_tong_switch_124.header_switch = pi_tong_switch_112.id
        pi_tong_switch_124.x_pos = 0
        pi_tong_switch_124.y_pos = 0

        # pi_tong_switch_126
        pi_tong_switch_126.positive_rail = pi_tong_58G.id
        pi_tong_switch_126.negative_rail = pi_tong_126_128WG.id
        pi_tong_switch_126.header_rail = False
        pi_tong_switch_126.positive_switch = False
        pi_tong_switch_126.negative_switch = False
        pi_tong_switch_126.header_switch = pi_tong_switch_124.id
        pi_tong_switch_126.x_pos = 0
        pi_tong_switch_126.y_pos = 0

        # pi_tong_switch_128
        pi_tong_switch_128.positive_rail = pi_tong_61G.id
        pi_tong_switch_128.negative_rail = False
        pi_tong_switch_128.header_rail = pi_tong_126_128WG.id
        pi_tong_switch_128.positive_switch = False
        pi_tong_switch_128.negative_switch = pi_tong_switch_130.id
        pi_tong_switch_128.header_switch = False
        pi_tong_switch_128.x_pos = 0
        pi_tong_switch_128.y_pos = 0

        # pi_tong_switch_130
        pi_tong_switch_130.positive_rail = pi_tong_D22G.id
        pi_tong_switch_130.negative_rail = False
        pi_tong_switch_130.header_rail = pi_tong_D30G.id
        pi_tong_switch_130.positive_switch = False
        pi_tong_switch_130.negative_switch = pi_tong_switch_128.id
        pi_tong_switch_130.header_switch = False
        pi_tong_switch_130.x_pos = 0
        pi_tong_switch_130.y_pos = 0

        # 区段
        # pi_tong_1G
        pi_tong_1G.left_rail_id = False
        pi_tong_1G.right_rail_id = pi_tong_16_D50WG.id
        pi_tong_1G.left_switch_id = False
        pi_tong_1G.right_switch_id = False
        pi_tong_1G.left_switch_position = False
        pi_tong_1G.right_switch_position = False
        pi_tong_1G.x_pos = 0
        pi_tong_1G.y_pos = 0

        # pi_tong_2G
        pi_tong_2G.left_rail_id = False
        pi_tong_2G.right_rail_id = False
        pi_tong_2G.left_switch_id = False
        pi_tong_2G.right_switch_id = pi_tong_switch_24.id
        pi_tong_2G.left_switch_position = False
        pi_tong_2G.right_switch_position = 'negative'
        pi_tong_2G.x_pos = 0
        pi_tong_2G.y_pos = 0

        # pi_tong_3G
        pi_tong_3G.left_rail_id = False
        pi_tong_3G.right_rail_id = False
        pi_tong_3G.left_switch_id = False
        pi_tong_3G.right_switch_id = pi_tong_switch_26.id
        pi_tong_3G.left_switch_position = False
        pi_tong_3G.right_switch_position = 'negative'
        pi_tong_3G.x_pos = 0
        pi_tong_3G.y_pos = 0

        # pi_tong_4G
        pi_tong_4G.left_rail_id = False
        pi_tong_4G.right_rail_id = False
        pi_tong_4G.left_switch_id = False
        pi_tong_4G.right_switch_id = pi_tong_switch_26.id
        pi_tong_4G.left_switch_position = False
        pi_tong_4G.right_switch_position = 'positive'
        pi_tong_4G.x_pos = 0
        pi_tong_4G.y_pos = 0

        # pi_tong_5G
        pi_tong_5G.left_rail_id = False
        pi_tong_5G.right_rail_id = False
        pi_tong_5G.left_switch_id = False
        pi_tong_5G.right_switch_id = pi_tong_switch_28.id
        pi_tong_5G.left_switch_position = False
        pi_tong_5G.right_switch_position = 'negative'
        pi_tong_5G.x_pos = 0
        pi_tong_5G.y_pos = 0

        # pi_tong_6G
        pi_tong_6G.left_rail_id = False
        pi_tong_6G.right_rail_id = False
        pi_tong_6G.left_switch_id = False
        pi_tong_6G.right_switch_id = pi_tong_switch_30.id
        pi_tong_6G.left_switch_position = False
        pi_tong_6G.right_switch_position = 'negative'
        pi_tong_6G.x_pos = 0
        pi_tong_6G.y_pos = 0

        # pi_tong_7G
        pi_tong_7G.left_rail_id = False
        pi_tong_7G.right_rail_id = False
        pi_tong_7G.left_switch_id = False
        pi_tong_7G.right_switch_id = pi_tong_switch_30.id
        pi_tong_7G.left_switch_position = False
        pi_tong_7G.right_switch_position = 'positive'
        pi_tong_7G.x_pos = 0
        pi_tong_7G.y_pos = 0

        # pi_tong_8G
        pi_tong_8G.left_rail_id = False
        pi_tong_8G.right_rail_id = False
        pi_tong_8G.left_switch_id = False
        pi_tong_8G.right_switch_id = pi_tong_switch_34.id
        pi_tong_8G.left_switch_position = False
        pi_tong_8G.right_switch_position = 'negative'
        pi_tong_8G.x_pos = 0
        pi_tong_8G.y_pos = 0

        # pi_tong_9G
        pi_tong_9G.left_rail_id = False
        pi_tong_9G.right_rail_id = False
        pi_tong_9G.left_switch_id = False
        pi_tong_9G.right_switch_id = pi_tong_switch_34.id
        pi_tong_9G.left_switch_position = False
        pi_tong_9G.right_switch_position = 'positive'
        pi_tong_9G.x_pos = 0
        pi_tong_9G.y_pos = 0

        # pi_tong_10G
        pi_tong_10G.left_rail_id = False
        pi_tong_10G.right_rail_id = False
        pi_tong_10G.left_switch_id = False
        pi_tong_10G.right_switch_id = pi_tong_switch_32.id
        pi_tong_10G.left_switch_position = False
        pi_tong_10G.right_switch_position = 'positive'
        pi_tong_10G.x_pos = 0
        pi_tong_10G.y_pos = 0

        # pi_tong_11G
        pi_tong_11G.left_rail_id = False
        pi_tong_11G.right_rail_id = False
        pi_tong_11G.left_switch_id = False
        pi_tong_11G.right_switch_id = pi_tong_switch_40.id
        pi_tong_11G.left_switch_position = False
        pi_tong_11G.right_switch_position = 'negative'
        pi_tong_11G.x_pos = 0
        pi_tong_11G.y_pos = 0

        # pi_tong_12G
        pi_tong_12G.left_rail_id = False
        pi_tong_12G.right_rail_id = False
        pi_tong_12G.left_switch_id = False
        pi_tong_12G.right_switch_id = pi_tong_switch_42.id
        pi_tong_12G.left_switch_position = False
        pi_tong_12G.right_switch_position = 'negative'
        pi_tong_12G.x_pos = 0
        pi_tong_12G.y_pos = 0

        # pi_tong_13G
        pi_tong_13G.left_rail_id = False
        pi_tong_13G.right_rail_id = False
        pi_tong_13G.left_switch_id = False
        pi_tong_13G.right_switch_id = pi_tong_switch_42.id
        pi_tong_13G.left_switch_position = False
        pi_tong_13G.right_switch_position = 'positive'
        pi_tong_13G.x_pos = 0
        pi_tong_13G.y_pos = 0

        # pi_tong_14G
        pi_tong_14G.left_rail_id = False
        pi_tong_14G.right_rail_id = False
        pi_tong_14G.left_switch_id = False
        pi_tong_14G.right_switch_id = pi_tong_switch_46.id
        pi_tong_14G.left_switch_position = False
        pi_tong_14G.right_switch_position = 'negative'
        pi_tong_14G.x_pos = 0
        pi_tong_14G.y_pos = 0

        # pi_tong_15G
        pi_tong_15G.left_rail_id = False
        pi_tong_15G.right_rail_id = False
        pi_tong_15G.left_switch_id = False
        pi_tong_15G.right_switch_id = pi_tong_switch_46.id
        pi_tong_15G.left_switch_position = False
        pi_tong_15G.right_switch_position = 'positive'
        pi_tong_15G.x_pos = 0
        pi_tong_15G.y_pos = 0

        # pi_tong_16G
        pi_tong_16G.left_rail_id = False
        pi_tong_16G.right_rail_id = False
        pi_tong_16G.left_switch_id = False
        pi_tong_16G.right_switch_id = pi_tong_switch_44.id
        pi_tong_16G.left_switch_position = False
        pi_tong_16G.right_switch_position = 'positive'
        pi_tong_16G.x_pos = 0
        pi_tong_16G.y_pos = 0

        # pi_tong_17G
        pi_tong_17G.left_rail_id = False
        pi_tong_17G.right_rail_id = False
        pi_tong_17G.left_switch_id = False
        pi_tong_17G.right_switch_id = pi_tong_switch_50.id
        pi_tong_17G.left_switch_position = False
        pi_tong_17G.right_switch_position = 'negative'
        pi_tong_17G.x_pos = 0
        pi_tong_17G.y_pos = 0

        # pi_tong_18G
        pi_tong_18G.left_rail_id = False
        pi_tong_18G.right_rail_id = False
        pi_tong_18G.left_switch_id = False
        pi_tong_18G.right_switch_id = pi_tong_switch_52.id
        pi_tong_18G.left_switch_position = False
        pi_tong_18G.right_switch_position = 'negative'
        pi_tong_18G.x_pos = 0
        pi_tong_18G.y_pos = 0

        # pi_tong_19G
        pi_tong_19G.left_rail_id = False
        pi_tong_19G.right_rail_id = False
        pi_tong_19G.left_switch_id = False
        pi_tong_19G.right_switch_id = pi_tong_switch_52.id
        pi_tong_19G.left_switch_position = False
        pi_tong_19G.right_switch_position = 'positive'
        pi_tong_19G.x_pos = 0
        pi_tong_19G.y_pos = 0

        # pi_tong_20G
        pi_tong_20G.left_rail_id = False
        pi_tong_20G.right_rail_id = False
        pi_tong_20G.left_switch_id = False
        pi_tong_20G.right_switch_id = pi_tong_switch_56.id
        pi_tong_20G.left_switch_position = False
        pi_tong_20G.right_switch_position = 'positive'
        pi_tong_20G.x_pos = 0
        pi_tong_20G.y_pos = 0

        # pi_tong_21G
        pi_tong_21G.left_rail_id = False
        pi_tong_21G.right_rail_id = False
        pi_tong_21G.left_switch_id = False
        pi_tong_21G.right_switch_id = pi_tong_switch_56.id
        pi_tong_21G.left_switch_position = False
        pi_tong_21G.right_switch_position = 'negative'
        pi_tong_21G.x_pos = 0
        pi_tong_21G.y_pos = 0

        # pi_tong_22G
        pi_tong_22G.left_rail_id = False
        pi_tong_22G.right_rail_id = False
        pi_tong_22G.left_switch_id = False
        pi_tong_22G.right_switch_id = pi_tong_switch_54.id
        pi_tong_22G.left_switch_position = False
        pi_tong_22G.right_switch_position = 'negative'
        pi_tong_22G.x_pos = 0
        pi_tong_22G.y_pos = 0

        # pi_tong_23G
        pi_tong_23G.left_rail_id = False
        pi_tong_23G.right_rail_id = False
        pi_tong_23G.left_switch_id = False
        pi_tong_23G.right_switch_id = pi_tong_switch_68.id
        pi_tong_23G.left_switch_position = False
        pi_tong_23G.right_switch_position = 'positive'
        pi_tong_23G.x_pos = 0
        pi_tong_23G.y_pos = 0

        # pi_tong_24G
        pi_tong_24G.left_rail_id = False
        pi_tong_24G.right_rail_id = False
        pi_tong_24G.left_switch_id = False
        pi_tong_24G.right_switch_id = pi_tong_switch_68.id
        pi_tong_24G.left_switch_position = False
        pi_tong_24G.right_switch_position = 'negative'
        pi_tong_24G.x_pos = 0
        pi_tong_24G.y_pos = 0

        # pi_tong_25G
        pi_tong_25G.left_rail_id = False
        pi_tong_25G.right_rail_id = False
        pi_tong_25G.left_switch_id = False
        pi_tong_25G.right_switch_id = pi_tong_switch_66.id
        pi_tong_25G.left_switch_position = False
        pi_tong_25G.right_switch_position = 'negative'
        pi_tong_25G.x_pos = 0
        pi_tong_25G.y_pos = 0

        # pi_tong_26G
        pi_tong_26G.left_rail_id = False
        pi_tong_26G.right_rail_id = False
        pi_tong_26G.left_switch_id = False
        pi_tong_26G.right_switch_id = pi_tong_switch_72.id
        pi_tong_26G.left_switch_position = False
        pi_tong_26G.right_switch_position = 'negative'
        pi_tong_26G.x_pos = 0
        pi_tong_26G.y_pos = 0

        # pi_tong_27G
        pi_tong_27G.left_rail_id = False
        pi_tong_27G.right_rail_id = False
        pi_tong_27G.left_switch_id = False
        pi_tong_27G.right_switch_id = pi_tong_switch_72.id
        pi_tong_27G.left_switch_position = False
        pi_tong_27G.right_switch_position = 'positive'
        pi_tong_27G.x_pos = 0
        pi_tong_27G.y_pos = 0

        # pi_tong_28G
        pi_tong_28G.left_rail_id = False
        pi_tong_28G.right_rail_id = False
        pi_tong_28G.left_switch_id = False
        pi_tong_28G.right_switch_id = pi_tong_switch_70.id
        pi_tong_28G.left_switch_position = False
        pi_tong_28G.right_switch_position = 'negative'
        pi_tong_28G.x_pos = 0
        pi_tong_28G.y_pos = 0

        # pi_tong_29G
        pi_tong_29G.left_rail_id = False
        pi_tong_29G.right_rail_id = False
        pi_tong_29G.left_switch_id = False
        pi_tong_29G.right_switch_id = pi_tong_switch_76.id
        pi_tong_29G.left_switch_position = False
        pi_tong_29G.right_switch_position = 'positive'
        pi_tong_29G.x_pos = 0
        pi_tong_29G.y_pos = 0

        # pi_tong_30G
        pi_tong_30G.left_rail_id = False
        pi_tong_30G.right_rail_id = False
        pi_tong_30G.left_switch_id = False
        pi_tong_30G.right_switch_id = pi_tong_switch_76.id
        pi_tong_30G.left_switch_position = False
        pi_tong_30G.right_switch_position = 'negative'
        pi_tong_30G.x_pos = 0
        pi_tong_30G.y_pos = 0

        # pi_tong_31G
        pi_tong_31G.left_rail_id = False
        pi_tong_31G.right_rail_id = False
        pi_tong_31G.left_switch_id = False
        pi_tong_31G.right_switch_id = pi_tong_switch_74.id
        pi_tong_31G.left_switch_position = False
        pi_tong_31G.right_switch_position = 'negative'
        pi_tong_31G.x_pos = 0
        pi_tong_31G.y_pos = 0

        # pi_tong_32G
        pi_tong_32G.left_rail_id = False
        pi_tong_32G.right_rail_id = False
        pi_tong_32G.left_switch_id = False
        pi_tong_32G.right_switch_id = pi_tong_switch_84.id
        pi_tong_32G.left_switch_position = False
        pi_tong_32G.right_switch_position = 'negative'
        pi_tong_32G.x_pos = 0
        pi_tong_32G.y_pos = 0

        # pi_tong_33G
        pi_tong_33G.left_rail_id = False
        pi_tong_33G.right_rail_id = False
        pi_tong_33G.left_switch_id = False
        pi_tong_33G.right_switch_id = pi_tong_switch_84.id
        pi_tong_33G.left_switch_position = False
        pi_tong_33G.right_switch_position = 'positive'
        pi_tong_33G.x_pos = 0
        pi_tong_33G.y_pos = 0

        # pi_tong_34G
        pi_tong_34G.left_rail_id = False
        pi_tong_34G.right_rail_id = False
        pi_tong_34G.left_switch_id = False
        pi_tong_34G.right_switch_id = pi_tong_switch_82.id
        pi_tong_34G.left_switch_position = False
        pi_tong_34G.right_switch_position = 'negative'
        pi_tong_34G.x_pos = 0
        pi_tong_34G.y_pos = 0

        # pi_tong_35G
        pi_tong_35G.left_rail_id = False
        pi_tong_35G.right_rail_id = False
        pi_tong_35G.left_switch_id = False
        pi_tong_35G.right_switch_id = pi_tong_switch_88.id
        pi_tong_35G.left_switch_position = False
        pi_tong_35G.right_switch_position = 'positive'
        pi_tong_35G.x_pos = 0
        pi_tong_35G.y_pos = 0

        # pi_tong_36G
        pi_tong_36G.left_rail_id = False
        pi_tong_36G.right_rail_id = False
        pi_tong_36G.left_switch_id = False
        pi_tong_36G.right_switch_id = pi_tong_switch_88.id
        pi_tong_36G.left_switch_position = False
        pi_tong_36G.right_switch_position = 'negative'
        pi_tong_36G.x_pos = 0
        pi_tong_36G.y_pos = 0

        # pi_tong_37G
        pi_tong_37G.left_rail_id = False
        pi_tong_37G.right_rail_id = False
        pi_tong_37G.left_switch_id = False
        pi_tong_37G.right_switch_id = pi_tong_switch_86.id
        pi_tong_37G.left_switch_position = False
        pi_tong_37G.right_switch_position = 'negative'
        pi_tong_37G.x_pos = 0
        pi_tong_37G.y_pos = 0

        # pi_tong_38G
        pi_tong_38G.left_rail_id = False
        pi_tong_38G.right_rail_id = False
        pi_tong_38G.left_switch_id = False
        pi_tong_38G.right_switch_id = pi_tong_switch_94.id
        pi_tong_38G.left_switch_position = False
        pi_tong_38G.right_switch_position = 'positive'
        pi_tong_38G.x_pos = 0
        pi_tong_38G.y_pos = 0

        # pi_tong_39G
        pi_tong_39G.left_rail_id = False
        pi_tong_39G.right_rail_id = False
        pi_tong_39G.left_switch_id = False
        pi_tong_39G.right_switch_id = pi_tong_switch_94.id
        pi_tong_39G.left_switch_position = False
        pi_tong_39G.right_switch_position = 'negative'
        pi_tong_39G.x_pos = 0
        pi_tong_39G.y_pos = 0

        # pi_tong_40G
        pi_tong_40G.left_rail_id = False
        pi_tong_40G.right_rail_id = False
        pi_tong_40G.left_switch_id = False
        pi_tong_40G.right_switch_id = pi_tong_switch_92.id
        pi_tong_40G.left_switch_position = False
        pi_tong_40G.right_switch_position = 'negative'
        pi_tong_40G.x_pos = 0
        pi_tong_40G.y_pos = 0

        # pi_tong_41G
        pi_tong_41G.left_rail_id = False
        pi_tong_41G.right_rail_id = False
        pi_tong_41G.left_switch_id = False
        pi_tong_41G.right_switch_id = pi_tong_switch_98.id
        pi_tong_41G.left_switch_position = False
        pi_tong_41G.right_switch_position = 'positive'
        pi_tong_41G.x_pos = 0
        pi_tong_41G.y_pos = 0

        # pi_tong_42G
        pi_tong_42G.left_rail_id = False
        pi_tong_42G.right_rail_id = False
        pi_tong_42G.left_switch_id = False
        pi_tong_42G.right_switch_id = pi_tong_switch_98.id
        pi_tong_42G.left_switch_position = False
        pi_tong_42G.right_switch_position = 'negative'
        pi_tong_42G.x_pos = 0
        pi_tong_42G.y_pos = 0

        # pi_tong_43G
        pi_tong_43G.left_rail_id = False
        pi_tong_43G.right_rail_id = False
        pi_tong_43G.left_switch_id = False
        pi_tong_43G.right_switch_id = pi_tong_switch_96.id
        pi_tong_43G.left_switch_position = False
        pi_tong_43G.right_switch_position = 'negative'
        pi_tong_43G.x_pos = 0
        pi_tong_43G.y_pos = 0

        # pi_tong_44G
        pi_tong_44G.left_rail_id = False
        pi_tong_44G.right_rail_id = False
        pi_tong_44G.left_switch_id = False
        pi_tong_44G.right_switch_id = pi_tong_switch_104.id
        pi_tong_44G.left_switch_position = False
        pi_tong_44G.right_switch_position = 'positive'
        pi_tong_44G.x_pos = 0
        pi_tong_44G.y_pos = 0

        # pi_tong_45G
        pi_tong_45G.left_rail_id = False
        pi_tong_45G.right_rail_id = False
        pi_tong_45G.left_switch_id = False
        pi_tong_45G.right_switch_id = pi_tong_switch_104.id
        pi_tong_45G.left_switch_position = False
        pi_tong_45G.right_switch_position = 'negative'
        pi_tong_45G.x_pos = 0
        pi_tong_45G.y_pos = 0

        # pi_tong_46G
        pi_tong_46G.left_rail_id = False
        pi_tong_46G.right_rail_id = False
        pi_tong_46G.left_switch_id = False
        pi_tong_46G.right_switch_id = pi_tong_switch_102.id
        pi_tong_46G.left_switch_position = False
        pi_tong_46G.right_switch_position = 'positive'
        pi_tong_46G.x_pos = 0
        pi_tong_46G.y_pos = 0

        # pi_tong_47G
        pi_tong_47G.left_rail_id = False
        pi_tong_47G.right_rail_id = False
        pi_tong_47G.left_switch_id = False
        pi_tong_47G.right_switch_id = pi_tong_switch_108.id
        pi_tong_47G.left_switch_position = False
        pi_tong_47G.right_switch_position = 'negative'
        pi_tong_47G.x_pos = 0
        pi_tong_47G.y_pos = 0

        # pi_tong_48G
        pi_tong_48G.left_rail_id = False
        pi_tong_48G.right_rail_id = False
        pi_tong_48G.left_switch_id = False
        pi_tong_48G.right_switch_id = pi_tong_switch_108.id
        pi_tong_48G.left_switch_position = False
        pi_tong_48G.right_switch_position = 'positive'
        pi_tong_48G.x_pos = 0
        pi_tong_48G.y_pos = 0

        # pi_tong_49G
        pi_tong_49G.left_rail_id = False
        pi_tong_49G.right_rail_id = False
        pi_tong_49G.left_switch_id = False
        pi_tong_49G.right_switch_id = pi_tong_switch_110.id
        pi_tong_49G.left_switch_position = False
        pi_tong_49G.right_switch_position = 'positive'
        pi_tong_49G.x_pos = 0
        pi_tong_49G.y_pos = 0

        # pi_tong_50G
        pi_tong_50G.left_rail_id = False
        pi_tong_50G.right_rail_id = False
        pi_tong_50G.left_switch_id = False
        pi_tong_50G.right_switch_id = pi_tong_switch_110.id
        pi_tong_50G.left_switch_position = False
        pi_tong_50G.right_switch_position = 'negative'
        pi_tong_50G.x_pos = 0
        pi_tong_50G.y_pos = 0

        # pi_tong_51G
        pi_tong_51G.left_rail_id = False
        pi_tong_51G.right_rail_id = False
        pi_tong_51G.left_switch_id = False
        pi_tong_51G.right_switch_id = pi_tong_switch_116.id
        pi_tong_51G.left_switch_position = False
        pi_tong_51G.right_switch_position = 'positive'
        pi_tong_51G.x_pos = 0
        pi_tong_51G.y_pos = 0

        # pi_tong_52G
        pi_tong_52G.left_rail_id = False
        pi_tong_52G.right_rail_id = False
        pi_tong_52G.left_switch_id = False
        pi_tong_52G.right_switch_id = pi_tong_switch_120.id
        pi_tong_52G.left_switch_position = False
        pi_tong_52G.right_switch_position = 'negative'
        pi_tong_52G.x_pos = 0
        pi_tong_52G.y_pos = 0

        # pi_tong_53G
        pi_tong_53G.left_rail_id = False
        pi_tong_53G.right_rail_id = False
        pi_tong_53G.left_switch_id = False
        pi_tong_53G.right_switch_id = pi_tong_switch_120.id
        pi_tong_53G.left_switch_position = False
        pi_tong_53G.right_switch_position = 'positive'
        pi_tong_53G.x_pos = 0
        pi_tong_53G.y_pos = 0

        # pi_tong_54G
        pi_tong_54G.left_rail_id = False
        pi_tong_54G.right_rail_id = False
        pi_tong_54G.left_switch_id = False
        pi_tong_54G.right_switch_id = pi_tong_switch_122.id
        pi_tong_54G.left_switch_position = False
        pi_tong_54G.right_switch_position = 'positive'
        pi_tong_54G.x_pos = 0
        pi_tong_54G.y_pos = 0

        # pi_tong_55G
        pi_tong_55G.left_rail_id = False
        pi_tong_55G.right_rail_id = False
        pi_tong_55G.left_switch_id = False
        pi_tong_55G.right_switch_id = pi_tong_switch_122.id
        pi_tong_55G.left_switch_position = False
        pi_tong_55G.right_switch_position = 'negative'
        pi_tong_55G.x_pos = 0
        pi_tong_55G.y_pos = 0

        # pi_tong_56G
        pi_tong_56G.left_rail_id = False
        pi_tong_56G.right_rail_id = pi_tong_114_D36WG.id
        pi_tong_56G.left_switch_id = False
        pi_tong_56G.right_switch_id = False
        pi_tong_56G.left_switch_position = False
        pi_tong_56G.right_switch_position = False
        pi_tong_56G.x_pos = 0
        pi_tong_56G.y_pos = 0

        # pi_tong_57G
        pi_tong_57G.left_rail_id = False
        pi_tong_57G.right_rail_id = pi_tong_124_D34WG.id
        pi_tong_57G.left_switch_id = False
        pi_tong_57G.right_switch_id = False
        pi_tong_57G.left_switch_position = False
        pi_tong_57G.right_switch_position = False
        pi_tong_57G.x_pos = 0
        pi_tong_57G.y_pos = 0

        # pi_tong_58G
        pi_tong_58G.left_rail_id = False
        pi_tong_58G.right_rail_id = False
        pi_tong_58G.left_switch_id = False
        pi_tong_58G.right_switch_id = pi_tong_switch_126.id
        pi_tong_58G.left_switch_position = False
        pi_tong_58G.right_switch_position = 'positive'
        pi_tong_58G.x_pos = 0
        pi_tong_58G.y_pos = 0

        # pi_tong_61G
        pi_tong_61G.left_rail_id = False
        pi_tong_61G.right_rail_id = False
        pi_tong_61G.left_switch_id = False
        pi_tong_61G.right_switch_id = pi_tong_switch_128.id
        pi_tong_61G.left_switch_position = False
        pi_tong_61G.right_switch_position = 'positive'
        pi_tong_61G.x_pos = 0
        pi_tong_61G.y_pos = 0

        # pi_tong_T1101G
        pi_tong_T1101G.left_rail_id = False
        pi_tong_T1101G.right_rail_id = pi_tong_T1103G.id
        pi_tong_T1101G.left_switch_id = pi_tong_switch_4.id
        pi_tong_T1101G.right_switch_id = False
        pi_tong_T1101G.left_switch_position = 'positive'
        pi_tong_T1101G.right_switch_position = False
        pi_tong_T1101G.x_pos = 0
        pi_tong_T1101G.y_pos = 0

        # pi_tong_T1103G
        pi_tong_T1103G.left_rail_id = pi_tong_T1101G.id
        pi_tong_T1103G.right_rail_id = False
        pi_tong_T1103G.left_switch_id = False
        pi_tong_T1103G.right_switch_id = False
        pi_tong_T1103G.left_switch_position = False
        pi_tong_T1103G.right_switch_position = False
        pi_tong_T1103G.x_pos = 0
        pi_tong_T1103G.y_pos = 0

        # pi_tong_T1126G
        pi_tong_T1126G.left_rail_id = False
        pi_tong_T1126G.right_rail_id = pi_tong_T1124G.id
        pi_tong_T1126G.left_switch_id = pi_tong_switch_6.id
        pi_tong_T1126G.right_switch_id = False
        pi_tong_T1126G.left_switch_position = 'positive'
        pi_tong_T1126G.right_switch_position = False
        pi_tong_T1126G.x_pos = 0
        pi_tong_T1126G.y_pos = 0

        # pi_tong_T1124G
        pi_tong_T1124G.left_rail_id = pi_tong_T1126G.id
        pi_tong_T1124G.right_rail_id = False
        pi_tong_T1124G.left_switch_id = False
        pi_tong_T1124G.right_switch_id = False
        pi_tong_T1124G.left_switch_position = False
        pi_tong_T1124G.right_switch_position = False
        pi_tong_T1124G.x_pos = 0
        pi_tong_T1124G.y_pos = 0

        # pi_tong_D2G
        pi_tong_D2G.left_rail_id = False
        pi_tong_D2G.right_rail_id = False
        pi_tong_D2G.left_switch_id = pi_tong_switch_2.id
        pi_tong_D2G.right_switch_id = False
        pi_tong_D2G.left_switch_position = 'header'
        pi_tong_D2G.right_switch_position = False
        pi_tong_D2G.x_pos = 0
        pi_tong_D2G.y_pos = 0

        # pi_tong_D4G
        pi_tong_D4G.left_rail_id = False
        pi_tong_D4G.right_rail_id = False
        pi_tong_D4G.left_switch_id = pi_tong_switch_6.id
        pi_tong_D4G.right_switch_id = False
        pi_tong_D4G.left_switch_position = 'negative'
        pi_tong_D4G.right_switch_position = False
        pi_tong_D4G.x_pos = 0
        pi_tong_D4G.y_pos = 0

        # pi_tong_D22G
        pi_tong_D22G.left_rail_id = False
        pi_tong_D22G.right_rail_id = False
        pi_tong_D22G.left_switch_id = pi_tong_switch_130.id
        pi_tong_D22G.right_switch_id = False
        pi_tong_D22G.left_switch_position = 'positive'
        pi_tong_D22G.right_switch_position = False
        pi_tong_D22G.x_pos = 0
        pi_tong_D22G.y_pos = 0

        # pi_tong_D30G
        pi_tong_D30G.left_rail_id = False
        pi_tong_D30G.right_rail_id = False
        pi_tong_D30G.left_switch_id = False
        pi_tong_D30G.right_switch_id = pi_tong_switch_130.id
        pi_tong_D30G.left_switch_position = False
        pi_tong_D30G.right_switch_position = 'header'
        pi_tong_D30G.x_pos = 0
        pi_tong_D30G.y_pos = 0

        # pi_tong_16_D50WG
        pi_tong_16_D50WG.left_rail_id = pi_tong_1G.id
        pi_tong_16_D50WG.right_rail_id = False
        pi_tong_16_D50WG.left_switch_id = False
        pi_tong_16_D50WG.right_switch_id = pi_tong_switch_16.id
        pi_tong_16_D50WG.left_switch_position = False
        pi_tong_16_D50WG.right_switch_position = 'False'
        pi_tong_16_D50WG.x_pos = 0
        pi_tong_16_D50WG.y_pos = 0

        # pi_tong_100_102WG
        pi_tong_100_102WG.left_rail_id = False
        pi_tong_100_102WG.right_rail_id = False
        pi_tong_100_102WG.left_switch_id = pi_tong_switch_102.id
        pi_tong_100_102WG.right_switch_id = pi_tong_switch_100.id
        pi_tong_100_102WG.left_switch_position = 'header'
        pi_tong_100_102WG.right_switch_position = 'positive'
        pi_tong_100_102WG.x_pos = 0
        pi_tong_100_102WG.y_pos = 0

        # pi_tong_100_106WG
        pi_tong_100_106WG.left_rail_id = False
        pi_tong_100_106WG.right_rail_id = False
        pi_tong_100_106WG.left_switch_id = pi_tong_switch_106.id
        pi_tong_100_106WG.right_switch_id = pi_tong_switch_100.id
        pi_tong_100_106WG.left_switch_position = 'header'
        pi_tong_100_106WG.right_switch_position = 'negative'
        pi_tong_100_106WG.x_pos = 0
        pi_tong_100_106WG.y_pos = 0

        # pi_tong_114_116WG
        pi_tong_114_116WG.left_rail_id = False
        pi_tong_114_116WG.right_rail_id = False
        pi_tong_114_116WG.left_switch_id = pi_tong_switch_116.id
        pi_tong_114_116WG.right_switch_id = pi_tong_switch_114.id
        pi_tong_114_116WG.left_switch_position = 'header'
        pi_tong_114_116WG.right_switch_position = 'positive'
        pi_tong_114_116WG.x_pos = 0
        pi_tong_114_116WG.y_pos = 0

        # pi_tong_114_D36WG
        pi_tong_114_D36WG.left_rail_id = pi_tong_56G.id
        pi_tong_114_D36WG.right_rail_id = False
        pi_tong_114_D36WG.left_switch_id = False
        pi_tong_114_D36WG.right_switch_id = pi_tong_switch_114.id
        pi_tong_114_D36WG.left_switch_position = False
        pi_tong_114_D36WG.right_switch_position = 'negative'
        pi_tong_114_D36WG.x_pos = 0
        pi_tong_114_D36WG.y_pos = 0

        # pi_tong_124_D34WG
        pi_tong_124_D34WG.left_rail_id = pi_tong_57G.id
        pi_tong_124_D34WG.right_rail_id = False
        pi_tong_124_D34WG.left_switch_id = False
        pi_tong_124_D34WG.right_switch_id = pi_tong_switch_124.id
        pi_tong_124_D34WG.left_switch_position = False
        pi_tong_124_D34WG.right_switch_position = 'positive'
        pi_tong_124_D34WG.x_pos = 0
        pi_tong_124_D34WG.y_pos = 0

        # pi_tong_126_128WG
        pi_tong_126_128WG.left_rail_id = False
        pi_tong_126_128WG.right_rail_id = False
        pi_tong_126_128WG.left_switch_id = pi_tong_switch_128.id
        pi_tong_126_128WG.right_switch_id = pi_tong_switch_126.id
        pi_tong_126_128WG.left_switch_position = 'header'
        pi_tong_126_128WG.right_switch_position = 'negative'
        pi_tong_126_128WG.x_pos = 0
        pi_tong_126_128WG.y_pos = 0

        long_deng_shan_switch_1 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_1')
        long_deng_shan_switch_3 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_3')
        long_deng_shan_switch_5 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_5')
        long_deng_shan_switch_7 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_7')
        long_deng_shan_switch_9 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_9')
        long_deng_shan_switch_11 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_11')
        long_deng_shan_switch_13 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_13')
        long_deng_shan_switch_15 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_15')
        long_deng_shan_switch_17 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_17')
        long_deng_shan_switch_19 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_19')
        long_deng_shan_switch_21 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_21')
        long_deng_shan_switch_23 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_23')
        long_deng_shan_switch_25 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_25')
        long_deng_shan_switch_27 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_27')
        long_deng_shan_switch_29 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_29')
        long_deng_shan_switch_31 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_31')
        long_deng_shan_switch_33 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_33')
        long_deng_shan_switch_35 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_35')
        long_deng_shan_switch_37 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_37')
        long_deng_shan_switch_39 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_39')
        long_deng_shan_switch_41 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_41')
        long_deng_shan_switch_43 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_43')
        long_deng_shan_switch_45 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_45')
        long_deng_shan_switch_47 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_47')
        long_deng_shan_switch_49 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_49')
        long_deng_shan_switch_51 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_51')
        long_deng_shan_switch_53 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_53')
        long_deng_shan_switch_55 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_55')
        long_deng_shan_switch_57 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_57')
        long_deng_shan_switch_59 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_59')
        long_deng_shan_switch_61 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_61')
        long_deng_shan_switch_63 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_63')
        long_deng_shan_switch_65 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_65')
        long_deng_shan_switch_67 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_67')
        long_deng_shan_switch_69 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_69')
        long_deng_shan_switch_71 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_71')
        long_deng_shan_switch_73 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_73')
        long_deng_shan_switch_75 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_75')
        long_deng_shan_switch_77 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_77')
        long_deng_shan_switch_79 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_79')
        long_deng_shan_switch_81 = self.env.ref(
            'metro_park_base.long_deng_shan_switch_81')

        ######################################################
        long_deng_shan_rail_7AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_7AG')
        long_deng_shan_rail_7BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_7BG')
        long_deng_shan_rail_8BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_8BG')
        long_deng_shan_rail_9BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_9BG')
        long_deng_shan_rail_10BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_10BG')
        long_deng_shan_rail_11BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_11BG')
        long_deng_shan_rail_12BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_12BG')
        long_deng_shan_rail_13BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_13BG')
        long_deng_shan_rail_14BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_14BG')
        long_deng_shan_rail_15BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_15BG')
        long_deng_shan_rail_16BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_16BG')
        long_deng_shan_rail_17BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_17BG')
        long_deng_shan_rail_18BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_18BG')
        long_deng_shan_rail_19BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_19BG')
        long_deng_shan_rail_20BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_20BG')
        long_deng_shan_rail_21BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_21BG')
        long_deng_shan_rail_22BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_22BG')
        long_deng_shan_rail_23BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_23BG')
        long_deng_shan_rail_24BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_24BG')
        long_deng_shan_rail_25BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_25BG')
        long_deng_shan_rail_26BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_26BG')
        long_deng_shan_rail_27BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_27BG')
        long_deng_shan_rail_28BG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_28BG')
        long_deng_shan_rail_29G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_29G')
        long_deng_shan_rail_28AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_28AG')
        long_deng_shan_rail_27AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_27AG')
        long_deng_shan_rail_26AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_26AG')
        long_deng_shan_rail_25AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_25AG')
        long_deng_shan_rail_24AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_24AG')
        long_deng_shan_rail_23AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_23AG')
        long_deng_shan_rail_22AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_22AG')
        long_deng_shan_rail_21AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_21AG')
        long_deng_shan_rail_20AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_20AG')
        long_deng_shan_rail_19AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_19AG')
        long_deng_shan_rail_18AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_18AG')
        long_deng_shan_rail_17AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_17AG')
        long_deng_shan_rail_16AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_16AG')
        long_deng_shan_rail_15AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_15AG')
        long_deng_shan_rail_14AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_14AG')
        long_deng_shan_rail_13AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_13AG')
        long_deng_shan_rail_12AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_12AG')
        long_deng_shan_rail_11AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_11AG')
        long_deng_shan_rail_10AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_10AG')
        long_deng_shan_rail_9AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_9AG')
        long_deng_shan_rail_8AG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_8AG')
        long_deng_shan_rail_6G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_6G')
        long_deng_shan_rail_1G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_1G')
        long_deng_shan_rail_D1G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_D1G')
        long_deng_shan_rail_D3G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_D3G')
        long_deng_shan_rail_1_75WG = self.env.ref(
            'metro_park_base.long_deng_shan_rail_1_75WG')
        long_deng_shan_rail_T4617 = self.env.ref(
            'metro_park_base.long_deng_shan_rail_T4617')
        long_deng_shan_rail_T4621 = self.env.ref(
            'metro_park_base.long_deng_shan_rail_T4621')
        long_deng_shan_rail_T4615 = self.env.ref(
            'metro_park_base.long_deng_shan_rail_T4615')
        long_deng_shan_rail_T4623 = self.env.ref(
            'metro_park_base.long_deng_shan_rail_T4623')
        long_deng_shan_rail_5G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_5G')
        long_deng_shan_rail_4G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_4G')
        long_deng_shan_rail_3G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_3G')
        long_deng_shan_rail_2G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_2G')
        long_deng_shan_rail_31G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_31G')
        long_deng_shan_rail_30G = self.env.ref(
            'metro_park_base.long_deng_shan_rail_30G')

        long_deng_shan_switch_1.positive_rail = long_deng_shan_rail_1_75WG.id
        long_deng_shan_switch_1.negative_rail = False
        long_deng_shan_switch_1.header_rail = long_deng_shan_rail_D3G.id
        long_deng_shan_switch_1.header_switch = False
        long_deng_shan_switch_1.positive_switch = False
        long_deng_shan_switch_1.negative_switch = long_deng_shan_switch_3.id
        long_deng_shan_switch_1.x_pos = 360
        long_deng_shan_switch_1.y_pos = 582

        long_deng_shan_switch_3.positive_rail = long_deng_shan_rail_T4615.id
        long_deng_shan_switch_3.negative_rail = False
        long_deng_shan_switch_3.header_rail = False
        long_deng_shan_switch_3.header_switch = long_deng_shan_switch_21.id
        long_deng_shan_switch_3.positive_switch = False
        long_deng_shan_switch_3.negative_switch = long_deng_shan_switch_1.id
        long_deng_shan_switch_3.x_pos = 360
        long_deng_shan_switch_3.y_pos = 582

        long_deng_shan_switch_5.positive_rail = False
        long_deng_shan_switch_5.negative_rail = False
        long_deng_shan_switch_5.header_rail = long_deng_shan_rail_D1G.id
        long_deng_shan_switch_5.header_switch = False
        long_deng_shan_switch_5.positive_switch = long_deng_shan_switch_11.id
        long_deng_shan_switch_5.negative_switch = long_deng_shan_switch_7.id
        long_deng_shan_switch_5.x_pos = 360
        long_deng_shan_switch_5.y_pos = 582

        long_deng_shan_switch_7.positive_rail = False
        long_deng_shan_switch_7.negative_rail = False
        long_deng_shan_switch_7.header_rail = False
        long_deng_shan_switch_7.header_switch = long_deng_shan_switch_17.id
        long_deng_shan_switch_7.positive_switch = long_deng_shan_switch_9.id
        long_deng_shan_switch_7.negative_switch = long_deng_shan_switch_5.id
        long_deng_shan_switch_7.x_pos = 360
        long_deng_shan_switch_7.y_pos = 582

        long_deng_shan_switch_9.positive_rail = False
        long_deng_shan_switch_9.negative_rail = False
        long_deng_shan_switch_9.header_rail = long_deng_shan_rail_T4621.id
        long_deng_shan_switch_9.header_switch = False
        long_deng_shan_switch_9.positive_switch = long_deng_shan_switch_7.id
        long_deng_shan_switch_9.negative_switch = long_deng_shan_switch_11.id
        long_deng_shan_switch_9.x_pos = 360
        long_deng_shan_switch_9.y_pos = 582

        long_deng_shan_switch_11.positive_rail = False
        long_deng_shan_switch_11.negative_rail = False
        long_deng_shan_switch_11.header_rail = False
        long_deng_shan_switch_11.header_switch = long_deng_shan_switch_13.id
        long_deng_shan_switch_11.positive_switch = long_deng_shan_switch_9.id
        long_deng_shan_switch_11.negative_switch = long_deng_shan_switch_5.id
        long_deng_shan_switch_11.x_pos = 360
        long_deng_shan_switch_11.y_pos = 582

        long_deng_shan_switch_13.positive_rail = False
        long_deng_shan_switch_13.negative_rail = False
        long_deng_shan_switch_13.header_rail = False
        long_deng_shan_switch_13.header_switch = long_deng_shan_switch_11.id
        long_deng_shan_switch_13.positive_switch = long_deng_shan_switch_27.id
        long_deng_shan_switch_13.negative_switch = long_deng_shan_switch_15.id
        long_deng_shan_switch_13.x_pos = 360
        long_deng_shan_switch_13.y_pos = 582

        long_deng_shan_switch_15.positive_rail = long_deng_shan_rail_31G.id
        long_deng_shan_switch_15.negative_rail = long_deng_shan_rail_30G.id
        long_deng_shan_switch_15.header_rail = False
        long_deng_shan_switch_15.header_switch = long_deng_shan_switch_13.id
        long_deng_shan_switch_15.positive_switch = False
        long_deng_shan_switch_15.negative_switch = False
        long_deng_shan_switch_15.x_pos = 360
        long_deng_shan_switch_15.y_pos = 582

        long_deng_shan_switch_17.positive_rail = False
        long_deng_shan_switch_17.negative_rail = False
        long_deng_shan_switch_17.header_rail = False
        long_deng_shan_switch_17.header_switch = long_deng_shan_switch_7.id
        long_deng_shan_switch_17.positive_switch = long_deng_shan_switch_23.id
        long_deng_shan_switch_17.negative_switch = long_deng_shan_switch_19.id
        long_deng_shan_switch_17.x_pos = 360
        long_deng_shan_switch_17.y_pos = 582

        long_deng_shan_switch_19.positive_rail = False
        long_deng_shan_switch_19.negative_rail = False
        long_deng_shan_switch_19.header_rail = False
        long_deng_shan_switch_19.header_switch = long_deng_shan_switch_61.id
        long_deng_shan_switch_19.positive_switch = long_deng_shan_switch_21.id
        long_deng_shan_switch_19.negative_switch = long_deng_shan_switch_17.id
        long_deng_shan_switch_19.x_pos = 360
        long_deng_shan_switch_19.y_pos = 582

        long_deng_shan_switch_21.positive_rail = False
        long_deng_shan_switch_21.negative_rail = False
        long_deng_shan_switch_21.header_rail = False
        long_deng_shan_switch_21.header_switch = long_deng_shan_switch_3.id
        long_deng_shan_switch_21.positive_switch = long_deng_shan_switch_19.id
        long_deng_shan_switch_21.negative_switch = long_deng_shan_switch_23.id
        long_deng_shan_switch_21.x_pos = 360
        long_deng_shan_switch_21.y_pos = 582

        long_deng_shan_switch_23.positive_rail = False
        long_deng_shan_switch_23.negative_rail = False
        long_deng_shan_switch_23.header_rail = False
        long_deng_shan_switch_23.header_switch = long_deng_shan_switch_39.id
        long_deng_shan_switch_23.positive_switch = long_deng_shan_switch_17.id
        long_deng_shan_switch_23.negative_switch = long_deng_shan_switch_21.id
        long_deng_shan_switch_23.x_pos = 360
        long_deng_shan_switch_23.y_pos = 582

        long_deng_shan_switch_25.positive_rail = False
        long_deng_shan_switch_25.negative_rail = False
        long_deng_shan_switch_25.header_rail = False
        long_deng_shan_switch_25.header_switch = long_deng_shan_switch_23.id
        long_deng_shan_switch_25.positive_switch = long_deng_shan_switch_39.id
        long_deng_shan_switch_25.negative_switch = long_deng_shan_switch_27.id
        long_deng_shan_switch_25.x_pos = 360
        long_deng_shan_switch_25.y_pos = 582

        long_deng_shan_switch_27.positive_rail = False
        long_deng_shan_switch_27.negative_rail = False
        long_deng_shan_switch_27.header_rail = False
        long_deng_shan_switch_27.header_switch = long_deng_shan_switch_29.id
        long_deng_shan_switch_27.positive_switch = long_deng_shan_switch_25.id
        long_deng_shan_switch_27.negative_switch = long_deng_shan_switch_13.id
        long_deng_shan_switch_27.x_pos = 360
        long_deng_shan_switch_27.y_pos = 582

        long_deng_shan_switch_29.positive_rail = False
        long_deng_shan_switch_29.negative_rail = False
        long_deng_shan_switch_29.header_rail = False
        long_deng_shan_switch_29.header_switch = long_deng_shan_switch_27.id
        long_deng_shan_switch_29.positive_switch = long_deng_shan_switch_35.id
        long_deng_shan_switch_29.negative_switch = long_deng_shan_switch_31.id
        long_deng_shan_switch_29.x_pos = 360
        long_deng_shan_switch_29.y_pos = 582

        long_deng_shan_switch_31.positive_rail = False
        long_deng_shan_switch_31.negative_rail = long_deng_shan_rail_1G.id
        long_deng_shan_switch_31.header_rail = False
        long_deng_shan_switch_31.header_switch = long_deng_shan_switch_29.id
        long_deng_shan_switch_31.positive_switch = long_deng_shan_switch_33.id
        long_deng_shan_switch_31.negative_switch = False
        long_deng_shan_switch_31.x_pos = 360
        long_deng_shan_switch_31.y_pos = 582

        long_deng_shan_switch_33.positive_rail = long_deng_shan_rail_3G.id
        long_deng_shan_switch_33.negative_rail = long_deng_shan_rail_4G.id
        long_deng_shan_switch_33.header_rail = False
        long_deng_shan_switch_33.header_switch = long_deng_shan_switch_31.id
        long_deng_shan_switch_33.positive_switch = False
        long_deng_shan_switch_33.negative_switch = False
        long_deng_shan_switch_33.x_pos = 360
        long_deng_shan_switch_33.y_pos = 582

        long_deng_shan_switch_35.positive_rail = long_deng_shan_rail_5G.id
        long_deng_shan_switch_35.negative_rail = False
        long_deng_shan_switch_35.header_rail = False
        long_deng_shan_switch_35.header_switch = long_deng_shan_switch_27.id
        long_deng_shan_switch_35.positive_switch = False
        long_deng_shan_switch_35.negative_switch = False
        long_deng_shan_switch_35.x_pos = 360
        long_deng_shan_switch_35.y_pos = 582

        long_deng_shan_switch_37.positive_rail = long_deng_shan_rail_6G.id
        long_deng_shan_switch_37.negative_rail = long_deng_shan_rail_5G.id
        long_deng_shan_switch_37.header_rail = False
        long_deng_shan_switch_37.header_switch = long_deng_shan_switch_35.id
        long_deng_shan_switch_37.positive_switch = False
        long_deng_shan_switch_37.negative_switch = False
        long_deng_shan_switch_37.x_pos = 360
        long_deng_shan_switch_37.y_pos = 582

        long_deng_shan_switch_39.positive_rail = False
        long_deng_shan_switch_39.negative_rail = False
        long_deng_shan_switch_39.header_rail = False
        long_deng_shan_switch_39.header_switch = long_deng_shan_switch_25.id
        long_deng_shan_switch_39.positive_switch = long_deng_shan_switch_47.id
        long_deng_shan_switch_39.negative_switch = long_deng_shan_switch_41.id
        long_deng_shan_switch_39.x_pos = 360
        long_deng_shan_switch_39.y_pos = 582

        long_deng_shan_switch_41.positive_rail = False
        long_deng_shan_switch_41.negative_rail = False
        long_deng_shan_switch_41.header_rail = False
        long_deng_shan_switch_41.header_switch = long_deng_shan_switch_39.id
        long_deng_shan_switch_41.positive_switch = long_deng_shan_switch_45.id
        long_deng_shan_switch_41.negative_switch = long_deng_shan_switch_43.id
        long_deng_shan_switch_41.x_pos = 360
        long_deng_shan_switch_41.y_pos = 582

        long_deng_shan_switch_43.positive_rail = long_deng_shan_rail_8AG.id
        long_deng_shan_switch_43.negative_rail = long_deng_shan_rail_7AG.id
        long_deng_shan_switch_43.header_rail = False
        long_deng_shan_switch_43.header_switch = long_deng_shan_switch_39.id
        long_deng_shan_switch_43.positive_switch = False
        long_deng_shan_switch_43.negative_switch = False
        long_deng_shan_switch_43.x_pos = 360
        long_deng_shan_switch_43.y_pos = 582

        long_deng_shan_switch_45.positive_rail = long_deng_shan_rail_9AG.id
        long_deng_shan_switch_45.negative_rail = long_deng_shan_rail_10AG.id
        long_deng_shan_switch_45.header_rail = False
        long_deng_shan_switch_45.header_switch = long_deng_shan_switch_41.id
        long_deng_shan_switch_45.positive_switch = False
        long_deng_shan_switch_45.negative_switch = False
        long_deng_shan_switch_45.x_pos = 360
        long_deng_shan_switch_45.y_pos = 582

        long_deng_shan_switch_47.positive_rail = False
        long_deng_shan_switch_47.negative_rail = False
        long_deng_shan_switch_47.header_rail = False
        long_deng_shan_switch_47.header_switch = long_deng_shan_switch_39.id
        long_deng_shan_switch_47.positive_switch = long_deng_shan_switch_55.id
        long_deng_shan_switch_47.negative_switch = long_deng_shan_switch_49.id
        long_deng_shan_switch_47.x_pos = 360
        long_deng_shan_switch_47.y_pos = 582

        long_deng_shan_switch_49.positive_rail = False
        long_deng_shan_switch_49.negative_rail = False
        long_deng_shan_switch_49.header_rail = False
        long_deng_shan_switch_49.header_switch = long_deng_shan_switch_47.id
        long_deng_shan_switch_49.positive_switch = long_deng_shan_switch_53.id
        long_deng_shan_switch_49.negative_switch = long_deng_shan_switch_51.id
        long_deng_shan_switch_49.x_pos = 360
        long_deng_shan_switch_49.y_pos = 582

        long_deng_shan_switch_51.positive_rail = long_deng_shan_rail_12AG.id
        long_deng_shan_switch_51.negative_rail = long_deng_shan_rail_11AG.id
        long_deng_shan_switch_51.header_rail = False
        long_deng_shan_switch_51.header_switch = long_deng_shan_switch_49.id
        long_deng_shan_switch_51.positive_switch = False
        long_deng_shan_switch_51.negative_switch = False
        long_deng_shan_switch_51.x_pos = 360
        long_deng_shan_switch_51.y_pos = 582

        long_deng_shan_switch_53.positive_rail = long_deng_shan_rail_13AG.id
        long_deng_shan_switch_53.negative_rail = long_deng_shan_rail_14AG.id
        long_deng_shan_switch_53.header_rail = False
        long_deng_shan_switch_53.header_switch = long_deng_shan_switch_47.id
        long_deng_shan_switch_53.positive_switch = False
        long_deng_shan_switch_53.negative_switch = False
        long_deng_shan_switch_53.x_pos = 360
        long_deng_shan_switch_53.y_pos = 582

        long_deng_shan_switch_55.positive_rail = False
        long_deng_shan_switch_55.negative_rail = False
        long_deng_shan_switch_55.header_rail = False
        long_deng_shan_switch_55.header_switch = long_deng_shan_switch_47.id
        long_deng_shan_switch_55.positive_switch = long_deng_shan_switch_59.id
        long_deng_shan_switch_55.negative_switch = long_deng_shan_switch_59.id
        long_deng_shan_switch_55.x_pos = 360
        long_deng_shan_switch_55.y_pos = 582

        long_deng_shan_switch_57.positive_rail = long_deng_shan_rail_16AG.id
        long_deng_shan_switch_57.negative_rail = long_deng_shan_rail_15AG.id
        long_deng_shan_switch_57.header_rail = False
        long_deng_shan_switch_57.header_switch = long_deng_shan_switch_45.id
        long_deng_shan_switch_57.positive_switch = False
        long_deng_shan_switch_57.negative_switch = False
        long_deng_shan_switch_57.x_pos = 360
        long_deng_shan_switch_57.y_pos = 582

        long_deng_shan_switch_59.positive_rail = long_deng_shan_rail_17AG.id
        long_deng_shan_switch_59.negative_rail = long_deng_shan_rail_18AG.id
        long_deng_shan_switch_59.header_rail = False
        long_deng_shan_switch_59.header_switch = long_deng_shan_switch_55.id
        long_deng_shan_switch_59.positive_switch = False
        long_deng_shan_switch_59.negative_switch = False
        long_deng_shan_switch_59.x_pos = 360
        long_deng_shan_switch_59.y_pos = 582

        long_deng_shan_switch_61.positive_rail = False
        long_deng_shan_switch_61.negative_rail = False
        long_deng_shan_switch_61.header_rail = False
        long_deng_shan_switch_61.header_switch = long_deng_shan_switch_19.id
        long_deng_shan_switch_61.positive_switch = long_deng_shan_switch_63.id
        long_deng_shan_switch_61.negative_switch = long_deng_shan_switch_73.id
        long_deng_shan_switch_61.x_pos = 360
        long_deng_shan_switch_61.y_pos = 582

        long_deng_shan_switch_63.positive_rail = False
        long_deng_shan_switch_63.negative_rail = False
        long_deng_shan_switch_63.header_rail = False
        long_deng_shan_switch_63.header_switch = long_deng_shan_switch_61.id
        long_deng_shan_switch_63.positive_switch = long_deng_shan_switch_65.id
        long_deng_shan_switch_63.negative_switch = long_deng_shan_switch_71.id
        long_deng_shan_switch_63.x_pos = 360
        long_deng_shan_switch_63.y_pos = 582

        long_deng_shan_switch_65.positive_rail = False
        long_deng_shan_switch_65.negative_rail = False
        long_deng_shan_switch_65.header_rail = False
        long_deng_shan_switch_65.header_switch = long_deng_shan_switch_63.id
        long_deng_shan_switch_65.positive_switch = long_deng_shan_switch_67.id
        long_deng_shan_switch_65.negative_switch = long_deng_shan_switch_69.id
        long_deng_shan_switch_65.x_pos = 360
        long_deng_shan_switch_65.y_pos = 582

        long_deng_shan_switch_67.positive_rail = long_deng_shan_rail_19AG.id
        long_deng_shan_switch_67.negative_rail = long_deng_shan_rail_20AG.id
        long_deng_shan_switch_67.header_rail = False
        long_deng_shan_switch_67.header_switch = long_deng_shan_switch_65.id
        long_deng_shan_switch_67.positive_switch = False
        long_deng_shan_switch_67.negative_switch = False
        long_deng_shan_switch_67.x_pos = 360
        long_deng_shan_switch_67.y_pos = 582

        long_deng_shan_switch_69.positive_rail = long_deng_shan_rail_21AG.id
        long_deng_shan_switch_69.negative_rail = long_deng_shan_rail_22AG.id
        long_deng_shan_switch_69.header_rail = False
        long_deng_shan_switch_69.header_switch = long_deng_shan_switch_65.id
        long_deng_shan_switch_69.positive_switch = False
        long_deng_shan_switch_69.negative_switch = False
        long_deng_shan_switch_69.x_pos = 360
        long_deng_shan_switch_69.y_pos = 582

        long_deng_shan_switch_71.positive_rail = long_deng_shan_rail_23AG.id
        long_deng_shan_switch_71.negative_rail = long_deng_shan_rail_24AG.id
        long_deng_shan_switch_71.header_rail = False
        long_deng_shan_switch_71.header_switch = long_deng_shan_switch_63.id
        long_deng_shan_switch_71.positive_switch = False
        long_deng_shan_switch_71.negative_switch = False
        long_deng_shan_switch_71.x_pos = 360
        long_deng_shan_switch_71.y_pos = 582

        long_deng_shan_switch_73.positive_rail = False
        long_deng_shan_switch_73.negative_rail = False
        long_deng_shan_switch_73.header_rail = False
        long_deng_shan_switch_73.header_switch = long_deng_shan_switch_61.id
        long_deng_shan_switch_73.positive_switch = long_deng_shan_switch_77.id
        long_deng_shan_switch_73.negative_switch = long_deng_shan_switch_75.id
        long_deng_shan_switch_73.x_pos = 360
        long_deng_shan_switch_73.y_pos = 582

        long_deng_shan_switch_75.positive_rail = False
        long_deng_shan_switch_75.negative_rail = False
        long_deng_shan_switch_75.header_rail = False
        long_deng_shan_switch_75.header_switch = long_deng_shan_switch_69.id
        long_deng_shan_switch_75.positive_switch = False
        long_deng_shan_switch_75.negative_switch = long_deng_shan_switch_73.id
        long_deng_shan_switch_75.x_pos = 360
        long_deng_shan_switch_75.y_pos = 582

        long_deng_shan_switch_77.positive_rail = long_deng_shan_rail_25AG.id
        long_deng_shan_switch_77.negative_rail = long_deng_shan_rail_26AG.id
        long_deng_shan_switch_77.header_rail = False
        long_deng_shan_switch_77.header_switch = long_deng_shan_switch_69.id
        long_deng_shan_switch_77.positive_switch = False
        long_deng_shan_switch_77.negative_switch = False
        long_deng_shan_switch_77.x_pos = 360
        long_deng_shan_switch_77.y_pos = 582

        long_deng_shan_switch_79.positive_rail = long_deng_shan_rail_27AG.id
        long_deng_shan_switch_79.negative_rail = False
        long_deng_shan_switch_79.header_rail = False
        long_deng_shan_switch_79.header_switch = long_deng_shan_switch_75.id
        long_deng_shan_switch_79.positive_switch = False
        long_deng_shan_switch_79.negative_switch = long_deng_shan_switch_81.id
        long_deng_shan_switch_79.x_pos = 360
        long_deng_shan_switch_79.y_pos = 582

        long_deng_shan_switch_81.positive_rail = long_deng_shan_rail_28AG.id
        long_deng_shan_switch_81.negative_rail = long_deng_shan_rail_29G.id
        long_deng_shan_switch_81.header_rail = False
        long_deng_shan_switch_81.header_switch = long_deng_shan_switch_79.id
        long_deng_shan_switch_81.positive_switch = False
        long_deng_shan_switch_81.negative_switch = False
        long_deng_shan_switch_81.x_pos = 360
        long_deng_shan_switch_81.y_pos = 582

        long_deng_shan_rail_7AG.left_rail_id = long_deng_shan_rail_7BG.id
        long_deng_shan_rail_7AG.right_rail_id = False
        long_deng_shan_rail_7AG.left_switch_id = False
        long_deng_shan_rail_7AG.right_switch_id = long_deng_shan_switch_43.id
        long_deng_shan_rail_7AG.left_switch_position = False
        long_deng_shan_rail_7AG.right_switch_position = 'negative'
        long_deng_shan_rail_7AG.x_pos = 1396
        long_deng_shan_rail_7AG.y_pos = 253

        long_deng_shan_rail_7BG.left_rail_id = False
        long_deng_shan_rail_7BG.right_rail_id = long_deng_shan_rail_7AG.id
        long_deng_shan_rail_7BG.left_switch_id = False
        long_deng_shan_rail_7BG.right_switch_id = False
        long_deng_shan_rail_7BG.left_switch_position = False
        long_deng_shan_rail_7BG.right_switch_position = False
        long_deng_shan_rail_7BG.x_pos = 1396
        long_deng_shan_rail_7BG.y_pos = 253

        long_deng_shan_rail_8BG.left_rail_id = False
        long_deng_shan_rail_8BG.right_rail_id = long_deng_shan_rail_8AG.id
        long_deng_shan_rail_8BG.left_switch_id = False
        long_deng_shan_rail_8BG.right_switch_id = False
        long_deng_shan_rail_8BG.left_switch_position = False
        long_deng_shan_rail_8BG.right_switch_position = False
        long_deng_shan_rail_8BG.x_pos = 1396
        long_deng_shan_rail_8BG.y_pos = 253

        long_deng_shan_rail_9BG.left_rail_id = False
        long_deng_shan_rail_9BG.right_rail_id = long_deng_shan_rail_9AG.id
        long_deng_shan_rail_9BG.left_switch_id = False
        long_deng_shan_rail_9BG.right_switch_id = False
        long_deng_shan_rail_9BG.left_switch_position = False
        long_deng_shan_rail_9BG.right_switch_position = False
        long_deng_shan_rail_9BG.x_pos = 1396
        long_deng_shan_rail_9BG.y_pos = 253

        long_deng_shan_rail_10BG.left_rail_id = False
        long_deng_shan_rail_10BG.right_rail_id = long_deng_shan_rail_10AG.id
        long_deng_shan_rail_10BG.left_switch_id = False
        long_deng_shan_rail_10BG.right_switch_id = False
        long_deng_shan_rail_10BG.left_switch_position = False
        long_deng_shan_rail_10BG.right_switch_position = False
        long_deng_shan_rail_10BG.x_pos = 1396
        long_deng_shan_rail_10BG.y_pos = 253

        long_deng_shan_rail_11BG.left_rail_id = False
        long_deng_shan_rail_11BG.right_rail_id = long_deng_shan_rail_11AG.id
        long_deng_shan_rail_11BG.left_switch_id = False
        long_deng_shan_rail_11BG.right_switch_id = False
        long_deng_shan_rail_11BG.left_switch_position = False
        long_deng_shan_rail_11BG.right_switch_position = False
        long_deng_shan_rail_11BG.x_pos = 1396
        long_deng_shan_rail_11BG.y_pos = 253

        long_deng_shan_rail_12BG.left_rail_id = False
        long_deng_shan_rail_12BG.right_rail_id = long_deng_shan_rail_12AG.id
        long_deng_shan_rail_12BG.left_switch_id = False
        long_deng_shan_rail_12BG.right_switch_id = False
        long_deng_shan_rail_12BG.left_switch_position = False
        long_deng_shan_rail_12BG.right_switch_position = False
        long_deng_shan_rail_12BG.x_pos = 1396
        long_deng_shan_rail_12BG.y_pos = 253

        long_deng_shan_rail_13BG.left_rail_id = False
        long_deng_shan_rail_13BG.right_rail_id = long_deng_shan_rail_13AG.id
        long_deng_shan_rail_13BG.left_switch_id = False
        long_deng_shan_rail_13BG.right_switch_id = False
        long_deng_shan_rail_13BG.left_switch_position = False
        long_deng_shan_rail_13BG.right_switch_position = False
        long_deng_shan_rail_13BG.x_pos = 1396
        long_deng_shan_rail_13BG.y_pos = 253

        long_deng_shan_rail_14BG.left_rail_id = False
        long_deng_shan_rail_14BG.right_rail_id = long_deng_shan_rail_14AG.id
        long_deng_shan_rail_14BG.left_switch_id = False
        long_deng_shan_rail_14BG.right_switch_id = False
        long_deng_shan_rail_14BG.left_switch_position = False
        long_deng_shan_rail_14BG.right_switch_position = False
        long_deng_shan_rail_14BG.x_pos = 1396
        long_deng_shan_rail_14BG.y_pos = 253

        long_deng_shan_rail_15BG.left_rail_id = False
        long_deng_shan_rail_15BG.right_rail_id = long_deng_shan_rail_15AG.id
        long_deng_shan_rail_15BG.left_switch_id = False
        long_deng_shan_rail_15BG.right_switch_id = False
        long_deng_shan_rail_15BG.left_switch_position = False
        long_deng_shan_rail_15BG.right_switch_position = False
        long_deng_shan_rail_15BG.x_pos = 1396
        long_deng_shan_rail_15BG.y_pos = 253

        long_deng_shan_rail_16BG.left_rail_id = False
        long_deng_shan_rail_16BG.right_rail_id = long_deng_shan_rail_16AG.id
        long_deng_shan_rail_16BG.left_switch_id = False
        long_deng_shan_rail_16BG.right_switch_id = False
        long_deng_shan_rail_16BG.left_switch_position = False
        long_deng_shan_rail_16BG.right_switch_position = False
        long_deng_shan_rail_16BG.x_pos = 1396
        long_deng_shan_rail_16BG.y_pos = 253

        long_deng_shan_rail_17BG.left_rail_id = False
        long_deng_shan_rail_17BG.right_rail_id = long_deng_shan_rail_17AG.id
        long_deng_shan_rail_17BG.left_switch_id = False
        long_deng_shan_rail_17BG.right_switch_id = False
        long_deng_shan_rail_17BG.left_switch_position = False
        long_deng_shan_rail_17BG.right_switch_position = False
        long_deng_shan_rail_17BG.x_pos = 1396
        long_deng_shan_rail_17BG.y_pos = 253

        long_deng_shan_rail_18BG.left_rail_id = False
        long_deng_shan_rail_18BG.right_rail_id = long_deng_shan_rail_18AG.id
        long_deng_shan_rail_18BG.left_switch_id = False
        long_deng_shan_rail_18BG.right_switch_id = False
        long_deng_shan_rail_18BG.left_switch_position = False
        long_deng_shan_rail_18BG.right_switch_position = False
        long_deng_shan_rail_18BG.x_pos = 1396
        long_deng_shan_rail_18BG.y_pos = 253

        long_deng_shan_rail_19BG.left_rail_id = False
        long_deng_shan_rail_19BG.right_rail_id = long_deng_shan_rail_19AG.id
        long_deng_shan_rail_19BG.left_switch_id = False
        long_deng_shan_rail_19BG.right_switch_id = False
        long_deng_shan_rail_19BG.left_switch_position = False
        long_deng_shan_rail_19BG.right_switch_position = False
        long_deng_shan_rail_19BG.x_pos = 1396
        long_deng_shan_rail_19BG.y_pos = 253

        long_deng_shan_rail_20BG.left_rail_id = False
        long_deng_shan_rail_20BG.right_rail_id = long_deng_shan_rail_20AG.id
        long_deng_shan_rail_20BG.left_switch_id = False
        long_deng_shan_rail_20BG.right_switch_id = False
        long_deng_shan_rail_20BG.left_switch_position = False
        long_deng_shan_rail_20BG.right_switch_position = False
        long_deng_shan_rail_20BG.x_pos = 1396
        long_deng_shan_rail_20BG.y_pos = 253

        long_deng_shan_rail_21BG.left_rail_id = False
        long_deng_shan_rail_21BG.right_rail_id = long_deng_shan_rail_21AG.id
        long_deng_shan_rail_21BG.left_switch_id = False
        long_deng_shan_rail_21BG.right_switch_id = False
        long_deng_shan_rail_21BG.left_switch_position = False
        long_deng_shan_rail_21BG.right_switch_position = False
        long_deng_shan_rail_21BG.x_pos = 1396
        long_deng_shan_rail_21BG.y_pos = 253

        long_deng_shan_rail_22BG.left_rail_id = False
        long_deng_shan_rail_22BG.right_rail_id = long_deng_shan_rail_22AG.id
        long_deng_shan_rail_22BG.left_switch_id = False
        long_deng_shan_rail_22BG.right_switch_id = False
        long_deng_shan_rail_22BG.left_switch_position = False
        long_deng_shan_rail_22BG.right_switch_position = False
        long_deng_shan_rail_22BG.x_pos = 1396
        long_deng_shan_rail_22BG.y_pos = 253

        long_deng_shan_rail_23BG.left_rail_id = False
        long_deng_shan_rail_23BG.right_rail_id = long_deng_shan_rail_23AG.id
        long_deng_shan_rail_23BG.left_switch_id = False
        long_deng_shan_rail_23BG.right_switch_id = False
        long_deng_shan_rail_23BG.left_switch_position = False
        long_deng_shan_rail_23BG.right_switch_position = False
        long_deng_shan_rail_23BG.x_pos = 1396
        long_deng_shan_rail_23BG.y_pos = 253

        long_deng_shan_rail_24BG.left_rail_id = False
        long_deng_shan_rail_24BG.right_rail_id = long_deng_shan_rail_24AG.id
        long_deng_shan_rail_24BG.left_switch_id = False
        long_deng_shan_rail_24BG.right_switch_id = False
        long_deng_shan_rail_24BG.left_switch_position = False
        long_deng_shan_rail_24BG.right_switch_position = False
        long_deng_shan_rail_24BG.x_pos = 1396
        long_deng_shan_rail_24BG.y_pos = 253

        long_deng_shan_rail_25BG.left_rail_id = False
        long_deng_shan_rail_25BG.right_rail_id = long_deng_shan_rail_25AG.id
        long_deng_shan_rail_25BG.left_switch_id = False
        long_deng_shan_rail_25BG.right_switch_id = False
        long_deng_shan_rail_25BG.left_switch_position = False
        long_deng_shan_rail_25BG.right_switch_position = False
        long_deng_shan_rail_25BG.x_pos = 1396
        long_deng_shan_rail_25BG.y_pos = 253

        long_deng_shan_rail_26BG.left_rail_id = False
        long_deng_shan_rail_26BG.right_rail_id = long_deng_shan_rail_26AG.id
        long_deng_shan_rail_26BG.left_switch_id = False
        long_deng_shan_rail_26BG.right_switch_id = False
        long_deng_shan_rail_26BG.left_switch_position = False
        long_deng_shan_rail_26BG.right_switch_position = False
        long_deng_shan_rail_26BG.x_pos = 1396
        long_deng_shan_rail_26BG.y_pos = 253

        long_deng_shan_rail_27BG.left_rail_id = False
        long_deng_shan_rail_27BG.right_rail_id = long_deng_shan_rail_27AG.id
        long_deng_shan_rail_27BG.left_switch_id = False
        long_deng_shan_rail_27BG.right_switch_id = False
        long_deng_shan_rail_27BG.left_switch_position = False
        long_deng_shan_rail_27BG.right_switch_position = False
        long_deng_shan_rail_27BG.x_pos = 1396
        long_deng_shan_rail_27BG.y_pos = 253

        long_deng_shan_rail_29G.left_rail_id = False
        long_deng_shan_rail_29G.right_rail_id = False
        long_deng_shan_rail_29G.left_switch_id = False
        long_deng_shan_rail_29G.right_switch_id = long_deng_shan_switch_81.id
        long_deng_shan_rail_29G.left_switch_position = False
        long_deng_shan_rail_29G.right_switch_position = 'negative'
        long_deng_shan_rail_29G.x_pos = 1396
        long_deng_shan_rail_29G.y_pos = 253

        long_deng_shan_rail_28AG.left_rail_id = long_deng_shan_rail_28BG.id
        long_deng_shan_rail_28AG.right_rail_id = False
        long_deng_shan_rail_28AG.left_switch_id = False
        long_deng_shan_rail_28AG.right_switch_id = long_deng_shan_switch_81.id
        long_deng_shan_rail_28AG.left_switch_position = False
        long_deng_shan_rail_28AG.right_switch_position = 'positive'
        long_deng_shan_rail_28AG.x_pos = 1396
        long_deng_shan_rail_28AG.y_pos = 253

        long_deng_shan_rail_27AG.left_rail_id = long_deng_shan_rail_27BG.id
        long_deng_shan_rail_27AG.right_rail_id = False
        long_deng_shan_rail_27AG.left_switch_id = False
        long_deng_shan_rail_27AG.right_switch_id = long_deng_shan_switch_79.id
        long_deng_shan_rail_27AG.left_switch_position = False
        long_deng_shan_rail_27AG.right_switch_position = 'positive'
        long_deng_shan_rail_27AG.x_pos = 1396
        long_deng_shan_rail_27AG.y_pos = 253

        long_deng_shan_rail_26AG.left_rail_id = long_deng_shan_rail_26BG.id
        long_deng_shan_rail_26AG.right_rail_id = False
        long_deng_shan_rail_26AG.left_switch_id = False
        long_deng_shan_rail_26AG.right_switch_id = long_deng_shan_switch_77.id
        long_deng_shan_rail_26AG.left_switch_position = False
        long_deng_shan_rail_26AG.right_switch_position = 'negative'
        long_deng_shan_rail_26AG.x_pos = 1396
        long_deng_shan_rail_26AG.y_pos = 253

        long_deng_shan_rail_25AG.left_rail_id = long_deng_shan_rail_25BG.id
        long_deng_shan_rail_25AG.right_rail_id = False
        long_deng_shan_rail_25AG.left_switch_id = False
        long_deng_shan_rail_25AG.right_switch_id = long_deng_shan_switch_77.id
        long_deng_shan_rail_25AG.left_switch_position = False
        long_deng_shan_rail_25AG.right_switch_position = 'positive'
        long_deng_shan_rail_25AG.x_pos = 1396
        long_deng_shan_rail_25AG.y_pos = 253

        long_deng_shan_rail_24AG.left_rail_id = long_deng_shan_rail_24BG.id
        long_deng_shan_rail_24AG.right_rail_id = False
        long_deng_shan_rail_24AG.left_switch_id = False
        long_deng_shan_rail_24AG.right_switch_id = long_deng_shan_switch_71.id
        long_deng_shan_rail_24AG.left_switch_position = False
        long_deng_shan_rail_24AG.right_switch_position = 'negative'
        long_deng_shan_rail_24AG.x_pos = 1396
        long_deng_shan_rail_24AG.y_pos = 253

        long_deng_shan_rail_23AG.left_rail_id = long_deng_shan_rail_23BG.id
        long_deng_shan_rail_23AG.right_rail_id = False
        long_deng_shan_rail_23AG.left_switch_id = False
        long_deng_shan_rail_23AG.right_switch_id = long_deng_shan_switch_71.id
        long_deng_shan_rail_23AG.left_switch_position = False
        long_deng_shan_rail_23AG.right_switch_position = 'positive'
        long_deng_shan_rail_23AG.x_pos = 1396
        long_deng_shan_rail_23AG.y_pos = 253

        long_deng_shan_rail_22AG.left_rail_id = long_deng_shan_rail_22BG.id
        long_deng_shan_rail_22AG.right_rail_id = False
        long_deng_shan_rail_22AG.left_switch_id = False
        long_deng_shan_rail_22AG.right_switch_id = long_deng_shan_switch_69.id
        long_deng_shan_rail_22AG.left_switch_position = False
        long_deng_shan_rail_22AG.right_switch_position = 'negative'
        long_deng_shan_rail_22AG.x_pos = 1396
        long_deng_shan_rail_22AG.y_pos = 253

        long_deng_shan_rail_21AG.left_rail_id = long_deng_shan_rail_21BG.id
        long_deng_shan_rail_21AG.right_rail_id = False
        long_deng_shan_rail_21AG.left_switch_id = False
        long_deng_shan_rail_21AG.right_switch_id = long_deng_shan_switch_69.id
        long_deng_shan_rail_21AG.left_switch_position = False
        long_deng_shan_rail_21AG.right_switch_position = 'positive'
        long_deng_shan_rail_21AG.x_pos = 1396
        long_deng_shan_rail_21AG.y_pos = 253

        long_deng_shan_rail_20AG.left_rail_id = long_deng_shan_rail_20BG.id
        long_deng_shan_rail_20AG.right_rail_id = False
        long_deng_shan_rail_20AG.left_switch_id = False
        long_deng_shan_rail_20AG.right_switch_id = long_deng_shan_switch_67.id
        long_deng_shan_rail_20AG.left_switch_position = False
        long_deng_shan_rail_20AG.right_switch_position = 'negative'
        long_deng_shan_rail_20AG.x_pos = 1396
        long_deng_shan_rail_20AG.y_pos = 253

        long_deng_shan_rail_19AG.left_rail_id = long_deng_shan_rail_19BG.id
        long_deng_shan_rail_19AG.right_rail_id = False
        long_deng_shan_rail_19AG.left_switch_id = False
        long_deng_shan_rail_19AG.right_switch_id = long_deng_shan_switch_67.id
        long_deng_shan_rail_19AG.left_switch_position = False
        long_deng_shan_rail_19AG.right_switch_position = 'positive'
        long_deng_shan_rail_19AG.x_pos = 1396
        long_deng_shan_rail_19AG.y_pos = 253

        long_deng_shan_rail_18AG.left_rail_id = long_deng_shan_rail_18BG.id
        long_deng_shan_rail_18AG.right_rail_id = False
        long_deng_shan_rail_18AG.left_switch_id = False
        long_deng_shan_rail_18AG.right_switch_id = long_deng_shan_switch_59.id
        long_deng_shan_rail_18AG.left_switch_position = False
        long_deng_shan_rail_18AG.right_switch_position = 'negative'
        long_deng_shan_rail_18AG.x_pos = 1396
        long_deng_shan_rail_18AG.y_pos = 253

        long_deng_shan_rail_17AG.left_rail_id = long_deng_shan_rail_17BG.id
        long_deng_shan_rail_17AG.right_rail_id = False
        long_deng_shan_rail_17AG.left_switch_id = False
        long_deng_shan_rail_17AG.right_switch_id = long_deng_shan_switch_59.id
        long_deng_shan_rail_17AG.left_switch_position = False
        long_deng_shan_rail_17AG.right_switch_position = 'positive'
        long_deng_shan_rail_17AG.x_pos = 1396
        long_deng_shan_rail_17AG.y_pos = 253

        long_deng_shan_rail_16AG.left_rail_id = long_deng_shan_rail_16BG.id
        long_deng_shan_rail_16AG.right_rail_id = False
        long_deng_shan_rail_16AG.left_switch_id = False
        long_deng_shan_rail_16AG.right_switch_id = long_deng_shan_switch_57.id
        long_deng_shan_rail_16AG.left_switch_position = False
        long_deng_shan_rail_16AG.right_switch_position = 'positive'
        long_deng_shan_rail_16AG.x_pos = 1396
        long_deng_shan_rail_16AG.y_pos = 253

        long_deng_shan_rail_15AG.left_rail_id = long_deng_shan_rail_15BG.id
        long_deng_shan_rail_15AG.right_rail_id = False
        long_deng_shan_rail_15AG.left_switch_id = False
        long_deng_shan_rail_15AG.right_switch_id = long_deng_shan_switch_57.id
        long_deng_shan_rail_15AG.left_switch_position = False
        long_deng_shan_rail_15AG.right_switch_position = 'negative'
        long_deng_shan_rail_15AG.x_pos = 1396
        long_deng_shan_rail_15AG.y_pos = 253

        long_deng_shan_rail_14AG.left_rail_id = long_deng_shan_rail_14BG.id
        long_deng_shan_rail_14AG.right_rail_id = False
        long_deng_shan_rail_14AG.left_switch_id = False
        long_deng_shan_rail_14AG.right_switch_id = long_deng_shan_switch_53.id
        long_deng_shan_rail_14AG.left_switch_position = False
        long_deng_shan_rail_14AG.right_switch_position = 'negative'
        long_deng_shan_rail_14AG.x_pos = 1396
        long_deng_shan_rail_14AG.y_pos = 253

        long_deng_shan_rail_13AG.left_rail_id = long_deng_shan_rail_13BG.id
        long_deng_shan_rail_13AG.right_rail_id = False
        long_deng_shan_rail_13AG.left_switch_id = False
        long_deng_shan_rail_13AG.right_switch_id = long_deng_shan_switch_53.id
        long_deng_shan_rail_13AG.left_switch_position = False
        long_deng_shan_rail_13AG.right_switch_position = 'positive'
        long_deng_shan_rail_13AG.x_pos = 1396
        long_deng_shan_rail_13AG.y_pos = 253

        long_deng_shan_rail_12AG.left_rail_id = long_deng_shan_rail_12BG.id
        long_deng_shan_rail_12AG.right_rail_id = False
        long_deng_shan_rail_12AG.left_switch_id = False
        long_deng_shan_rail_12AG.right_switch_id = long_deng_shan_switch_51.id
        long_deng_shan_rail_12AG.left_switch_position = False
        long_deng_shan_rail_12AG.right_switch_position = 'positive'
        long_deng_shan_rail_12AG.x_pos = 1396
        long_deng_shan_rail_12AG.y_pos = 253

        long_deng_shan_rail_11AG.left_rail_id = long_deng_shan_rail_11BG.id
        long_deng_shan_rail_11AG.right_rail_id = False
        long_deng_shan_rail_11AG.left_switch_id = False
        long_deng_shan_rail_11AG.right_switch_id = long_deng_shan_switch_51.id
        long_deng_shan_rail_11AG.left_switch_position = False
        long_deng_shan_rail_11AG.right_switch_position = 'negative'
        long_deng_shan_rail_11AG.x_pos = 1396
        long_deng_shan_rail_11AG.y_pos = 253

        long_deng_shan_rail_10AG.left_rail_id = long_deng_shan_rail_10BG.id
        long_deng_shan_rail_10AG.right_rail_id = False
        long_deng_shan_rail_10AG.left_switch_id = False
        long_deng_shan_rail_10AG.right_switch_id = long_deng_shan_switch_45.id
        long_deng_shan_rail_10AG.left_switch_position = False
        long_deng_shan_rail_10AG.right_switch_position = 'negative'
        long_deng_shan_rail_10AG.x_pos = 1396
        long_deng_shan_rail_10AG.y_pos = 253

        long_deng_shan_rail_9AG.left_rail_id = long_deng_shan_rail_9BG.id
        long_deng_shan_rail_9AG.right_rail_id = False
        long_deng_shan_rail_9AG.left_switch_id = False
        long_deng_shan_rail_9AG.right_switch_id = long_deng_shan_switch_45.id
        long_deng_shan_rail_9AG.left_switch_position = False
        long_deng_shan_rail_9AG.right_switch_position = 'positive'
        long_deng_shan_rail_9AG.x_pos = 1396
        long_deng_shan_rail_9AG.y_pos = 253

        long_deng_shan_rail_8AG.left_rail_id = long_deng_shan_rail_8BG.id
        long_deng_shan_rail_8AG.right_rail_id = False
        long_deng_shan_rail_8AG.left_switch_id = False
        long_deng_shan_rail_8AG.right_switch_id = long_deng_shan_switch_43.id
        long_deng_shan_rail_8AG.left_switch_position = False
        long_deng_shan_rail_8AG.right_switch_position = 'positive'
        long_deng_shan_rail_8AG.x_pos = 1396
        long_deng_shan_rail_8AG.y_pos = 253

        long_deng_shan_rail_6G.left_rail_id = False
        long_deng_shan_rail_6G.right_rail_id = False
        long_deng_shan_rail_6G.left_switch_id = False
        long_deng_shan_rail_6G.right_switch_id = long_deng_shan_switch_35.id
        long_deng_shan_rail_6G.left_switch_position = False
        long_deng_shan_rail_6G.right_switch_position = 'negative'
        long_deng_shan_rail_6G.x_pos = 1396
        long_deng_shan_rail_6G.y_pos = 253

        long_deng_shan_rail_5G.left_rail_id = False
        long_deng_shan_rail_5G.right_rail_id = False
        long_deng_shan_rail_5G.left_switch_id = False
        long_deng_shan_rail_5G.right_switch_id = long_deng_shan_switch_37.id
        long_deng_shan_rail_5G.left_switch_position = False
        long_deng_shan_rail_5G.right_switch_position = 'positive'
        long_deng_shan_rail_5G.x_pos = 1396
        long_deng_shan_rail_5G.y_pos = 253

        long_deng_shan_rail_4G.left_rail_id = False
        long_deng_shan_rail_4G.right_rail_id = False
        long_deng_shan_rail_4G.left_switch_id = False
        long_deng_shan_rail_4G.right_switch_id = long_deng_shan_switch_37.id
        long_deng_shan_rail_4G.left_switch_position = False
        long_deng_shan_rail_4G.right_switch_position = 'negative'
        long_deng_shan_rail_4G.x_pos = 1396
        long_deng_shan_rail_4G.y_pos = 253

        long_deng_shan_rail_3G.left_rail_id = False
        long_deng_shan_rail_3G.right_rail_id = False
        long_deng_shan_rail_3G.left_switch_id = False
        long_deng_shan_rail_3G.right_switch_id = long_deng_shan_switch_33.id
        long_deng_shan_rail_3G.left_switch_position = False
        long_deng_shan_rail_3G.right_switch_position = 'negative'
        long_deng_shan_rail_3G.x_pos = 1396
        long_deng_shan_rail_3G.y_pos = 253

        long_deng_shan_rail_2G.left_rail_id = False
        long_deng_shan_rail_2G.right_rail_id = False
        long_deng_shan_rail_2G.left_switch_id = False
        long_deng_shan_rail_2G.right_switch_id = long_deng_shan_switch_33.id
        long_deng_shan_rail_2G.left_switch_position = False
        long_deng_shan_rail_2G.right_switch_position = 'positive'
        long_deng_shan_rail_2G.x_pos = 1396
        long_deng_shan_rail_2G.y_pos = 253

        long_deng_shan_rail_1G.left_rail_id = False
        long_deng_shan_rail_1G.right_rail_id = False
        long_deng_shan_rail_1G.left_switch_id = False
        long_deng_shan_rail_1G.right_switch_id = long_deng_shan_switch_31.id
        long_deng_shan_rail_1G.left_switch_position = False
        long_deng_shan_rail_1G.right_switch_position = 'negative'
        long_deng_shan_rail_1G.x_pos = 1396
        long_deng_shan_rail_1G.y_pos = 253

        long_deng_shan_rail_D1G.left_rail_id = False
        long_deng_shan_rail_D1G.right_rail_id = False
        long_deng_shan_rail_D1G.left_switch_id = False
        long_deng_shan_rail_D1G.right_switch_id = long_deng_shan_switch_5.id
        long_deng_shan_rail_D1G.left_switch_position = False
        long_deng_shan_rail_D1G.right_switch_position = 'header'
        long_deng_shan_rail_D1G.x_pos = 1396
        long_deng_shan_rail_D1G.y_pos = 253

        long_deng_shan_rail_D3G.left_rail_id = False
        long_deng_shan_rail_D3G.right_rail_id = False
        long_deng_shan_rail_D3G.left_switch_id = long_deng_shan_switch_75.id
        long_deng_shan_rail_D3G.right_switch_id = False
        long_deng_shan_rail_D3G.left_switch_position = 'positive'
        long_deng_shan_rail_D3G.right_switch_position = False
        long_deng_shan_rail_D3G.x_pos = 1396
        long_deng_shan_rail_D3G.y_pos = 253

        long_deng_shan_rail_1_75WG.left_rail_id = False
        long_deng_shan_rail_1_75WG.right_rail_id = long_deng_shan_rail_D3G.id
        long_deng_shan_rail_1_75WG.left_switch_id = long_deng_shan_switch_75.id
        long_deng_shan_rail_1_75WG.right_switch_id = False
        long_deng_shan_rail_1_75WG.left_switch_position = 'positive'
        long_deng_shan_rail_1_75WG.right_switch_position = False
        long_deng_shan_rail_1_75WG.x_pos = 1396
        long_deng_shan_rail_1_75WG.y_pos = 253

        long_deng_shan_rail_T4617.left_rail_id = False
        long_deng_shan_rail_T4617.right_rail_id = long_deng_shan_rail_T4615.id
        long_deng_shan_rail_T4617.left_switch_id = long_deng_shan_switch_3.id
        long_deng_shan_rail_T4617.right_switch_id = False
        long_deng_shan_rail_T4617.left_switch_position = 'positive'
        long_deng_shan_rail_T4617.right_switch_position = False
        long_deng_shan_rail_T4617.x_pos = 1396
        long_deng_shan_rail_T4617.y_pos = 253

        long_deng_shan_rail_T4621.left_rail_id = False
        long_deng_shan_rail_T4621.right_rail_id = long_deng_shan_rail_T4623.id
        long_deng_shan_rail_T4621.left_switch_id = long_deng_shan_switch_9.id
        long_deng_shan_rail_T4621.right_switch_id = False
        long_deng_shan_rail_T4621.left_switch_position = 'header'
        long_deng_shan_rail_T4621.right_switch_position = False
        long_deng_shan_rail_T4621.x_pos = 1396
        long_deng_shan_rail_T4621.y_pos = 253

        long_deng_shan_rail_T4615.left_rail_id = long_deng_shan_rail_T4617.id
        long_deng_shan_rail_T4615.right_rail_id = False
        long_deng_shan_rail_T4615.left_switch_id = False
        long_deng_shan_rail_T4615.right_switch_id = False
        long_deng_shan_rail_T4615.left_switch_position = False
        long_deng_shan_rail_T4615.right_switch_position = False
        long_deng_shan_rail_T4615.x_pos = 1396
        long_deng_shan_rail_T4615.y_pos = 253

        long_deng_shan_rail_T4623.left_rail_id = long_deng_shan_rail_T4621.id
        long_deng_shan_rail_T4623.right_rail_id = False
        long_deng_shan_rail_T4623.left_switch_id = False
        long_deng_shan_rail_T4623.right_switch_id = False
        long_deng_shan_rail_T4623.left_switch_position = False
        long_deng_shan_rail_T4623.right_switch_position = False
        long_deng_shan_rail_T4623.x_pos = 1396
        long_deng_shan_rail_T4623.y_pos = 253

        long_deng_shan_rail_31G.left_rail_id = False
        long_deng_shan_rail_31G.right_rail_id = False
        long_deng_shan_rail_31G.left_switch_id = False
        long_deng_shan_rail_31G.right_switch_id = long_deng_shan_switch_15.id
        long_deng_shan_rail_31G.left_switch_position = False
        long_deng_shan_rail_31G.right_switch_position = 'positive'
        long_deng_shan_rail_31G.x_pos = 1396
        long_deng_shan_rail_31G.y_pos = 253

        long_deng_shan_rail_30G.left_rail_id = False
        long_deng_shan_rail_30G.right_rail_id = False
        long_deng_shan_rail_30G.left_switch_id = False
        long_deng_shan_rail_30G.right_switch_id = long_deng_shan_switch_15.id
        long_deng_shan_rail_30G.left_switch_position = False
        long_deng_shan_rail_30G.right_switch_position = 'negative'
        long_deng_shan_rail_30G.x_pos = 1396
        long_deng_shan_rail_30G.y_pos = 253
