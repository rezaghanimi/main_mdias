from odoo import models, fields


class HandoverTrackCondition(models.Model):
    """
        车轨情况
    """

    _name = 'metro_park_production.handover.track_condition'

    track_id = fields.Many2one('metro_park_base.rails_sec', string='股道编号')
    description = fields.Text(string='使用情况')
    track_condition = fields.Many2one('metro_park_production.handover.parker')


class HandoverTrackTypeCondition(models.Model):
    """
        各类型车轨使用情况
    """

    _name = 'metro_park_production.handover.track_type_condition'

    track_type_id = fields.Many2one('metro_park_base.rail_type', string='股道类型')
    description = fields.Text(string='使用情况')
    handover_work_info_id = fields.Many2one('metro_park_production.handover.work_info')


class HandoverTrainStatus(models.Model):
    """
        车状态信息
    """

    _name = 'metro_park_production.handover.train_status'

    train_id = fields.Many2one('metro_park_maintenance.train_dev', string='车辆')

    description = fields.Text(string='备注')


class HandoverTrainStatus(models.Model):
    """
        维修车信息
    """

    _name = 'metro_park_production.handover.maintain_train'

    train_id = fields.Many2one('metro_park_maintenance.train_dev', string='车辆')
    work_content = fields.Char(string="作业内容")
    work_progress = fields.Char(string="作业进度")
    completion_status = fields.Char(string="完成情况")

    description = fields.Text(string='备注')


class HandoverInfoItem(models.Model):
    _name = 'metro_park_production.handover.info_item'

    description = fields.Char(string='内容')
