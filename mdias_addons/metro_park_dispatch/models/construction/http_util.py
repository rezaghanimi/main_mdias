import time
import logging
import requests
from odoo.models import AbstractModel

_logger = logging.getLogger(__name__)

PLAN_RANGE_MILLISECOND = 3*24*60*60 * 1000


class NotFound404(Exception):
    pass


class RequestAPIError(Exception):
    pass


class HttpUtil(AbstractModel):
    _name = 'metro_park_dispatch.construction.http'

    _COMM_URL = '/consapi-external/webapi'
    _token_expire_time = 0
    _token = None

    @property
    def host(self):
        '''
        取得服务器配置
        :return: 
        '''
        config = self.env['metro_park_base.system_config'].get_configs()
        host = config['construction_api_host']
        if not host:
            return False
        return host + self._COMM_URL

    def _request_token(self):
        """
        请求token接口信息
        :return:
        """
        if self.app_key and self.app_id:
            url = '/getToken?appId=%s&appKey=%s' % (self.app_id, self.app_key)
            data = self._request(url, is_token=True)
            if 'token' in data and 'tokenExpireTime' in data:
                HttpUtil._token = data['token']
                HttpUtil._token_expire_time = data.get('tokenExpireTime', 0) / 1000
        return None

    def _refresh_token(self):
        """
        刷新token,刷新token，
        旧的token就失效了,会刷新token过期时间
        :return:
        """
        url = '/refreshToken?appId=%s&appKey=%s' % (self.app_id, self.app_key)
        data = self._request(url, is_token=True)
        if 'token' in data and 'tokenExpireTime' in data:
            HttpUtil._token = data['token']
            HttpUtil._token_expire_time = data.get('tokenExpireTime', 0) / 1000

    @property
    def token(self):
        """
        请求token，没有token会生成新的，
        有token会直接返回，token及过期时间不变
        :return:
        """
        if not HttpUtil._token:
            self._request_token()
        now = time.time() - 24 * 60 * 60
        if HttpUtil._token_expire_time < now:
            self._refresh_token()
        return HttpUtil._token

    @property
    def app_id(self):
        return self.env['metro_park_base.system_config'].get_configs()['construction_app_id']

    @property
    def app_key(self):
        return self.env['metro_park_base.system_config'].get_configs()['construction_app_key']

    def _request(self, url, check_token=False, is_token=False):
        _url = self.host + url

        if not is_token:
            _url += '&appId=%s&token=%s' % (self.app_id, self.token)
        response = requests.get(_url)
        _logger.info('request api url: %s' % _url)
        if response.status_code == 200:
            obj = response.json()
            if 'success' in obj and obj['success']:
                return obj['businessObject']
            elif not check_token:
                self._request_token()
                self._request(url, True)
            else:
                raise RequestAPIError('施工调度接口,请求%s地址失败' % _url)
        elif response.status_code == 404:
            raise NotFound404(response.text)
        else:
            raise ValueError('状态码未知')

    def construction_plans(self, line_id, depot_id, word_date):
        work_date_start = int(time.mktime(word_date.timetuple())) * 1000
        work_date_end = work_date_start + PLAN_RANGE_MILLISECOND
        url = '/plPlan/queryPlanByDepot?lineId=%s&depotId=%s&workDate=%s&endWorkDate=%s' % (
            line_id, depot_id, work_date_start, work_date_end)
        data = self._request(url) or []
        return data

    def construction_work_area_status(self, line_id, location_id, area_ids=None):
        url = '/bsdWorkarea/queryWorkareaByDepot?lineId=%s&depotId=%s' % (line_id, location_id)
        if area_ids:
            url += '&workAreaIds=%s' % (','.join(area_ids))
        data = self._request(url) or []
        return data

    def construction_power_area_status(self, line_id, location_id):
        url = '/bsdPowerarea/queryPowerareaByDepot?lineId=%s&depotId=%s' % (line_id, location_id)
        data = self._request(url)
        return data

    def construction_work_plan_status(self, line_id, depot_id, word_date):
        work_date_start = int(time.mktime(word_date.timetuple())) * 1000
        work_date_end = work_date_start + PLAN_RANGE_MILLISECOND
        url = '/plPlan/queryPlanStateByDepot?lineId=%s&depotId=%s&workDate=%s&endWorkDate=%s' % (
            line_id, depot_id, work_date_start, work_date_end)
        data = self._request(url) or []
        return data
