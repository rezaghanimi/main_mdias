# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BasData(models.Model):
    _inherit = 'metro_park_base.switches'

    @api.model
    def init_huilong_switches(self):
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
        hui_long_rail_3_5DG = self.env.ref('metro_park_base.hui_long_rail_3-5DG')
        hui_long_rail_3_19WG = self.env.ref('metro_park_base.hui_long_rail_3/19WG')
        hui_long_rail_19_21WG = self.env.ref('metro_park_base.hui_long_rail_19/21WG')
        hui_long_rail_21_25DG = self.env.ref('metro_park_base.hui_long_rail_21-25DG')
        hui_long_rail_1G = self.env.ref('metro_park_base.hui_long_rail_1G')
        hui_long_rail_2G = self.env.ref('metro_park_base.hui_long_rail_2G')
        hui_long_rail_3G = self.env.ref('metro_park_base.hui_long_rail_3G')
        hui_long_rail_T6604G = self.env.ref('metro_park_base.hui_long_rail_T6604G')
        hui_long_rail_T6602G = self.env.ref('metro_park_base.hui_long_rail_T6602G')
        hui_long_rail_1_7DG = self.env.ref('metro_park_base.hui_long_rail_1-7DG')
        hui_long_rail_9_15DG = self.env.ref('metro_park_base.hui_long_rail_9-15DG')
        hui_long_rail_17_31DG = self.env.ref('metro_park_base.hui_long_rail_17-31DG')
        hui_long_rail_29_33DG = self.env.ref('metro_park_base.hui_long_rail_29-33DG')
        hui_long_rail_39DG = self.env.ref('metro_park_base.hui_long_rail_39DG')
        hui_long_rail_41DG = self.env.ref('metro_park_base.hui_long_rail_41DG')
        hui_long_rail_43_47DG = self.env.ref('metro_park_base.hui_long_rail_43-47DG')
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
        hui_long_rail_T6615G = self.env.ref('metro_park_base.hui_long_rail_T6615G')
        hui_long_rail_T6617G = self.env.ref('metro_park_base.hui_long_rail_T6617G')
        hui_long_rail_D9G = self.env.ref('metro_park_base.hui_long_rail_D9G')
        hui_long_rail_11_13DG = self.env.ref('metro_park_base.hui_long_rail_11-13DG')
        hui_long_rail_49_61DG = self.env.ref('metro_park_base.hui_long_rail_49-61DG')
        hui_long_rail_69_73DG = self.env.ref('metro_park_base.hui_long_rail_69-73DG')
        hui_long_rail_57DG = self.env.ref('metro_park_base.hui_long_rail_57DG')
        hui_long_rail_51_53DG = self.env.ref('metro_park_base.hui_long_rail_51-53DG')
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
        hui_long_rail_L0515DGJF = self.env.ref('metro_park_base.hui_long_rail_L0515DGJF')
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
        hui_long_switch_5.positive_rail = hui_long_rail_3_5DG.id
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
