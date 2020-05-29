from openpyxl import load_workbook

wb = load_workbook(filename='./RealationData.xlsx')
template = """<record id="construction_area_relation_%s" model="metro_park_dispatch.construction_area_relation">
                    <field name="area_id">%s</field>
                    <field name="area_name">%s</field>
                    <field name="area_code">%s</field>
                    <field name="park_element_code">%s</field>
                    <field name="element_type">%s</field>
                    <field name="line_id">%s</field>
                    <field name="location_id">%s</field>
            </record>
        """
sheet_ranges = wb['Sheet1']
xml = """
        <?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
    """
i = 0
exeits = []
for index in range(1, 167):
    area_id = sheet_ranges['E%s' % index].value
    area_code = sheet_ranges['F%s' % index].value
    area_name = sheet_ranges['G%s' % index].value
    element_des = sheet_ranges['J%s' % index].value
    line_id = sheet_ranges['A%s' % index].value
    location_id = sheet_ranges['C%s' % index].value
    if not element_des:
        continue

    if '道岔' in element_des:
        element_des= element_des.replace('道岔', '')
        element_type = 'switch'

        exeits.append(element_des)
    else:
        element_type = 'rail'
    i += 1
        # exeits.append(element_des)

    xml += template % (area_id, area_id, area_name, area_code, element_des, element_type, line_id, location_id)

xml += """
        </data>
</odoo>
"""
with open('./relation.xml', 'w') as f:
    f.write(xml)
print(tuple(exeits))
print(i)
