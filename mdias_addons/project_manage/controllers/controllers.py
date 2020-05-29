# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import exceptions

import logging
import json

_logger = logging.getLogger(__name__)


class ProjectManage(http.Controller):
    '''
    接口
    '''
    @http.route('/api/project_manage/list', auth='user')
    def get_project(self, **kw):
        '''
        取得所有的项目
        :param kw:
        :return:
        '''
        rst = {
            'data': {
                'list': [],
            }
        }
        try:
            rst['errcode'] = 0
            page_num = int(request.params['pageNum']) - 1
            page_size = int(request.params['pageSize'])
            query = request.params['query']
            model = http.request.env['project_manage.project_manage']
            domain = []
            if query and query != '':
                domain.append(('name', 'like', query))
            _logger.info('the domain is {domain} and the page size is {page_size} and the page_num is {page_num}'
                         .format(domain=domain, page_num=page_num, page_size=page_size))
            records = model.search(domain, limit=page_size, offset=page_size * page_num)
            rst['data'] = {
                'list': []
            }
            for record in records:
                rst['data']['list'].append({
                    'id': record.id,
                    'name': record.name,
                    'progress': record.cur_progress
                })
        except Exception as ec:
            rst['data']['list'] = []
            rst['errcode'] = 500
            rst['msg'] = str(ec)
            _logger.info(ec)

        _logger.info(rst)
        return json.dumps(rst)

    @http.route('/api/project_manage/detail', auth='user')
    def get_project_info(self, **kw):
        '''
        取得项目信息
        :param kw:
        :return:
        '''
        rst = dict()
        try:
            rst['errcode'] = 0
            rst['msg'] = 'success'
            project_id = int(request.params['id'])
            if not project_id:
                raise exceptions.ValidationError('参数不正确')
            model = http.request.env['project_manage.project_manage']
            record = model.browse(project_id)
            rst['data'] = {
                'begin': str(record.plan_start_date),
                'description': str(record.project_info),
                'end': str(record.finish_date),
                'id': record.id,
                'name': record.name,
                'progress': record.cur_progress,
                'contents': record.report_content.read(['id', 'content'])
            }
        except Exception as ec:
            rst['data'] = []
            rst['errcode'] = 500
            rst['msg'] = str(ec)
            _logger.info(ec)
        _logger.info(rst)
        return json.dumps(rst)

    @http.route('/api/project_manage/user_info', auth='user')
    def get_project_info(self, **kw):
        '''
        获取登陆用户的信息
        :param kw:
        :return:
        '''
        rst = dict()
        try:
            user = http.request.env.user
            rst['data'] = {
                "name": user.name,
                "userid": user.login
            }
            rst['errcode'] = 0
            rst['msg'] = 'success'
        except Exception as ec:
            rst['data'] = []
            rst['errcode'] = 500
            rst['msg'] = str(ec)
            _logger.info(ec)
        _logger.info(rst)
        return json.dumps(rst)
