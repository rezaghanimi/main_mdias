
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PreDateTrainInfos(models.Model):
    '''
    车辆上一日位置
    '''
    _name = 'metro_park_maintenance.pre_date_train_infos'

    train = fields.Many2one(string='车辆',
                            comodel_name='metro_park_maintenance.train_dev')
    train_no = fields.Char(string="车号", related='train.dev_no')
    location = fields.Many2one(string='位置',
                               comodel_name='metro_park_base.location')
    rail = fields.Many2one(string='区段',
                           comodel_name='metro_park_base.rails_sec',
                           domain="[('location', '=', location)]")
    # 里程相关信息
    miles = fields.Float(string="里程数")
    last_mile_repair_date = fields.Date(string="上次里程检日期")
    last_repair_miles = fields.Float(string="上次里程检公里数")
    miles_after_last_repair = fields.Float(string="上次里程后公里数",
                                           compute="_compute_miles_after_last_repair")

    @api.depends("miles", "last_repair_miles")
    def _compute_miles_after_last_repair(self):
        '''
        计算距离上次里程公里数
        :return:
        '''
        for record in self:
            record.miles_after_last_repair = record.miles - record.last_repair_miles


class PreDateWizardTrainInfos(models.TransientModel):
    '''
    车辆上一日位置, 和上边模型一样，用于向导添加数据
    '''
    _name = 'metro_park_maintenance.pre_date_wizard_train_infos'

    train = fields.Many2one(string='车辆',
                            comodel_name='metro_park_maintenance.train_dev')
    train_no = fields.Char(string="车号", related='train.dev_no')
    location = fields.Many2one(string='位置',
                               comodel_name='metro_park_base.location')
    rail = fields.Many2one(string='区段',
                           comodel_name='metro_park_base.rails_sec',
                           domain="[('location', '=', location)]")

    # 里程相关信息
    miles = fields.Float(string="里程数")
    last_mile_repair_date = fields.Date(string="上次里程检日期")
    last_repair_miles = fields.Float(string="上次里程检公里数")
    miles_after_last_repair = fields.Float(string="上次里程后公里数", compute="_compute_miles_after_last_repair")

    @api.depends("miles", "last_repair_miles")
    def _compute_miles_after_last_repair(self):
        '''
        计算距离上次里程公里数
        :return:
        '''
        for record in self:
            record.miles_after_last_repair = record.miles - record.last_repair_miles

