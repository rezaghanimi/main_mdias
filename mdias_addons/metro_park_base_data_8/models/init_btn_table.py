
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitBtnTable(models.TransientModel):
    '''
    初始化轨道和道岔信息
    '''
    _name = 'metro_park_base_data_8.init_btn_table'

    @api.model
    def init_button_table(self):
        '''
        初始化按扭表
        :return:
        '''
        records = self.search([])
        if len(records) > 0:
            return

        gao_da_lu_table = ["1 = SZC = LA", "2 = SZC = YA", "3 = SZC = YZSA", "4 = XC = LA", "5 = XC = YA",
                           "6 = XC = YZSA", "7 = SZR = LA", "8 = SZR = YA", "9 = SZR = YZSA", "10 = XR = LA",
                           "11 = XR = YA", "12 = XR = YZSA", "13 = D12 = LA", "14 = D12 = YA", "15 = D12 = YZSA",
                           "16 = D14 = LA", "17 = D14 = YA", "18 = D14 = YZSA", "19 = XRZA = LA", "20 = XRZA = YA",
                           "21 = XRZA = YZSA", "22 = XCZA = LA", "23 = XCZA = YA", "24 = XCZA = YZSA", "25 = S2 = LA",
                           "26 = S4 = LA", "27 = S6 = LA", "28 = S8 = LA", "29 = S10 = LA", "30 = S12 = LA",
                           "31 = S14 = LA", "32 = S3 = LA", "33 = S5 = LA", "34 = S7 = LA", "35 = S9 = LA",
                           "36 = S11 = LA", "37 = S13 = LA", "38 = S15 = LA", "39 = SC = LA", "40 = SR = LA",
                           "41 = S25 = LA", "42 = S24 = LA", "43 = S23 = LA", "44 = S16 = LA", "45 = D12 = DA",
                           "46 = D14 = DA", "47 = S2 = DA", "48 = S4 = DA", "49 = S6 = DA", "50 = S8 = DA",
                           "51 = S10 = DA", "52 = S12 = DA", "53 = S14 = DA", "54 = S3 = DA", "55 = S5 = DA",
                           "56 = S7 = DA", "57 = S9 = DA", "58 = S11 = DA", "59 = S13 = DA", "60 = S15 = DA",
                           "61 = SC = DA", "62 = SR = DA", "63 = S25 = DA", "64 = S24 = DA", "65 = S23 = DA",
                           "66 = S16 = DA", "67 = D5A = DA", "68 = D7A = DA", "69 = D9A = DA", "70 = D11A = DA",
                           "71 = D13A = DA", "72 = D15A = DA", "73 = D6A = DA", "74 = D8A = DA", "75 = D10A = DA",
                           "76 = D12A = DA", "77 = D14A = DA", "78 = D16A = DA", "79 = D5B = DA", "80 = D7B = DA",
                           "81 = D9B = DA", "82 = D11B = DA", "83 = D13B = DA", "84 = D15B = DA", "85 = D6B = DA",
                           "86 = D8B = DA", "87 = D10B = DA", "88 = D12B = DA", "89 = D14B = DA", "90 = D16B = DA",
                           "91 = D2 = DA", "92 = D4 = DA", "93 = D6 = DA", "94 = D8 = DA", "95 = D10 = DA",
                           "96 = D16 = DA", "97 = D18 = DA", "98 = D20 = DA", "99 = D22 = DA", "100 = D24 = DA",
                           "101 = D26 = DA", "102 = D16BZA = DA", "103 = D5BZA = DA", "104 = D6BZA = DA",
                           "105 = D7BZA = DA", "106 = D8BZA = DA", "107 = D9BZA = DA", "108 = D10BZA = DA",
                           "109 = D11BZA = DA", "110 = D12BZA = DA", "111 = D13BZA = DA", "112 = D14BZA = DA",
                           "113 = D15BZA = DA", "114 = JT14 = DA", "115 = JT16 = DA", "116 = JT18 = DA",
                           "117 = JT12 = DA", "118 = JT2 = DA", "119 = JT6 = DA", "120 = JT8 = DA", "121 = JT10 = DA",
                           "122 = JT4 = DA", "123 = 2 = CA", "124 = 2DG = CQ", "125 = 4 = CA", "126 = 4DG = CQ",
                           "127 = 6 = CA", "128 = 6_12DG = CQ", "129 = 8 = CA", "130 = 8_10DG = CQ", "131 = 10 = CA",
                           "132 = 12 = CA", "133 = 14 = CA", "134 = 14_20DG = CQ", "135 = 16 = CA",
                           "136 = 16_18DG = CQ", "137 = 18 = CA", "138 = 20 = CA", "139 = 22 = CA",
                           "140 = 22_26DG = CQ", "141 = 24 = CA", "142 = 26 = CA", "143 = 28 = CA", "144 = 28DG = CQ",
                           "145 = 30 = CA", "146 = 30_32DG = CQ", "147 = 32 = CA", "148 = 34 = CA", "149 = 34DG = CQ",
                           "150 = 36 = CA", "151 = 36DG = CQ", "152 = 38 = CA", "153 = 38DG = CQ", "154 = 40 = CA",
                           "155 = 40_42DG = CQ", "156 = 42 = CA", "157 = 44 = CA", "158 = 44_48DG = CQ",
                           "159 = 46 = CA", "160 = 48 = CA", "161 = 50 = CA", "162 = 50_52DG = CQ", "163 = 52 = CA",
                           "164 = 54 = CA", "165 = 54_60DG = CQ", "166 = 56 = CA", "167 = 58 = CA", "168 = 60 = CA",
                           "169 = 62 = CA", "170 = 62DG = CQ", "171 = 16AG = WC", "172 = 15AG = WC", "173 = 14AG = WC",
                           "174 = 13AG = WC", "175 = 12AG = WC", "176 = 11AG = WC", "177 = 10AG = WC", "178 = 9AG = WC",
                           "179 = 8AG = WC", "180 = 7AG = WC", "181 = 6AG = WC", "182 = 5AG = WC", "183 = 1G = WC",
                           "184 = 16BG = WC", "185 = 15BG = WC", "186 = 14BG = WC", "187 = 13BG = WC",
                           "188 = 12BG = WC", "189 = 11BG = WC", "190 = 10BG = WC", "191 = 9BG = WC", "192 = 8BG = WC",
                           "193 = 7BG = WC", "194 = 6BG = WC", "195 = 5BG = WC", "196 = D4G = WC", "197 = D2G = WC",
                           "198 = D26WG = WC", "199 = D22G = WC", "200 = T2602G = WC", "201 = T2617G = WC",
                           "202 = 2_34WG = WC", "203 = T2604G = WC", "204 = T2615G = WC", "205 = 4G = GD",
                           "206 = 3G = GD", "207 = 2G = GD", "208 = 23G = GD", "209 = 24G = GD", "210 = 25G = GD",
                           "211 = 场引导总锁 = BTN"]
        ban_qiao_table = ["1 = SR = LA", "2 = SR = YA", "3 = SR = YZSA", "4 = XZR = LA", "5 = XZR = YA",
                          "6 = XZR = YZSA", "7 = XZC = LA", "8 = XZC = YA", "9 = XZC = YZSA", "10 = SC = LA",
                          "11 = SC = YA", "12 = SC = YZSA", "13 = XCZA = LA", "14 = XCZA = YA", "15 = XCZA = YZSA",
                          "16 = XRZA = LA", "17 = XRZA = YA", "18 = XRZA = YZSA", "19 = SCZA = LA", "20 = SCZA = YA",
                          "21 = SCZA = YZSA", "22 = SRZA = LA", "23 = SRZA = YA", "24 = SRZA = YZSA", "25 = X23 = LA",
                          "26 = X25 = LA", "27 = X27 = LA", "28 = X29 = LA", "29 = X31 = LA", "30 = X33 = LA",
                          "31 = X35 = LA", "32 = X37 = LA", "33 = X39 = LA", "34 = X22 = LA", "35 = X24 = LA",
                          "36 = X26 = LA", "37 = X28 = LA", "38 = X30 = LA", "39 = X32 = LA", "40 = X34 = LA",
                          "41 = X36 = LA", "42 = X38 = LA", "43 = XC = LA", "44 = XR = LA", "45 = X21 = LA",
                          "46 = X23 = DA", "47 = X25 = DA", "48 = X27 = DA", "49 = X29 = DA", "50 = X31 = DA",
                          "51 = X33 = DA", "52 = X35 = DA", "53 = X37 = DA", "54 = X39 = DA", "55 = X22 = DA",
                          "56 = X24 = DA", "57 = X26 = DA", "58 = X28 = DA", "59 = X30 = DA", "60 = X32 = DA",
                          "61 = X34 = DA", "62 = X36 = DA", "63 = X38 = DA", "64 = XC = DA", "65 = XR = DA",
                          "66 = X21 = DA", "67 = D21A = DA", "68 = D23A = DA", "69 = D25A = DA", "70 = D27A = DA",
                          "71 = D29A = DA", "72 = D31A = DA", "73 = D22A = DA", "74 = D24A = DA", "75 = D26A = DA",
                          "76 = D28A = DA", "77 = D30A = DA", "78 = D32A = DA", "79 = D21B = DA", "80 = D23B = DA",
                          "81 = D25B = DA", "82 = D27B = DA", "83 = D29B = DA", "84 = D31B = DA", "85 = D22B = DA",
                          "86 = D24B = DA", "87 = D26B = DA", "88 = D28B = DA", "89 = D30B = DA", "90 = D32B = DA",
                          "91 = D45 = DA", "92 = D47 = DA", "93 = D49 = DA", "94 = D51 = DA", "95 = D53 = DA",
                          "96 = D55 = DA", "97 = D57 = DA", "98 = D59 = DA", "99 = D61 = DA", "100 = D63 = DA",
                          "101 = D65 = DA", "102 = D67 = DA", "103 = D1 = DA", "104 = D3 = DA", "105 = D5 = DA",
                          "106 = D7 = DA", "107 = D9 = DA", "108 = D11 = DA", "109 = D13 = DA", "110 = D15 = DA",
                          "111 = D17 = DA", "112 = D19 = DA", "113 = D21 = DA", "114 = D23 = DA", "115 = D25 = DA",
                          "116 = D27 = DA", "117 = D29 = DA", "118 = D31 = DA", "119 = D37 = DA", "120 = D39 = DA",
                          "121 = D41 = DA", "122 = D43 = DA", "123 = D23BZA = DA", "124 = D21BZA = DA",
                          "125 = D22BZA = DA", "126 = D24BZA = DA", "127 = D25BZA = DA", "128 = D26BZA = DA",
                          "129 = D27BZA = DA", "130 = D28BZA = DA", "131 = D29BZA = DA", "132 = D30BZA = DA",
                          "133 = D31BZA = DA", "134 = D32BZA = DA", "135 = JT25 = DA", "136 = JT23 = DA",
                          "137 = D33 = DA", "138 = D35 = DA", "139 = JT7 = DA", "140 = JT5 = DA", "141 = JT3 = DA",
                          "142 = JT1 = DA", "143 = JT17 = DA", "144 = JT19 = DA", "145 = JT21 = DA", "146 = JT15 = DA",
                          "147 = JT9 = DA", "148 = JT11 = DA", "149 = JT13 = DA", "150 = JT27 = DA", "151 = 1 = CA",
                          "152 = 1_3DG = CQ", "153 = 3 = CA", "154 = 5 = CA", "155 = 5DG = CQ", "156 = 7 = CA",
                          "157 = 7DG = CQ", "158 = 9 = CA", "159 = 9DG = CQ", "160 = 11 = CA", "161 = 11DG = CQ",
                          "162 = 13 = CA", "163 = 13_19DG = CQ", "164 = 15 = CA", "165 = 15_17DG = CQ", "166 = 17 = CA",
                          "167 = 19 = CA", "168 = 21 = CA", "169 = 21DG = CQ", "170 = 23 = CA", "171 = 23DG = CQ",
                          "172 = 25 = CA", "173 = 25DG = CQ", "174 = 27 = CA", "175 = 27DG = CQ", "176 = 29 = CA",
                          "177 = 29_35DG = CQ", "178 = 31 = CA", "179 = 33 = CA", "180 = 35 = CA", "181 = 37 = CA",
                          "182 = 37_39DG = CQ", "183 = 39 = CA", "184 = 41 = CA", "185 = 41_43DG = CQ", "186 = 43 = CA",
                          "187 = 45 = CA", "188 = 45_49DG = CQ", "189 = 47 = CA", "190 = 49 = CA", "191 = 51 = CA",
                          "192 = 51_53DG = CQ", "193 = 53 = CA", "194 = 55 = CA", "195 = 55_59DG = CQ", "196 = 57 = CA",
                          "197 = 59 = CA", "198 = 63 = CA", "199 = 63_65DG = CQ", "200 = 65 = CA", "201 = 67 = CA",
                          "202 = 67_73DG = CQ", "203 = 69 = CA", "204 = 71 = CA", "205 = 73 = CA", "206 = 75 = CA",
                          "207 = 75_77DG = CQ", "208 = 77 = CA", "209 = 79 = CA", "210 = 79_81DG = CQ", "211 = 81 = CA",
                          "212 = 83 = CA", "213 = 83DG = CQ", "214 = 61 = CA", "215 = 61DG = CQ", "216 = 21AG = WC",
                          "217 = 22AG = WC", "218 = 23AG = WC", "219 = 24AG = WC", "220 = 25AG = WC", "221 = 27AG = WC",
                          "222 = 28AG = WC", "223 = 29AG = WC", "224 = 30AG = WC", "225 = 31AG = WC", "226 = 32AG = WC",
                          "227 = 21BG = WC", "228 = 22BG = WC", "229 = 23BG = WC", "230 = 24BG = WC", "231 = 25BG = WC",
                          "232 = 26BG = WC", "233 = 27BG = WC", "234 = 28BG = WC", "235 = 29BG = WC", "236 = 30BG = WC",
                          "237 = 31BG = WC", "238 = 32BG = WC", "239 = 10G = WC", "240 = 11G = WC", "241 = 12G = WC",
                          "242 = 13G = WC", "243 = 14G = WC", "244 = 15G = WC", "245 = 16G = WC", "246 = 17G = WC",
                          "247 = 18G = WC", "248 = D7G = WC", "249 = D5G = WC", "250 = D1G = WC", "251 = 5_27WG = WC",
                          "252 = 9_23WG = WC", "253 = 23_61WG = WC", "254 = 21_51WG = WC", "255 = 25_41WG = WC",
                          "256 = 27_29WG = WC", "257 = 65_83WG = WC", "258 = D37G = WC", "259 = 1_63WG = WC",
                          "260 = 19G = WC", "261 = 20G = WC", "262 = 26AG = WC", "263 = T1714G = WC",
                          "264 = T1701G = WC", "265 = T04G = WC", "266 = ST83G = WC", "267 = T1710G = WC",
                          "268 = T1705G = WC", "269 = 33G = GD", "270 = 34G = GD", "271 = 35G = GD", "272 = 36G = GD",
                          "273 = 37G = GD", "274 = 38G = GD", "275 = 39G = GD", "276 = 段引导总锁 = BTN", "277 = 非进路1 = BTN",
                          "278 = 非进路事故1 = BTN"]

        location_banqiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        location_gaodalu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        vals = []
        for item in gao_da_lu_table:
            tmp_ar = item.split("=")
            vals.append({
                "location": location_gaodalu,
                "index": int(tmp_ar[0].strip()),
                "name": tmp_ar[1].strip(),
                "type": tmp_ar[2].strip()
            })

        for item in ban_qiao_table:
            tmp_ar = item.split("=")
            vals.append({
                "location": location_banqiao,
                "index": int(tmp_ar[0].strip()),
                "name": tmp_ar[1].strip(),
                "type": tmp_ar[2].strip()
            })

        self.create(vals)
