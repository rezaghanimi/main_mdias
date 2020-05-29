# -*- coding: utf-8 -*-

addresses = '''
11	太平园
12	簇锦
13	华兴
14	金花
15	双流机场1航站楼站
16	双流机场2航站楼站
17	双流西
18	应天寺
19	黄水
20	花源
21	新津
22	花桥
23	五津
24	儒林路
25	刘家碾
26	新平
98	板桥车辆段
99	高大路停车场
'''

template = '''
<record id="metro_park_base.ats_address_line_10_address_{no}"
        model="metro_park_base.ats_address">
    <field name="no">{no}</field>
    <field name="name">{name}</field>
    <field name="location" ref="metro_park_base.main_line_location"/>
</record>
'''

rst = []
tmp_array = addresses.split("\n")
for item in tmp_array:
    if item == "":
        pass
    address_ar = item.split("	")
    if len(address_ar) != 2:
        continue
    tmp = template.format(no=address_ar[0], name=address_ar[1])
    rst.append(tmp)
print("\n".join(rst))
