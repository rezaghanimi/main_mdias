# -*- coding: utf-8 -*-
import base64
import json

import pendulum
import werkzeug.exceptions
from odoo.addons.web.controllers.main import serialize_exception

from odoo import http
from odoo.http import request


class MetroParkProduction(http.Controller):
    @http.route('/maintenance/large_screen/get_msg', type='http', auth='public', csrf=False)
    def get_img_no(self, location_id=None, **kwargs):
        """
        取得大屏信息
        :return:
        """
        result = http.request.env['metro_park_production.screen.page']\
            .sudo().request_data(location_id)
        return json.dumps(result)

    @http.route('/production/files/upload', type='http', auth='user', csrf=False, method=['POST'])
    def upload_files(self, **kwargs):
        file = kwargs['file']
        file_name = file.filename
        content = base64.b64encode(file.read())
        type_id = int(kwargs['file_type'])
        http.request.env['metro_park_production.files'].create({
            'file_name': file_name,
            'file_size': '',
            'file_content': content,
            'file_type_id': type_id
        })
        return

    @http.route('/metro_park_production/upload_video_for_scene', type='http', auth="none", csrf=False)
    @serialize_exception
    def upload_video_for_scene(self, machine_name, ufile):
        files = request.httprequest.files.getlist('ufile')
        Model = request.env['ir.attachment']
        video_model_name = 'metro_park_production.video'
        now = pendulum.now()
        field_name = '%s/%s/%s' % (machine_name, now.date(), now.hour)
        for ufile in files:

            video = request.env[video_model_name].sudo().create({
                'machine_name': machine_name,
                'ip': request.httprequest.environ.get("REMOTE_ADDR", '')
            })
            try:
                attachment = Model.sudo().create({
                    'name': field_name,
                    'datas': base64.encodebytes(ufile.read()),
                    'datas_fname': field_name,
                    'res_model': video_model_name,
                    'res_id': video.id
                })
                video.write({
                    'attachment_id': attachment.id
                })
                attachment._post_add_create()
            except Exception:
                return json.dumps({
                    'status': 404
                })
        return json.dumps({
            'status': 200
        })

    @http.route('/metro_park_production/video_stream', type='http', auth="none", csrf=False)
    def video_stream(self, attachment_video_id):
        """
            视频流的请求方式, 相关信息参照https协议: Accept-Ranges ， Content-Range 请求头
        :param attachment_video_id: 附件id,
            附件应该是一个视频类型文件<mp4>, 目前前端组件仅仅对mp4 文件进行了处理
        :return: response
        """
        try:
            attachment_id = request.env['ir.attachment'].search([('id', '=', attachment_video_id)])
            if not attachment_id:
                return http.Response(status=404)
            stream = attachment_id.datas
            content_base64 = base64.b64decode(stream)
            headers = [

                ("Accept-Ranges", 'bytes'),
                ("Content-Disposition", 'attachment; filename="{}"'.format(attachment_id.name)),

            ]
            status = 200
            hrange = request.httprequest.range
            # 通过数据流的方式请求
            if hrange:
                ranges = hrange.ranges[0]
                # 这里仅仅正对单个请求片,多个未处理
                if not ranges[0] and not ranges[1]:
                    # 这里是开始请求[0, None]
                    block_content_base64 = content_base64
                    len_content = len(block_content_base64)
                    headers += [('Content-Type', 'video/mp4'), ('Content-Length', len(block_content_base64)),
                                ('Content-Range', ' bytes %s-%s/%s' % (0, len_content, len_content))]
                else:
                    headers.append(('Content-Type','application/octet-stream'))
                    if not ranges[1]:
                        # [x:None]
                        block_content_base64 = content_base64[ranges[0]:]
                        len_content = len(block_content_base64)
                        headers += [('Content-Length', len(block_content_base64)),
                                    ('Content-Range', ' bytes %s-%s/%s' % (ranges[0], len_content, len_content))]
                    elif not ranges[0]:
                        # [None, x]
                        block_content_base64 = content_base64[:ranges[1]+1]
                        len_content = len(block_content_base64)
                        headers += [('Content-Length', len(block_content_base64)),
                                    ('Content-Range', ' bytes %s-%s/%s' % (0, len_content, len_content))]
                    else:
                        # [x:x]
                        block_content_base64 = content_base64[ranges[0]:ranges[1] + 1]
                        headers += [('Content-Length', len(block_content_base64)),
                                    ('Content-Range', ' bytes %s-%s/%s' % (ranges[10], ranges[1], len(block_content_base64)))]

            else:
                # 直接返回整个文件
                block_content_base64 = content_base64
                headers += [('Content-Length', len(block_content_base64)),('Content-Type', 'video/mp4'),
                            ('Content-Range', ' bytes 0-%s/%s' % (block_content_base64, block_content_base64))]
            response = werkzeug.wrappers.Response(block_content_base64,
                                                  headers=headers,
                                                  direct_passthrough=True,
                                                  status=status
                                                  )
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            return http.Response(status=404)
