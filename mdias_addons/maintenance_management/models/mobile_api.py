from odoo import models
from odoo.models import DEFAULT_SERVER_DATETIME_FORMAT


class MobileApi(models.AbstractModel):
    _name = 'maintenance_management.mobile_api'

    def get_equipments(self, room_id):
        domain = [('place', '=', int(room_id))]
        equipments = self.env['maintenance_equipment'].search(domain)
        result = self.env['maintenance_management.equipment_state']. \
            search_read([('equipment', 'in', equipments.ids)], ['name', 'id', 'equipment', 'state'])
        return result

    def get_equipment_rooms(self, location_id):

        domain = [('station', '=', int(location_id))]
        result = self.env['maintenance_place'].sudo().search_read(domain, ['name', 'id'])
        return result

    def get_locations(self, line_id=None):
        '''
        TODO 这里后面要配置
        :param line_id:
        :return:
        '''
        line_id = self.env.ref('metro_park_base_data_10.line10', raise_if_not_found=False).id
        domain = [('line', '=', line_id), ('name', '!=', '正线')]
        result = self.env['metro_park_base.location'].search_read(domain, ['name', 'id'])
        return result

    def get_waring_logs(self, equipment_id, offset, limit=20):
        domain = [('equipment', '=', int(equipment_id))]
        res = self.env['maintenance_management.call_record'].sudo().search(domain,
                                                                           offset=offset,
                                                                           limit=limit,
                                                                           order='create_date desc')
        result = []

        def make_value(record):
            if record.alarm_level == '高':

                log_level = 'high'
            else:
                log_level = 'low'
            return {
                'log_level_desc': record.alarm_level,
                'log_level': log_level,
                'log_location_name': record.place,
                'log_location_datetime': record.create_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'log_type_desc': record.content
            }

        for re in res:
            val = make_value(re)
            result.append(val)

        return {
            'data': result,
            'more': len(result) == limit
        }
