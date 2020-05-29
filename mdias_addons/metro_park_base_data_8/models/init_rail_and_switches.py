
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitRailAndSwitches(models.TransientModel):
    '''
    初始化轨道和道岔信息
    '''
    _name = 'metro_park_base_data_8.init_rail_and_switches'

    name = fields.Char(string='name')

    @api.model
    def init_switches(self):
        '''
        建立板桥道岔位置关系, 一定要先把道岔和轨道建立了才行
        :return:
        '''

        yuan_hua_switch_0802 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0802')
        yuan_hua_switch_0804 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0804')
        yuan_hua_switch_0806 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0806')
        yuan_hua_switch_0808 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0808')
        yuan_hua_switch_0810 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0810')
        yuan_hua_switch_0812 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0812')
        yuan_hua_switch_0814 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0814')
        yuan_hua_switch_0816 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0816')
        yuan_hua_switch_0818 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0818')
        yuan_hua_switch_0820 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0820')
        yuan_hua_switch_0822 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0822')
        yuan_hua_switch_0824 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0824')
        yuan_hua_switch_0826 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0826')
        yuan_hua_switch_0828 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0828')
        yuan_hua_switch_0830 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0830')
        yuan_hua_switch_0832 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0832')
        yuan_hua_switch_0834 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0834')
        yuan_hua_switch_0836 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0836')
        yuan_hua_switch_0838 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0838')
        yuan_hua_switch_0840 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0840')
        yuan_hua_switch_0842 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0842')
        yuan_hua_switch_0844 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0844')
        yuan_hua_switch_0846 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0846')
        yuan_hua_switch_0848 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0848')
        yuan_hua_switch_0850 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0850')
        yuan_hua_switch_0852 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0852')
        yuan_hua_switch_0854 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0854')
        yuan_hua_switch_0856 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0856')
        yuan_hua_switch_0858 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0858')
        yuan_hua_switch_0860 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0860')
        yuan_hua_switch_0862 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0862')
        yuan_hua_switch_0864 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0864')
        yuan_hua_switch_0866 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0866')
        yuan_hua_switch_0868 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0868')
        yuan_hua_switch_0870 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0870')
        yuan_hua_switch_0872 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0872')
        yuan_hua_switch_0874 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0874')
        yuan_hua_switch_0876 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0876')
        yuan_hua_switch_0878 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0878')
        yuan_hua_switch_0880 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0880')
        yuan_hua_switch_0882 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0882')
        yuan_hua_switch_0884 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0884')
        yuan_hua_switch_0886 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0886')
        yuan_hua_switch_0888 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_switch_0888')

        # 所有的区段
        yuan_hua_rail_0810_0830WG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_0810/0830WG')
        yuan_hua_rail_0884_0886WG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_0884/0886WG')
        yuan_hua_rail_10AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_10AG')
        yuan_hua_rail_10BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_10BG')
        yuan_hua_rail_11AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_11AG')
        yuan_hua_rail_11BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_11BG')
        yuan_hua_rail_12AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_12AG')
        yuan_hua_rail_12BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_12BG')
        yuan_hua_rail_13AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_13AG')
        yuan_hua_rail_13BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_13BG')
        yuan_hua_rail_14AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_14AG')
        yuan_hua_rail_14BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_14BG')
        yuan_hua_rail_15AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_15AG')
        yuan_hua_rail_15BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_15BG')
        yuan_hua_rail_16AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_16AG')
        yuan_hua_rail_16BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_16BG')
        yuan_hua_rail_17AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_17AG')
        yuan_hua_rail_17BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_17BG')
        yuan_hua_rail_18AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_18AG')
        yuan_hua_rail_18BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_18BG')
        yuan_hua_rail_19G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_19G')
        yuan_hua_rail_1AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_1AG')
        yuan_hua_rail_1BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_1BG')
        yuan_hua_rail_1CG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_1CG')
        yuan_hua_rail_20G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_20G')
        yuan_hua_rail_21G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_21G')
        yuan_hua_rail_24G1 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_24G1')
        yuan_hua_rail_25G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_25G')
        yuan_hua_rail_26G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_26G')
        yuan_hua_rail_27G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_27G')
        yuan_hua_rail_28G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_28G')
        yuan_hua_rail_29G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_29G')
        yuan_hua_rail_2G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_2G')
        yuan_hua_rail_30G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_30G')
        yuan_hua_rail_31G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_31G')
        yuan_hua_rail_34G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_34G')
        yuan_hua_rail_3AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_3AG')
        yuan_hua_rail_3BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_3BG')
        yuan_hua_rail_4AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_4AG')
        yuan_hua_rail_4BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_4BG')
        yuan_hua_rail_5AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_5AG')
        yuan_hua_rail_5BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_5BG')
        yuan_hua_rail_6AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_6AG')
        yuan_hua_rail_6BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_6BG')
        yuan_hua_rail_7AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_7AG')
        yuan_hua_rail_7BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_7BG')
        yuan_hua_rail_8AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_8AG')
        yuan_hua_rail_8BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_8BG')
        yuan_hua_rail_9AG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_9AG')
        yuan_hua_rail_9BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_9BG')
        yuan_hua_rail_T2613 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2613')
        yuan_hua_rail_T2806 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2806')
        yuan_hua_rail_T2825 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2825')
        yuan_hua_rail_T2609 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2609')
        yuan_hua_rail_T2611 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2611')
        yuan_hua_rail_T2802 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2802')
        yuan_hua_rail_T2804 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2804')
        yuan_hua_rail_T2827 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2827')
        yuan_hua_rail_T2829 = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_T2829')
        yuan_hua_rail_22G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_22G')
        yuan_hua_rail_23G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_23G')
        yuan_hua_rail_24G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_24G')
        yuan_hua_rail_D40G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_D40G')
        yuan_hua_rail_D44G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_D44G')
        yuan_hua_rail_D46G = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_D46G')
        yuan_hua_rail_S18BG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_S18BG')
        yuan_hua_rail_0586DG = self.env.ref(
            'metro_park_base_data_8.yuan_hua_rail_0586DG')

        # 从标以仿真程序在1920 * 1280上面的位置为准
        # yuan_hua_switch_0802
        yuan_hua_switch_0802.positive_rail = False
        yuan_hua_switch_0802.negative_rail = False
        yuan_hua_switch_0802.header_rail = yuan_hua_rail_T2802.id
        yuan_hua_switch_0802.positive_switch = yuan_hua_switch_0808.id
        yuan_hua_switch_0802.negative_switch = yuan_hua_switch_0804.id
        yuan_hua_switch_0802.header_switch = False
        yuan_hua_switch_0802.x_pos = 0
        yuan_hua_switch_0802.y_pos = 0

        # yuan_hua_switch_0804
        yuan_hua_switch_0804.positive_rail = False
        yuan_hua_switch_0804.negative_rail = False
        yuan_hua_switch_0804.header_rail = False
        yuan_hua_switch_0804.positive_switch = yuan_hua_switch_0806.id
        yuan_hua_switch_0804.negative_switch = yuan_hua_switch_0802.id
        yuan_hua_switch_0804.header_switch = yuan_hua_switch_0822.id
        yuan_hua_switch_0804.x_pos = 0
        yuan_hua_switch_0804.y_pos = 0

        # yuan_hua_switch_0806
        yuan_hua_switch_0806.positive_rail = False
        yuan_hua_switch_0806.negative_rail = False
        yuan_hua_switch_0806.header_rail = yuan_hua_rail_34G.id
        yuan_hua_switch_0806.positive_switch = yuan_hua_switch_0804.id
        yuan_hua_switch_0806.negative_switch = yuan_hua_switch_0808.id
        yuan_hua_switch_0806.header_switch = False
        yuan_hua_switch_0806.x_pos = 0
        yuan_hua_switch_0806.y_pos = 0

        # yuan_hua_switch_0808
        yuan_hua_switch_0808.positive_rail = False
        yuan_hua_switch_0808.negative_rail = False
        yuan_hua_switch_0808.header_rail = False
        yuan_hua_switch_0808.positive_switch = yuan_hua_switch_0802.id
        yuan_hua_switch_0808.negative_switch = yuan_hua_switch_0806.id
        yuan_hua_switch_0808.header_switch = yuan_hua_switch_0818.id
        yuan_hua_switch_0808.x_pos = 0
        yuan_hua_switch_0808.y_pos = 0

        # yuan_hua_switch_0810
        yuan_hua_switch_0810.positive_rail = yuan_hua_rail_0810_0830WG.id
        yuan_hua_switch_0810.negative_rail = False
        yuan_hua_switch_0810.header_rail = yuan_hua_rail_T2609.id
        yuan_hua_switch_0810.positive_switch = False
        yuan_hua_switch_0810.negative_switch = yuan_hua_switch_0812.id
        yuan_hua_switch_0810.header_switch = False
        yuan_hua_switch_0810.x_pos = 0
        yuan_hua_switch_0810.y_pos = 0

        # yuan_hua_switch_0812
        yuan_hua_switch_0812.positive_rail = yuan_hua_rail_T2829.id
        yuan_hua_switch_0812.negative_rail = False
        yuan_hua_switch_0812.header_rail = False
        yuan_hua_switch_0812.positive_switch = False
        yuan_hua_switch_0812.negative_switch = yuan_hua_switch_0810.id
        yuan_hua_switch_0812.header_switch = yuan_hua_switch_0814.id
        yuan_hua_switch_0812.x_pos = 0
        yuan_hua_switch_0812.y_pos = 0

        # yuan_hua_switch_0814
        yuan_hua_switch_0814.positive_rail = False
        yuan_hua_switch_0814.negative_rail = False
        yuan_hua_switch_0814.header_rail = False
        yuan_hua_switch_0814.positive_switch = yuan_hua_switch_0820.id
        yuan_hua_switch_0814.negative_switch = yuan_hua_switch_0816.id
        yuan_hua_switch_0814.header_switch = yuan_hua_switch_0812.id
        yuan_hua_switch_0814.x_pos = 0
        yuan_hua_switch_0814.y_pos = 0

        # yuan_hua_switch_0816
        yuan_hua_switch_0816.positive_rail = False
        yuan_hua_switch_0816.negative_rail = False
        yuan_hua_switch_0816.header_rail = False
        yuan_hua_switch_0816.positive_switch = yuan_hua_switch_0818.id
        yuan_hua_switch_0816.negative_switch = yuan_hua_switch_0814.id
        yuan_hua_switch_0816.header_switch = yuan_hua_switch_0832.id
        yuan_hua_switch_0816.x_pos = 0
        yuan_hua_switch_0816.y_pos = 0

        # yuan_hua_switch_0818
        yuan_hua_switch_0818.positive_rail = False
        yuan_hua_switch_0818.negative_rail = False
        yuan_hua_switch_0818.header_rail = False
        yuan_hua_switch_0818.positive_switch = yuan_hua_switch_0816.id
        yuan_hua_switch_0818.negative_switch = yuan_hua_switch_0820.id
        yuan_hua_switch_0818.header_switch = yuan_hua_switch_0808.id
        yuan_hua_switch_0818.x_pos = 0
        yuan_hua_switch_0818.y_pos = 0

        # yuan_hua_switch_0820
        yuan_hua_switch_0820.positive_rail = False
        yuan_hua_switch_0820.negative_rail = False
        yuan_hua_switch_0820.header_rail = False
        yuan_hua_switch_0820.positive_switch = yuan_hua_switch_0814.id
        yuan_hua_switch_0820.negative_switch = yuan_hua_switch_0818.id
        yuan_hua_switch_0820.header_switch = yuan_hua_switch_0828.id
        yuan_hua_switch_0820.x_pos = 0
        yuan_hua_switch_0820.y_pos = 0

        # yuan_hua_switch_0822
        yuan_hua_switch_0822.positive_rail = False
        yuan_hua_switch_0822.negative_rail = False
        yuan_hua_switch_0822.header_rail = False
        yuan_hua_switch_0822.positive_switch = yuan_hua_switch_0824.id
        yuan_hua_switch_0822.negative_switch = yuan_hua_switch_0826.id
        yuan_hua_switch_0822.header_switch = yuan_hua_switch_0804.id
        yuan_hua_switch_0822.x_pos = 0
        yuan_hua_switch_0822.y_pos = 0

        # yuan_hua_switch_0824
        yuan_hua_switch_0824.positive_rail = False
        yuan_hua_switch_0824.negative_rail = False
        yuan_hua_switch_0824.header_rail = yuan_hua_rail_27G.id
        yuan_hua_switch_0824.positive_switch = yuan_hua_switch_0836.id
        yuan_hua_switch_0824.negative_switch = False
        yuan_hua_switch_0824.header_switch = yuan_hua_switch_0822.id
        yuan_hua_switch_0824.x_pos = 0
        yuan_hua_switch_0824.y_pos = 0

        # yuan_hua_switch_0826
        yuan_hua_switch_0826.positive_rail = False
        yuan_hua_switch_0826.negative_rail = False
        yuan_hua_switch_0826.header_rail = False
        yuan_hua_switch_0826.positive_switch = yuan_hua_switch_0838.id
        yuan_hua_switch_0826.negative_switch = yuan_hua_switch_0824.id
        yuan_hua_switch_0826.header_switch = yuan_hua_switch_0822.id
        yuan_hua_switch_0826.x_pos = 0
        yuan_hua_switch_0826.y_pos = 0

        # yuan_hua_switch_0828
        yuan_hua_switch_0828.positive_rail = False
        yuan_hua_switch_0828.negative_rail = False
        yuan_hua_switch_0828.header_rail = False
        yuan_hua_switch_0828.positive_switch = yuan_hua_switch_0848.id
        yuan_hua_switch_0828.negative_switch = yuan_hua_switch_0830.id
        yuan_hua_switch_0828.header_switch = yuan_hua_switch_0820.id
        yuan_hua_switch_0828.x_pos = 0
        yuan_hua_switch_0828.y_pos = 0

        # yuan_hua_switch_0830
        yuan_hua_switch_0830.positive_rail = yuan_hua_rail_0810_0830WG.id
        yuan_hua_switch_0830.negative_rail = False
        yuan_hua_switch_0830.header_rail = False
        yuan_hua_switch_0830.positive_switch = False
        yuan_hua_switch_0830.negative_switch = yuan_hua_switch_0828.id
        yuan_hua_switch_0830.header_switch = yuan_hua_switch_0846.id
        yuan_hua_switch_0830.x_pos = 0
        yuan_hua_switch_0830.y_pos = 0

        # yuan_hua_switch_0832
        yuan_hua_switch_0832.positive_rail = False
        yuan_hua_switch_0832.negative_rail = False
        yuan_hua_switch_0832.header_rail = False
        yuan_hua_switch_0832.positive_switch = yuan_hua_switch_0842.id
        yuan_hua_switch_0832.negative_switch = yuan_hua_switch_0834.id
        yuan_hua_switch_0832.header_switch = yuan_hua_switch_0816.id
        yuan_hua_switch_0832.x_pos = 0
        yuan_hua_switch_0832.y_pos = 0

        # yuan_hua_switch_0834
        yuan_hua_switch_0834.positive_rail = False
        yuan_hua_switch_0834.negative_rail = False
        yuan_hua_switch_0834.header_rail = False
        yuan_hua_switch_0834.positive_switch = yuan_hua_switch_0836.id
        yuan_hua_switch_0834.negative_switch = yuan_hua_switch_0832.id
        yuan_hua_switch_0834.header_switch = yuan_hua_switch_0862.id
        yuan_hua_switch_0834.x_pos = 0
        yuan_hua_switch_0834.y_pos = 0

        # yuan_hua_switch_0836
        yuan_hua_switch_0836.positive_rail = False
        yuan_hua_switch_0836.negative_rail = False
        yuan_hua_switch_0836.header_rail = False
        yuan_hua_switch_0836.positive_switch = yuan_hua_switch_0834.id
        yuan_hua_switch_0836.negative_switch = yuan_hua_switch_0844.id
        yuan_hua_switch_0836.header_switch = yuan_hua_switch_0824.id
        yuan_hua_switch_0836.x_pos = 0
        yuan_hua_switch_0836.y_pos = 0

        # yuan_hua_switch_0838
        yuan_hua_switch_0838.positive_rail = yuan_hua_rail_28G.id
        yuan_hua_switch_0838.negative_rail = yuan_hua_rail_29G.id
        yuan_hua_switch_0838.header_rail = False
        yuan_hua_switch_0838.positive_switch = False
        yuan_hua_switch_0838.negative_switch = False
        yuan_hua_switch_0838.header_switch = yuan_hua_switch_0826.id
        yuan_hua_switch_0838.x_pos = 0
        yuan_hua_switch_0838.y_pos = 0

        # yuan_hua_switch_0840
        yuan_hua_switch_0840.positive_rail = yuan_hua_rail_30G.id
        yuan_hua_switch_0840.negative_rail = yuan_hua_rail_31G.id
        yuan_hua_switch_0840.header_rail = False
        yuan_hua_switch_0840.positive_switch = False
        yuan_hua_switch_0840.negative_switch = False
        yuan_hua_switch_0840.header_switch = yuan_hua_switch_0826.id
        yuan_hua_switch_0840.x_pos = 0
        yuan_hua_switch_0840.y_pos = 0

        # yuan_hua_switch_0842
        yuan_hua_switch_0842.positive_rail = False
        yuan_hua_switch_0842.negative_rail = False
        yuan_hua_switch_0842.header_rail = False
        yuan_hua_switch_0842.positive_switch = yuan_hua_switch_0852.id
        yuan_hua_switch_0842.negative_switch = yuan_hua_switch_0860.id
        yuan_hua_switch_0842.header_switch = yuan_hua_switch_0832.id
        yuan_hua_switch_0842.x_pos = 0
        yuan_hua_switch_0842.y_pos = 0

        # yuan_hua_switch_0844
        yuan_hua_switch_0844.positive_rail = yuan_hua_rail_24G1.id
        yuan_hua_switch_0844.negative_rail = yuan_hua_rail_26G.id
        yuan_hua_switch_0844.header_rail = False
        yuan_hua_switch_0844.positive_switch = False
        yuan_hua_switch_0844.negative_switch = False
        yuan_hua_switch_0844.header_switch = yuan_hua_switch_0836.id
        yuan_hua_switch_0844.x_pos = 0
        yuan_hua_switch_0844.y_pos = 0

        # yuan_hua_switch_0846
        yuan_hua_switch_0846.positive_rail = False
        yuan_hua_switch_0846.negative_rail = False
        yuan_hua_switch_0846.header_rail = False
        yuan_hua_switch_0846.positive_switch = yuan_hua_switch_0866.id
        yuan_hua_switch_0846.negative_switch = yuan_hua_switch_0850.id
        yuan_hua_switch_0846.header_switch = yuan_hua_switch_0830.id
        yuan_hua_switch_0846.x_pos = 0
        yuan_hua_switch_0846.y_pos = 0

        # yuan_hua_switch_0848
        yuan_hua_switch_0848.positive_rail = False
        yuan_hua_switch_0848.negative_rail = False
        yuan_hua_switch_0848.header_rail = False
        yuan_hua_switch_0848.positive_switch = yuan_hua_switch_0854.id
        yuan_hua_switch_0848.negative_switch = yuan_hua_switch_0856.id
        yuan_hua_switch_0848.header_switch = yuan_hua_switch_0828.id
        yuan_hua_switch_0848.x_pos = 0
        yuan_hua_switch_0848.y_pos = 0

        # yuan_hua_switch_0850
        yuan_hua_switch_0850.positive_rail = False
        yuan_hua_switch_0850.negative_rail = yuan_hua_rail_25G.id
        yuan_hua_switch_0850.header_rail = False
        yuan_hua_switch_0850.positive_switch = yuan_hua_switch_0864.id
        yuan_hua_switch_0850.negative_switch = False
        yuan_hua_switch_0850.header_switch = yuan_hua_switch_0846.id
        yuan_hua_switch_0850.x_pos = 0
        yuan_hua_switch_0850.y_pos = 0

        # yuan_hua_switch_0852
        yuan_hua_switch_0852.positive_rail = False
        yuan_hua_switch_0852.negative_rail = False
        yuan_hua_switch_0852.header_rail = False
        yuan_hua_switch_0852.positive_switch = yuan_hua_switch_0874.id
        yuan_hua_switch_0852.negative_switch = yuan_hua_switch_0858.id
        yuan_hua_switch_0852.header_switch = yuan_hua_switch_0842.id
        yuan_hua_switch_0852.x_pos = 0
        yuan_hua_switch_0852.y_pos = 0

        # yuan_hua_switch_0854
        yuan_hua_switch_0854.positive_rail = False
        yuan_hua_switch_0854.negative_rail = yuan_hua_rail_6AG.id
        yuan_hua_switch_0854.header_rail = False
        yuan_hua_switch_0854.positive_switch = yuan_hua_switch_0868.id
        yuan_hua_switch_0854.negative_switch = False
        yuan_hua_switch_0854.header_switch = yuan_hua_switch_0848.id
        yuan_hua_switch_0854.x_pos = 0
        yuan_hua_switch_0854.y_pos = 0

        # yuan_hua_switch_0856
        yuan_hua_switch_0856.positive_rail = False
        yuan_hua_switch_0856.negative_rail = False
        yuan_hua_switch_0856.header_rail = False
        yuan_hua_switch_0856.positive_switch = yuan_hua_switch_0872.id
        yuan_hua_switch_0856.negative_switch = yuan_hua_switch_0870.id
        yuan_hua_switch_0856.header_switch = yuan_hua_switch_0848.id
        yuan_hua_switch_0856.x_pos = 0
        yuan_hua_switch_0856.y_pos = 0

        # yuan_hua_switch_0858
        yuan_hua_switch_0858.positive_rail = False
        yuan_hua_switch_0858.negative_rail = yuan_hua_rail_18AG.id
        yuan_hua_switch_0858.header_rail = False
        yuan_hua_switch_0858.positive_switch = yuan_hua_switch_0876.id
        yuan_hua_switch_0858.negative_switch = False
        yuan_hua_switch_0858.header_switch = yuan_hua_switch_0852.id
        yuan_hua_switch_0858.x_pos = 0
        yuan_hua_switch_0858.y_pos = 0

        # yuan_hua_switch_0860
        yuan_hua_switch_0860.positive_rail = yuan_hua_rail_19G.id
        yuan_hua_switch_0860.negative_rail = False
        yuan_hua_switch_0860.header_rail = False
        yuan_hua_switch_0860.positive_switch = False
        yuan_hua_switch_0860.negative_switch = yuan_hua_switch_0878.id
        yuan_hua_switch_0860.header_switch = yuan_hua_switch_0842.id
        yuan_hua_switch_0860.x_pos = 0
        yuan_hua_switch_0860.y_pos = 0

        # yuan_hua_switch_0862
        yuan_hua_switch_0862.positive_rail = yuan_hua_rail_22G.id
        yuan_hua_switch_0862.negative_rail = yuan_hua_rail_23G.id
        yuan_hua_switch_0862.header_rail = False
        yuan_hua_switch_0862.positive_switch = False
        yuan_hua_switch_0862.negative_switch = False
        yuan_hua_switch_0862.header_switch = yuan_hua_switch_0834.id
        yuan_hua_switch_0862.x_pos = 0
        yuan_hua_switch_0862.y_pos = 0

        # yuan_hua_switch_0864
        yuan_hua_switch_0864.positive_rail = yuan_hua_rail_2G.id
        yuan_hua_switch_0864.negative_rail = yuan_hua_rail_1AG.id
        yuan_hua_switch_0864.header_rail = False
        yuan_hua_switch_0864.positive_switch = False
        yuan_hua_switch_0864.negative_switch = False
        yuan_hua_switch_0864.header_switch = yuan_hua_switch_0850.id
        yuan_hua_switch_0864.x_pos = 0
        yuan_hua_switch_0864.y_pos = 0

        # yuan_hua_switch_0866
        yuan_hua_switch_0866.positive_rail = yuan_hua_rail_4AG.id
        yuan_hua_switch_0866.negative_rail = yuan_hua_rail_3AG.id
        yuan_hua_switch_0866.header_rail = False
        yuan_hua_switch_0866.positive_switch = False
        yuan_hua_switch_0866.negative_switch = False
        yuan_hua_switch_0866.header_switch = yuan_hua_switch_0846.id
        yuan_hua_switch_0866.x_pos = 0
        yuan_hua_switch_0866.y_pos = 0

        # yuan_hua_switch_0868
        yuan_hua_switch_0868.positive_rail = yuan_hua_rail_7AG.id
        yuan_hua_switch_0868.negative_rail = yuan_hua_rail_6AG.id
        yuan_hua_switch_0868.header_rail = False
        yuan_hua_switch_0868.positive_switch = False
        yuan_hua_switch_0868.negative_switch = False
        yuan_hua_switch_0868.header_switch = yuan_hua_switch_0854.id
        yuan_hua_switch_0868.x_pos = 0
        yuan_hua_switch_0868.y_pos = 0

        # yuan_hua_switch_0870
        yuan_hua_switch_0870.positive_rail = yuan_hua_rail_9AG.id
        yuan_hua_switch_0870.negative_rail = yuan_hua_rail_8AG.id
        yuan_hua_switch_0870.header_rail = False
        yuan_hua_switch_0870.positive_switch = False
        yuan_hua_switch_0870.negative_switch = False
        yuan_hua_switch_0870.header_switch = yuan_hua_switch_0856.id
        yuan_hua_switch_0870.x_pos = 0
        yuan_hua_switch_0870.y_pos = 0

        # yuan_hua_switch_0872
        yuan_hua_switch_0872.positive_rail = False
        yuan_hua_switch_0872.negative_rail = yuan_hua_rail_10AG.id
        yuan_hua_switch_0872.header_rail = False
        yuan_hua_switch_0872.positive_switch = yuan_hua_switch_0880.id
        yuan_hua_switch_0872.negative_switch = False
        yuan_hua_switch_0872.header_switch = yuan_hua_switch_0856.id
        yuan_hua_switch_0872.x_pos = 0
        yuan_hua_switch_0872.y_pos = 0

        # yuan_hua_switch_0874
        yuan_hua_switch_0874.positive_rail = False
        yuan_hua_switch_0874.negative_rail = yuan_hua_rail_15AG.id
        yuan_hua_switch_0874.header_rail = False
        yuan_hua_switch_0874.positive_switch = yuan_hua_switch_0882.id
        yuan_hua_switch_0874.negative_switch = False
        yuan_hua_switch_0874.header_switch = yuan_hua_switch_0874.id
        yuan_hua_switch_0874.x_pos = 0
        yuan_hua_switch_0874.y_pos = 0

        # yuan_hua_switch_0876
        yuan_hua_switch_0876.positive_rail = yuan_hua_rail_16AG.id
        yuan_hua_switch_0876.negative_rail = yuan_hua_rail_17AG.id
        yuan_hua_switch_0876.header_rail = False
        yuan_hua_switch_0876.positive_switch = False
        yuan_hua_switch_0876.negative_switch = False
        yuan_hua_switch_0876.header_switch = yuan_hua_switch_0858.id
        yuan_hua_switch_0876.x_pos = 0
        yuan_hua_switch_0876.y_pos = 0

        # yuan_hua_switch_0878
        yuan_hua_switch_0878.positive_rail = yuan_hua_rail_21G.id
        yuan_hua_switch_0878.negative_rail = yuan_hua_rail_20G.id
        yuan_hua_switch_0878.header_rail = False
        yuan_hua_switch_0878.positive_switch = False
        yuan_hua_switch_0878.negative_switch = False
        yuan_hua_switch_0878.header_switch = yuan_hua_switch_0860.id
        yuan_hua_switch_0878.x_pos = 0
        yuan_hua_switch_0878.y_pos = 0

        # yuan_hua_switch_0880
        yuan_hua_switch_0880.positive_rail = yuan_hua_rail_12AG.id
        yuan_hua_switch_0880.negative_rail = yuan_hua_rail_11AG.id
        yuan_hua_switch_0880.header_rail = False
        yuan_hua_switch_0880.positive_switch = False
        yuan_hua_switch_0880.negative_switch = False
        yuan_hua_switch_0880.header_switch = yuan_hua_switch_0872.id
        yuan_hua_switch_0880.x_pos = 0
        yuan_hua_switch_0880.y_pos = 0

        # yuan_hua_switch_0882
        yuan_hua_switch_0882.positive_rail = yuan_hua_rail_13AG.id
        yuan_hua_switch_0882.negative_rail = yuan_hua_rail_14AG.id
        yuan_hua_switch_0882.header_rail = False
        yuan_hua_switch_0882.positive_switch = False
        yuan_hua_switch_0882.negative_switch = False
        yuan_hua_switch_0882.header_switch = yuan_hua_switch_0874.id
        yuan_hua_switch_0882.x_pos = 0
        yuan_hua_switch_0882.y_pos = 0

        # yuan_hua_switch_0884
        yuan_hua_switch_0884.positive_rail = yuan_hua_rail_S18BG.id
        yuan_hua_switch_0884.negative_rail = yuan_hua_rail_34G.id
        yuan_hua_switch_0884.header_rail = yuan_hua_rail_0884_0886WG.id
        yuan_hua_switch_0884.positive_switch = False
        yuan_hua_switch_0884.negative_switch = False
        yuan_hua_switch_0884.header_switch = False
        yuan_hua_switch_0884.x_pos = 0
        yuan_hua_switch_0884.y_pos = 0

        # yuan_hua_switch_0886
        yuan_hua_switch_0886.positive_rail = yuan_hua_rail_0884_0886WG.id
        yuan_hua_switch_0886.negative_rail = False
        yuan_hua_switch_0886.header_rail = yuan_hua_rail_D46G.id
        yuan_hua_switch_0886.positive_switch = False
        yuan_hua_switch_0886.negative_switch = yuan_hua_switch_0888.id
        yuan_hua_switch_0886.header_switch = False
        yuan_hua_switch_0886.x_pos = 0
        yuan_hua_switch_0886.y_pos = 0

        # yuan_hua_switch_0888
        yuan_hua_switch_0888.positive_rail = yuan_hua_rail_D44G.id
        yuan_hua_switch_0888.negative_rail = False
        yuan_hua_switch_0888.header_rail = yuan_hua_rail_D40G.id
        yuan_hua_switch_0888.positive_switch = False
        yuan_hua_switch_0888.negative_switch = yuan_hua_switch_0886.id
        yuan_hua_switch_0888.header_switch = False
        yuan_hua_switch_0888.x_pos = 0
        yuan_hua_switch_0888.y_pos = 0

        # yuan_hua_rail_0810_0830WG
        yuan_hua_rail_0810_0830WG.left_rail_id = False
        yuan_hua_rail_0810_0830WG.right_rail_id = False
        yuan_hua_rail_0810_0830WG.left_switch_id = yuan_hua_switch_0830.id
        yuan_hua_rail_0810_0830WG.right_switch_id = yuan_hua_switch_0810.id
        yuan_hua_rail_0810_0830WG.left_switch_position = 'positive'
        yuan_hua_rail_0810_0830WG.right_switch_position = False
        yuan_hua_rail_0810_0830WG.x_pos = 2
        yuan_hua_rail_0810_0830WG.y_pos = 2

        # yuan_hua_rail_0884_0886WG
        yuan_hua_rail_0884_0886WG.left_rail_id = False
        yuan_hua_rail_0884_0886WG.right_rail_id = False
        yuan_hua_rail_0884_0886WG.left_switch_id = yuan_hua_switch_0886.id
        yuan_hua_rail_0884_0886WG.right_switch_id = yuan_hua_switch_0884.id
        yuan_hua_rail_0884_0886WG.left_switch_position = 'positive'
        yuan_hua_rail_0884_0886WG.right_switch_position = 'header'
        yuan_hua_rail_0884_0886WG.x_pos = 28
        yuan_hua_rail_0884_0886WG.y_pos = 28

        # yuan_hua_rail_10AG
        yuan_hua_rail_10AG.left_rail_id = yuan_hua_rail_10BG.id
        yuan_hua_rail_10AG.right_rail_id = False
        yuan_hua_rail_10AG.left_switch_id = False
        yuan_hua_rail_10AG.right_switch_id = yuan_hua_switch_0872.id
        yuan_hua_rail_10AG.left_switch_position = False
        yuan_hua_rail_10AG.right_switch_position = 'negative'
        yuan_hua_rail_10AG.x_pos = 32
        yuan_hua_rail_10AG.y_pos = 32

        # yuan_hua_rail_10BG
        yuan_hua_rail_10BG.left_rail_id = False
        yuan_hua_rail_10BG.right_rail_id = yuan_hua_rail_10AG.id
        yuan_hua_rail_10BG.left_switch_id = False
        yuan_hua_rail_10BG.right_switch_id = False
        yuan_hua_rail_10BG.left_switch_position = False
        yuan_hua_rail_10BG.right_switch_position = False
        yuan_hua_rail_10BG.x_pos = 33
        yuan_hua_rail_10BG.y_pos = 33

        # yuan_hua_rail_11AG
        yuan_hua_rail_11AG.left_rail_id = yuan_hua_rail_11BG.id
        yuan_hua_rail_11AG.right_rail_id = False
        yuan_hua_rail_11AG.left_switch_id = False
        yuan_hua_rail_11AG.right_switch_id = yuan_hua_switch_0880.id
        yuan_hua_rail_11AG.left_switch_position = False
        yuan_hua_rail_11AG.right_switch_position = 'negative'
        yuan_hua_rail_11AG.x_pos = 34
        yuan_hua_rail_11AG.y_pos = 34

        # yuan_hua_rail_11BG
        yuan_hua_rail_11BG.left_rail_id = yuan_hua_rail_11AG.id
        yuan_hua_rail_11BG.right_rail_id = False
        yuan_hua_rail_11BG.left_switch_id = False
        yuan_hua_rail_11BG.right_switch_id = False
        yuan_hua_rail_11BG.left_switch_position = False
        yuan_hua_rail_11BG.right_switch_position = False
        yuan_hua_rail_11BG.x_pos = 35
        yuan_hua_rail_11BG.y_pos = 35

        # yuan_hua_rail_12AG
        yuan_hua_rail_12AG.left_rail_id = yuan_hua_rail_12BG.id
        yuan_hua_rail_12AG.right_rail_id = False
        yuan_hua_rail_12AG.left_switch_id = False
        yuan_hua_rail_12AG.right_switch_id = yuan_hua_switch_0880.id
        yuan_hua_rail_12AG.left_switch_position = False
        yuan_hua_rail_12AG.right_switch_position = 'positive'
        yuan_hua_rail_12AG.x_pos = 36
        yuan_hua_rail_12AG.y_pos = 36

        # yuan_hua_rail_12BG
        yuan_hua_rail_12BG.left_rail_id = yuan_hua_rail_12AG.id
        yuan_hua_rail_12BG.right_rail_id = False
        yuan_hua_rail_12BG.left_switch_id = False
        yuan_hua_rail_12BG.right_switch_id = False
        yuan_hua_rail_12BG.left_switch_position = False
        yuan_hua_rail_12BG.right_switch_position = False
        yuan_hua_rail_12BG.x_pos = 37
        yuan_hua_rail_12BG.y_pos = 37

        # yuan_hua_rail_13AG
        yuan_hua_rail_13AG.left_rail_id = yuan_hua_rail_13BG.id
        yuan_hua_rail_13AG.right_rail_id = False
        yuan_hua_rail_13AG.left_switch_id = False
        yuan_hua_rail_13AG.right_switch_id = yuan_hua_switch_0882.id
        yuan_hua_rail_13AG.left_switch_position = False
        yuan_hua_rail_13AG.right_switch_position = 'positive'
        yuan_hua_rail_13AG.x_pos = 38
        yuan_hua_rail_13AG.y_pos = 38

        # yuan_hua_rail_13BG
        yuan_hua_rail_13BG.left_rail_id = yuan_hua_rail_13AG.id
        yuan_hua_rail_13BG.right_rail_id = False
        yuan_hua_rail_13BG.left_switch_id = False
        yuan_hua_rail_13BG.right_switch_id = False
        yuan_hua_rail_13BG.left_switch_position = False
        yuan_hua_rail_13BG.right_switch_position = False
        yuan_hua_rail_13BG.x_pos = 39
        yuan_hua_rail_13BG.y_pos = 39

        # yuan_hua_rail_14AG
        yuan_hua_rail_14AG.left_rail_id = yuan_hua_rail_14BG.id
        yuan_hua_rail_14AG.right_rail_id = False
        yuan_hua_rail_14AG.left_switch_id = False
        yuan_hua_rail_14AG.right_switch_id = yuan_hua_switch_0882.id
        yuan_hua_rail_14AG.left_switch_position = False
        yuan_hua_rail_14AG.right_switch_position = 'negative'
        yuan_hua_rail_14AG.x_pos = 40
        yuan_hua_rail_14AG.y_pos = 40

        # yuan_hua_rail_14BG
        yuan_hua_rail_14BG.left_rail_id = yuan_hua_rail_14AG.id
        yuan_hua_rail_14BG.right_rail_id = False
        yuan_hua_rail_14BG.left_switch_id = False
        yuan_hua_rail_14BG.right_switch_id = False
        yuan_hua_rail_14BG.left_switch_position = False
        yuan_hua_rail_14BG.right_switch_position = False
        yuan_hua_rail_14BG.x_pos = 41
        yuan_hua_rail_14BG.y_pos = 41

        # yuan_hua_rail_15AG
        yuan_hua_rail_15AG.left_rail_id = yuan_hua_rail_15BG.id
        yuan_hua_rail_15AG.right_rail_id = False
        yuan_hua_rail_15AG.left_switch_id = False
        yuan_hua_rail_15AG.right_switch_id = yuan_hua_switch_0874.id
        yuan_hua_rail_15AG.left_switch_position = False
        yuan_hua_rail_15AG.right_switch_position = 'negative'
        yuan_hua_rail_15AG.x_pos = 42
        yuan_hua_rail_15AG.y_pos = 42

        # yuan_hua_rail_15BG
        yuan_hua_rail_15BG.left_rail_id = yuan_hua_rail_15AG.id
        yuan_hua_rail_15BG.right_rail_id = False
        yuan_hua_rail_15BG.left_switch_id = False
        yuan_hua_rail_15BG.right_switch_id = False
        yuan_hua_rail_15BG.left_switch_position = False
        yuan_hua_rail_15BG.right_switch_position = False
        yuan_hua_rail_15BG.x_pos = 43
        yuan_hua_rail_15BG.y_pos = 43

        # yuan_hua_rail_16AG
        yuan_hua_rail_16AG.left_rail_id = yuan_hua_rail_16BG.id
        yuan_hua_rail_16AG.right_rail_id = False
        yuan_hua_rail_16AG.left_switch_id = False
        yuan_hua_rail_16AG.right_switch_id = yuan_hua_switch_0876.id
        yuan_hua_rail_16AG.left_switch_position = False
        yuan_hua_rail_16AG.right_switch_position = 'positive'
        yuan_hua_rail_16AG.x_pos = 44
        yuan_hua_rail_16AG.y_pos = 44

        # yuan_hua_rail_16BG
        yuan_hua_rail_16BG.left_rail_id = yuan_hua_rail_16AG.id
        yuan_hua_rail_16BG.right_rail_id = False
        yuan_hua_rail_16BG.left_switch_id = False
        yuan_hua_rail_16BG.right_switch_id = False
        yuan_hua_rail_16BG.left_switch_position = False
        yuan_hua_rail_16BG.right_switch_position = False
        yuan_hua_rail_16BG.x_pos = 45
        yuan_hua_rail_16BG.y_pos = 45

        # yuan_hua_rail_17AG
        yuan_hua_rail_17AG.left_rail_id = yuan_hua_rail_17BG.id
        yuan_hua_rail_17AG.right_rail_id = False
        yuan_hua_rail_17AG.left_switch_id = False
        yuan_hua_rail_17AG.right_switch_id = yuan_hua_switch_0876.id
        yuan_hua_rail_17AG.left_switch_position = False
        yuan_hua_rail_17AG.right_switch_position = 'negative'
        yuan_hua_rail_17AG.x_pos = 46
        yuan_hua_rail_17AG.y_pos = 46

        # yuan_hua_rail_17BG
        yuan_hua_rail_17BG.left_rail_id = yuan_hua_rail_17AG.id
        yuan_hua_rail_17BG.right_rail_id = False
        yuan_hua_rail_17BG.left_switch_id = False
        yuan_hua_rail_17BG.right_switch_id = False
        yuan_hua_rail_17BG.left_switch_position = False
        yuan_hua_rail_17BG.right_switch_position = False
        yuan_hua_rail_17BG.x_pos = 47
        yuan_hua_rail_17BG.y_pos = 47

        # yuan_hua_rail_18AG
        yuan_hua_rail_18AG.left_rail_id = False
        yuan_hua_rail_18AG.right_rail_id = False
        yuan_hua_rail_18AG.left_switch_id = False
        yuan_hua_rail_18AG.right_switch_id = yuan_hua_switch_0858.id
        yuan_hua_rail_18AG.left_switch_position = False
        yuan_hua_rail_18AG.right_switch_position = 'negative'
        yuan_hua_rail_18AG.x_pos = 48
        yuan_hua_rail_18AG.y_pos = 48

        # yuan_hua_rail_18BG
        yuan_hua_rail_18BG.left_rail_id = yuan_hua_rail_18AG.id
        yuan_hua_rail_18BG.right_rail_id = False
        yuan_hua_rail_18BG.left_switch_id = False
        yuan_hua_rail_18BG.right_switch_id = False
        yuan_hua_rail_18BG.left_switch_position = False
        yuan_hua_rail_18BG.right_switch_position = False
        yuan_hua_rail_18BG.x_pos = 49
        yuan_hua_rail_18BG.y_pos = 49

        # yuan_hua_rail_19G
        yuan_hua_rail_19G.left_rail_id = False
        yuan_hua_rail_19G.right_rail_id = False
        yuan_hua_rail_19G.left_switch_id = False
        yuan_hua_rail_19G.right_switch_id = yuan_hua_switch_0860.id
        yuan_hua_rail_19G.left_switch_position = False
        yuan_hua_rail_19G.right_switch_position = False
        yuan_hua_rail_19G.x_pos = 50
        yuan_hua_rail_19G.y_pos = 50

        # yuan_hua_rail_1AG
        yuan_hua_rail_1AG.left_rail_id = yuan_hua_rail_1BG.id
        yuan_hua_rail_1AG.right_rail_id = False
        yuan_hua_rail_1AG.left_switch_id = False
        yuan_hua_rail_1AG.right_switch_id = yuan_hua_switch_0864.id
        yuan_hua_rail_1AG.left_switch_position = 'negative'
        yuan_hua_rail_1AG.right_switch_position = False
        yuan_hua_rail_1AG.x_pos = 51
        yuan_hua_rail_1AG.y_pos = 51

        # yuan_hua_rail_1BG
        yuan_hua_rail_1BG.left_rail_id = yuan_hua_rail_1CG.id
        yuan_hua_rail_1BG.right_rail_id = yuan_hua_rail_1AG.id
        yuan_hua_rail_1BG.left_switch_id = False
        yuan_hua_rail_1BG.right_switch_id = False
        yuan_hua_rail_1BG.left_switch_position = False
        yuan_hua_rail_1BG.right_switch_position = False
        yuan_hua_rail_1BG.x_pos = 52
        yuan_hua_rail_1BG.y_pos = 52

        # yuan_hua_rail_1CG
        yuan_hua_rail_1CG.left_rail_id = False
        yuan_hua_rail_1CG.right_rail_id = yuan_hua_rail_1BG.id
        yuan_hua_rail_1CG.left_switch_id = False
        yuan_hua_rail_1CG.right_switch_id = False
        yuan_hua_rail_1CG.left_switch_position = False
        yuan_hua_rail_1CG.right_switch_position = False
        yuan_hua_rail_1CG.x_pos = 53
        yuan_hua_rail_1CG.y_pos = 53

        # yuan_hua_rail_20G
        yuan_hua_rail_20G.left_rail_id = False
        yuan_hua_rail_20G.right_rail_id = False
        yuan_hua_rail_20G.left_switch_id = False
        yuan_hua_rail_20G.right_switch_id = yuan_hua_switch_0878.id
        yuan_hua_rail_20G.left_switch_position = False
        yuan_hua_rail_20G.right_switch_position = 'negative'
        yuan_hua_rail_20G.x_pos = 54
        yuan_hua_rail_20G.y_pos = 54

        # yuan_hua_rail_21G
        yuan_hua_rail_21G.left_rail_id = False
        yuan_hua_rail_21G.right_rail_id = False
        yuan_hua_rail_21G.left_switch_id = False
        yuan_hua_rail_21G.right_switch_id = yuan_hua_switch_0878.id
        yuan_hua_rail_21G.left_switch_position = False
        yuan_hua_rail_21G.right_switch_position = 'positive'
        yuan_hua_rail_21G.x_pos = 55
        yuan_hua_rail_21G.y_pos = 55

        # yuan_hua_rail_22G
        yuan_hua_rail_22G.left_rail_id = False
        yuan_hua_rail_22G.right_rail_id = False
        yuan_hua_rail_22G.left_switch_id = False
        yuan_hua_rail_22G.right_switch_id = yuan_hua_switch_0862.id
        yuan_hua_rail_22G.left_switch_position = False
        yuan_hua_rail_22G.right_switch_position = 'positive'
        yuan_hua_rail_22G.x_pos = 56
        yuan_hua_rail_22G.y_pos = 56

        # yuan_hua_rail_23G
        yuan_hua_rail_23G.left_rail_id = False
        yuan_hua_rail_23G.right_rail_id = False
        yuan_hua_rail_23G.left_switch_id = False
        yuan_hua_rail_23G.right_switch_id = yuan_hua_switch_0862.id
        yuan_hua_rail_23G.left_switch_position = False
        yuan_hua_rail_23G.right_switch_position = 'negative'
        yuan_hua_rail_23G.x_pos = 57
        yuan_hua_rail_23G.y_pos = 57

        # yuan_hua_rail_24G
        yuan_hua_rail_24G.left_rail_id = False
        yuan_hua_rail_24G.right_rail_id = yuan_hua_rail_24G.id
        yuan_hua_rail_24G.left_switch_id = False
        yuan_hua_rail_24G.right_switch_id = False
        yuan_hua_rail_24G.left_switch_position = False
        yuan_hua_rail_24G.right_switch_position = False
        yuan_hua_rail_24G.x_pos = 58
        yuan_hua_rail_24G.y_pos = 58

        # yuan_hua_rail_24G1
        yuan_hua_rail_24G1.left_rail_id = yuan_hua_rail_24G.id
        yuan_hua_rail_24G1.right_rail_id = False
        yuan_hua_rail_24G1.left_switch_id = False
        yuan_hua_rail_24G1.right_switch_id = yuan_hua_switch_0844.id
        yuan_hua_rail_24G1.left_switch_position = False
        yuan_hua_rail_24G1.right_switch_position = False
        yuan_hua_rail_24G1.x_pos = 59
        yuan_hua_rail_24G1.y_pos = 59

        # yuan_hua_rail_25G
        yuan_hua_rail_25G.left_rail_id = False
        yuan_hua_rail_25G.right_rail_id = False
        yuan_hua_rail_25G.left_switch_id = False
        yuan_hua_rail_25G.right_switch_id = yuan_hua_switch_0850.id
        yuan_hua_rail_25G.left_switch_position = False
        yuan_hua_rail_25G.right_switch_position = 'negative'
        yuan_hua_rail_25G.x_pos = 60
        yuan_hua_rail_25G.y_pos = 60

        # yuan_hua_rail_26G
        yuan_hua_rail_26G.left_rail_id = False
        yuan_hua_rail_26G.right_rail_id = False
        yuan_hua_rail_26G.left_switch_id = False
        yuan_hua_rail_26G.right_switch_id = yuan_hua_switch_0844.id
        yuan_hua_rail_26G.left_switch_position = False
        yuan_hua_rail_26G.right_switch_position = 'negative'
        yuan_hua_rail_26G.x_pos = 61
        yuan_hua_rail_26G.y_pos = 61

        # yuan_hua_rail_27G
        yuan_hua_rail_27G.left_rail_id = False
        yuan_hua_rail_27G.right_rail_id = False
        yuan_hua_rail_27G.left_switch_id = False
        yuan_hua_rail_27G.right_switch_id = yuan_hua_switch_0824.id
        yuan_hua_rail_27G.left_switch_position = False
        yuan_hua_rail_27G.right_switch_position = 'negative'
        yuan_hua_rail_27G.x_pos = 62
        yuan_hua_rail_27G.y_pos = 62

        # yuan_hua_rail_28G
        yuan_hua_rail_28G.left_rail_id = False
        yuan_hua_rail_28G.right_rail_id = False
        yuan_hua_rail_28G.left_switch_id = False
        yuan_hua_rail_28G.right_switch_id = yuan_hua_switch_0838.id
        yuan_hua_rail_28G.left_switch_position = False
        yuan_hua_rail_28G.right_switch_position = 'positive'
        yuan_hua_rail_28G.x_pos = 63
        yuan_hua_rail_28G.y_pos = 63

        # yuan_hua_rail_29G
        yuan_hua_rail_29G.left_rail_id = False
        yuan_hua_rail_29G.right_rail_id = False
        yuan_hua_rail_29G.left_switch_id = False
        yuan_hua_rail_29G.right_switch_id = yuan_hua_switch_0838.id
        yuan_hua_rail_29G.left_switch_position = False
        yuan_hua_rail_29G.right_switch_position = 'negative'
        yuan_hua_rail_29G.x_pos = 64
        yuan_hua_rail_29G.y_pos = 64

        # yuan_hua_rail_2G
        yuan_hua_rail_2G.left_rail_id = False
        yuan_hua_rail_2G.right_rail_id = False
        yuan_hua_rail_2G.left_switch_id = False
        yuan_hua_rail_2G.right_switch_id = yuan_hua_switch_0864.id
        yuan_hua_rail_2G.left_switch_position = False
        yuan_hua_rail_2G.right_switch_position = False
        yuan_hua_rail_2G.x_pos = 65
        yuan_hua_rail_2G.y_pos = 65

        # yuan_hua_rail_30G
        yuan_hua_rail_30G.left_rail_id = False
        yuan_hua_rail_30G.right_rail_id = False
        yuan_hua_rail_30G.left_switch_id = False
        yuan_hua_rail_30G.right_switch_id = yuan_hua_switch_0840.id
        yuan_hua_rail_30G.left_switch_position = False
        yuan_hua_rail_30G.right_switch_position = 'positive'
        yuan_hua_rail_30G.x_pos = 66
        yuan_hua_rail_30G.y_pos = 66

        # yuan_hua_rail_31G
        yuan_hua_rail_31G.left_rail_id = False
        yuan_hua_rail_31G.right_rail_id = False
        yuan_hua_rail_31G.left_switch_id = False
        yuan_hua_rail_31G.right_switch_id = yuan_hua_switch_0840.id
        yuan_hua_rail_31G.left_switch_position = False
        yuan_hua_rail_31G.right_switch_position = 'negative'
        yuan_hua_rail_31G.x_pos = 67
        yuan_hua_rail_31G.y_pos = 67

        # yuan_hua_rail_34G
        yuan_hua_rail_34G.left_rail_id = False
        yuan_hua_rail_34G.right_rail_id = False
        yuan_hua_rail_34G.left_switch_id = yuan_hua_switch_0806.id
        yuan_hua_rail_34G.right_switch_id = yuan_hua_switch_0884.id
        yuan_hua_rail_34G.left_switch_position = 'header'
        yuan_hua_rail_34G.right_switch_position = 'negative'
        yuan_hua_rail_34G.x_pos = 68
        yuan_hua_rail_34G.y_pos = 68

        # yuan_hua_rail_3AG
        yuan_hua_rail_3AG.left_rail_id = yuan_hua_rail_3BG.id
        yuan_hua_rail_3AG.right_rail_id = False
        yuan_hua_rail_3AG.left_switch_id = False
        yuan_hua_rail_3AG.right_switch_id = yuan_hua_switch_0886.id
        yuan_hua_rail_3AG.left_switch_position = False
        yuan_hua_rail_3AG.right_switch_position = 'negative'
        yuan_hua_rail_3AG.x_pos = 69
        yuan_hua_rail_3AG.y_pos = 69

        # yuan_hua_rail_3BG
        yuan_hua_rail_3BG.left_rail_id = yuan_hua_rail_3AG.id
        yuan_hua_rail_3BG.right_rail_id = False
        yuan_hua_rail_3BG.left_switch_id = False
        yuan_hua_rail_3BG.right_switch_id = False
        yuan_hua_rail_3BG.left_switch_position = False
        yuan_hua_rail_3BG.right_switch_position = False
        yuan_hua_rail_3BG.x_pos = 70
        yuan_hua_rail_3BG.y_pos = 70

        # yuan_hua_rail_4AG
        yuan_hua_rail_4AG.left_rail_id = yuan_hua_rail_4BG.id
        yuan_hua_rail_4AG.right_rail_id = False
        yuan_hua_rail_4AG.left_switch_id = False
        yuan_hua_rail_4AG.right_switch_id = yuan_hua_switch_0886.id
        yuan_hua_rail_4AG.left_switch_position = False
        yuan_hua_rail_4AG.right_switch_position = 'positive'
        yuan_hua_rail_4AG.x_pos = 71
        yuan_hua_rail_4AG.y_pos = 71

        # yuan_hua_rail_4BG
        yuan_hua_rail_4BG.left_rail_id = yuan_hua_rail_4AG.id
        yuan_hua_rail_4BG.right_rail_id = False
        yuan_hua_rail_4BG.left_switch_id = False
        yuan_hua_rail_4BG.right_switch_id = False
        yuan_hua_rail_4BG.left_switch_position = False
        yuan_hua_rail_4BG.right_switch_position = False
        yuan_hua_rail_4BG.x_pos = 72
        yuan_hua_rail_4BG.y_pos = 72

        # yuan_hua_rail_5AG
        yuan_hua_rail_5AG.left_rail_id = yuan_hua_rail_5BG.id
        yuan_hua_rail_5AG.right_rail_id = False
        yuan_hua_rail_5AG.left_switch_id = False
        yuan_hua_rail_5AG.right_switch_id = yuan_hua_switch_0854.id
        yuan_hua_rail_5AG.left_switch_position = False
        yuan_hua_rail_5AG.right_switch_position = 'negative'
        yuan_hua_rail_5AG.x_pos = 73
        yuan_hua_rail_5AG.y_pos = 73

        # yuan_hua_rail_5BG
        yuan_hua_rail_5BG.left_rail_id = yuan_hua_rail_5AG.id
        yuan_hua_rail_5BG.right_rail_id = False
        yuan_hua_rail_5BG.left_switch_id = False
        yuan_hua_rail_5BG.right_switch_id = False
        yuan_hua_rail_5BG.left_switch_position = False
        yuan_hua_rail_5BG.right_switch_position = False
        yuan_hua_rail_5BG.x_pos = 74
        yuan_hua_rail_5BG.y_pos = 74

        # yuan_hua_rail_6AG
        yuan_hua_rail_6AG.left_rail_id = yuan_hua_rail_6BG.id
        yuan_hua_rail_6AG.right_rail_id = False
        yuan_hua_rail_6AG.left_switch_id = False
        yuan_hua_rail_6AG.right_switch_id = yuan_hua_switch_0868.id
        yuan_hua_rail_6AG.left_switch_position = False
        yuan_hua_rail_6AG.right_switch_position = 'negative'
        yuan_hua_rail_6AG.x_pos = 75
        yuan_hua_rail_6AG.y_pos = 75

        # yuan_hua_rail_6BG
        yuan_hua_rail_6BG.left_rail_id = yuan_hua_rail_6AG.id
        yuan_hua_rail_6BG.right_rail_id = False
        yuan_hua_rail_6BG.left_switch_id = False
        yuan_hua_rail_6BG.right_switch_id = False
        yuan_hua_rail_6BG.left_switch_position = False
        yuan_hua_rail_6BG.right_switch_position = False
        yuan_hua_rail_6BG.x_pos = 76
        yuan_hua_rail_6BG.y_pos = 76

        # yuan_hua_rail_7AG
        yuan_hua_rail_7AG.left_rail_id = yuan_hua_rail_7BG.id
        yuan_hua_rail_7AG.right_rail_id = False
        yuan_hua_rail_7AG.left_switch_id = False
        yuan_hua_rail_7AG.right_switch_id = yuan_hua_switch_0868.id
        yuan_hua_rail_7AG.left_switch_position = False
        yuan_hua_rail_7AG.right_switch_position = 'positive'
        yuan_hua_rail_7AG.x_pos = 77
        yuan_hua_rail_7AG.y_pos = 77

        # yuan_hua_rail_7BG
        yuan_hua_rail_7BG.left_rail_id = yuan_hua_rail_7AG.id
        yuan_hua_rail_7BG.right_rail_id = False
        yuan_hua_rail_7BG.left_switch_id = False
        yuan_hua_rail_7BG.right_switch_id = False
        yuan_hua_rail_7BG.left_switch_position = False
        yuan_hua_rail_7BG.right_switch_position = False
        yuan_hua_rail_7BG.x_pos = 78
        yuan_hua_rail_7BG.y_pos = 78

        # yuan_hua_rail_8AG
        yuan_hua_rail_8AG.left_rail_id = yuan_hua_rail_8BG.id
        yuan_hua_rail_8AG.right_rail_id = False
        yuan_hua_rail_8AG.left_switch_id = False
        yuan_hua_rail_8AG.right_switch_id = yuan_hua_switch_0870.id
        yuan_hua_rail_8AG.left_switch_position = False
        yuan_hua_rail_8AG.right_switch_position = 'negative'
        yuan_hua_rail_8AG.x_pos = 79
        yuan_hua_rail_8AG.y_pos = 79

        # yuan_hua_rail_8BG
        yuan_hua_rail_8BG.left_rail_id = yuan_hua_rail_8AG.id
        yuan_hua_rail_8BG.right_rail_id = False
        yuan_hua_rail_8BG.left_switch_id = False
        yuan_hua_rail_8BG.right_switch_id = False
        yuan_hua_rail_8BG.left_switch_position = False
        yuan_hua_rail_8BG.right_switch_position = False
        yuan_hua_rail_8BG.x_pos = 80
        yuan_hua_rail_8BG.y_pos = 80

        # yuan_hua_rail_9AG
        yuan_hua_rail_9AG.left_rail_id = yuan_hua_rail_9BG.id
        yuan_hua_rail_9AG.right_rail_id = False
        yuan_hua_rail_9AG.left_switch_id = False
        yuan_hua_rail_9AG.right_switch_id = yuan_hua_switch_0870.id
        yuan_hua_rail_9AG.left_switch_position = False
        yuan_hua_rail_9AG.right_switch_position = 'positive'
        yuan_hua_rail_9AG.x_pos = 81
        yuan_hua_rail_9AG.y_pos = 81

        # yuan_hua_rail_9BG
        yuan_hua_rail_9BG.left_rail_id = yuan_hua_rail_9AG.id
        yuan_hua_rail_9BG.right_rail_id = False
        yuan_hua_rail_9BG.left_switch_id = False
        yuan_hua_rail_9BG.right_switch_id = False
        yuan_hua_rail_9BG.left_switch_position = False
        yuan_hua_rail_9BG.right_switch_position = False
        yuan_hua_rail_9BG.x_pos = 82
        yuan_hua_rail_9BG.y_pos = 82

        # yuan_hua_rail_D40G
        yuan_hua_rail_D40G.left_rail_id = False
        yuan_hua_rail_D40G.right_rail_id = False
        yuan_hua_rail_D40G.left_switch_id = yuan_hua_switch_0888.id
        yuan_hua_rail_D40G.right_switch_id = False
        yuan_hua_rail_D40G.left_switch_position = 'header'
        yuan_hua_rail_D40G.right_switch_position = False
        yuan_hua_rail_D40G.x_pos = 83
        yuan_hua_rail_D40G.y_pos = 83

        # yuan_hua_rail_D44G
        yuan_hua_rail_D44G.left_rail_id = False
        yuan_hua_rail_D44G.right_rail_id = False
        yuan_hua_rail_D44G.left_switch_id = False
        yuan_hua_rail_D44G.right_switch_id = yuan_hua_switch_0888.id
        yuan_hua_rail_D44G.left_switch_position = False
        yuan_hua_rail_D44G.right_switch_position = 'positive'
        yuan_hua_rail_D44G.x_pos = 84
        yuan_hua_rail_D44G.y_pos = 84

        # yuan_hua_rail_D46G
        yuan_hua_rail_D46G.left_rail_id = yuan_hua_rail_0586DG.id
        yuan_hua_rail_D46G.right_rail_id = False
        yuan_hua_rail_D46G.left_switch_id = False
        yuan_hua_rail_D46G.right_switch_id = yuan_hua_switch_0886.id
        yuan_hua_rail_D46G.left_switch_position = False
        yuan_hua_rail_D46G.right_switch_position = False
        yuan_hua_rail_D46G.x_pos = 85
        yuan_hua_rail_D46G.y_pos = 85

        # yuan_hua_rail_T2613
        yuan_hua_rail_T2613.left_rail_id = yuan_hua_rail_T2611.id
        yuan_hua_rail_T2613.right_rail_id = False
        yuan_hua_rail_T2613.left_switch_id = False
        yuan_hua_rail_T2613.right_switch_id = False
        yuan_hua_rail_T2613.left_switch_position = False
        yuan_hua_rail_T2613.right_switch_position = False
        yuan_hua_rail_T2613.x_pos = 86
        yuan_hua_rail_T2613.y_pos = 86

        # yuan_hua_rail_T2611
        yuan_hua_rail_T2611.left_rail_id = yuan_hua_rail_T2609.id
        yuan_hua_rail_T2611.right_rail_id = yuan_hua_rail_T2613.id
        yuan_hua_rail_T2611.left_switch_id = False
        yuan_hua_rail_T2611.right_switch_id = False
        yuan_hua_rail_T2611.left_switch_position = False
        yuan_hua_rail_T2611.right_switch_position = False
        yuan_hua_rail_T2611.x_pos = 86
        yuan_hua_rail_T2611.y_pos = 86

        # yuan_hua_rail_T2806
        yuan_hua_rail_T2806.left_rail_id = yuan_hua_rail_T2804.id
        yuan_hua_rail_T2806.right_rail_id = False
        yuan_hua_rail_T2806.left_switch_id = False
        yuan_hua_rail_T2806.right_switch_id = False
        yuan_hua_rail_T2806.left_switch_position = False
        yuan_hua_rail_T2806.right_switch_position = False
        yuan_hua_rail_T2806.x_pos = 89
        yuan_hua_rail_T2806.y_pos = 89

        # yuan_hua_rail_T2825
        yuan_hua_rail_T2825.left_rail_id = yuan_hua_rail_T2827.id
        yuan_hua_rail_T2825.right_rail_id = False
        yuan_hua_rail_T2825.left_switch_id = False
        yuan_hua_rail_T2825.right_switch_id = False
        yuan_hua_rail_T2825.left_switch_position = False
        yuan_hua_rail_T2825.right_switch_position = False
        yuan_hua_rail_T2825.x_pos = 92
        yuan_hua_rail_T2825.y_pos = 92

        # yuan_hua_rail_T2609
        yuan_hua_rail_T2609.left_rail_id = False
        yuan_hua_rail_T2609.right_rail_id = yuan_hua_rail_T2611.id
        yuan_hua_rail_T2609.left_switch_id = yuan_hua_switch_0810.id
        yuan_hua_rail_T2609.right_switch_id = False
        yuan_hua_rail_T2609.left_switch_position = 'header'
        yuan_hua_rail_T2609.right_switch_position = False
        yuan_hua_rail_T2609.x_pos = 93
        yuan_hua_rail_T2609.y_pos = 93

        # yuan_hua_rail_T2611
        yuan_hua_rail_T2611.left_rail_id = yuan_hua_rail_T2609.id
        yuan_hua_rail_T2611.right_rail_id = yuan_hua_rail_T2613.id
        yuan_hua_rail_T2611.left_switch_id = False
        yuan_hua_rail_T2611.right_switch_id = False
        yuan_hua_rail_T2611.left_switch_position = False
        yuan_hua_rail_T2611.right_switch_position = False
        yuan_hua_rail_T2611.x_pos = 94
        yuan_hua_rail_T2611.y_pos = 94

        # yuan_hua_rail_T2802
        yuan_hua_rail_T2802.left_rail_id = False
        yuan_hua_rail_T2802.right_rail_id = yuan_hua_rail_T2804.id
        yuan_hua_rail_T2802.left_switch_id = yuan_hua_switch_0802
        yuan_hua_rail_T2802.right_switch_id = False
        yuan_hua_rail_T2802.left_switch_position = False
        yuan_hua_rail_T2802.right_switch_position = False
        yuan_hua_rail_T2802.x_pos = 95
        yuan_hua_rail_T2802.y_pos = 95

        # yuan_hua_rail_T2804
        yuan_hua_rail_T2804.left_rail_id = yuan_hua_rail_T2802.id
        yuan_hua_rail_T2804.right_rail_id = yuan_hua_rail_T2806.id
        yuan_hua_rail_T2804.left_switch_id = False
        yuan_hua_rail_T2804.right_switch_id = False
        yuan_hua_rail_T2804.left_switch_position = False
        yuan_hua_rail_T2804.right_switch_position = False
        yuan_hua_rail_T2804.x_pos = 96
        yuan_hua_rail_T2804.y_pos = 96

        # yuan_hua_rail_T2827
        yuan_hua_rail_T2827.left_rail_id = yuan_hua_rail_T2829.id
        yuan_hua_rail_T2827.right_rail_id = yuan_hua_rail_T2825.id
        yuan_hua_rail_T2827.left_switch_id = False
        yuan_hua_rail_T2827.right_switch_id = False
        yuan_hua_rail_T2827.left_switch_position = False
        yuan_hua_rail_T2827.right_switch_position = False
        yuan_hua_rail_T2827.x_pos = 97
        yuan_hua_rail_T2827.y_pos = 97

        # yuan_hua_rail_T2829
        yuan_hua_rail_T2829.left_rail_id = False
        yuan_hua_rail_T2829.right_rail_id = yuan_hua_rail_T2827.id
        yuan_hua_rail_T2829.left_switch_id = yuan_hua_switch_0812.id
        yuan_hua_rail_T2829.right_switch_id = False
        yuan_hua_rail_T2829.left_switch_position = False
        yuan_hua_rail_T2829.right_switch_position = False
        yuan_hua_rail_T2829.x_pos = 98
        yuan_hua_rail_T2829.y_pos = 98
