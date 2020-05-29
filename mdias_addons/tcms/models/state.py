# -*- coding: utf-8 -*-
from odoo import api, models, fields


class Station(models.Model):
    _name = 'tcms.station'

    BigCode = fields.Char('数据编码')
    paraCode = fields.Char('解析编码')
    des = fields.Char('')


class EquipmentEnergy(models.Model):
    _name = 'tcms.equipment_energy'
    _description = 'Tc1/Tc2车记录牵引设备能耗'
    name = fields.Char(string='车号')
    equipment_energy = fields.Char(string='设备能耗')


class StationTemperature(models.Model):
    _name = 'tcms.temperature'
    _description = '客室温度'

    name = fields.Char(string='车号')
    temperature = fields.Char(string='客室温度')


class OperatingModeSignal(models.Model):
    _name = 'tcms.signal'
    _description = '运行模式信号'

    name = fields.Char(string='车号')
    signal = fields.Char(string='运行模式信号')


class OperatingBrakeSignal(models.Model):
    _name = 'tcms.brake_signal'
    _description = '紧急制动信号'

    name = fields.Char(string='车号')
    signal = fields.Char(string='紧急制动信号')


class StateEB(models.Model):
    _name = 'tcms.eb'
    _description = 'EB按钮按下信号'

    name = fields.Char(string='车号')
    signal = fields.Char(string='EB按钮按下信号')


class StateNetwork(models.Model):
    _name = 'tcms.network'
    _description = '网压使能信号'

    name = fields.Char(string='车号')
    signal = fields.Char(string='网压使能信号')


class StateActivateSignal(models.Model):
    _name = 'tcms.activate_signal'
    _description = '列车激活信号'

    name = fields.Char(string='车号')
    TC1 = fields.Char(string='TC1激活')
    TC2 = fields.Char(string='TC2激活')


class TC1CompressorWorkTime(models.Model):
    _name = 'tc1.compressor_work_time'
    _description = 'TC1压缩机工作时间(原值)'

    name = fields.Char(string='车号')
    work_time = fields.Char(string='工作时间')


class TC1CompressorWorkTimeH(models.Model):
    _name = 'tc1.compressor_work_time_h'
    _description = 'TC1压缩机工作时间H'

    name = fields.Char(string='车号')
    work_time = fields.Char(string='工作时间')


class TC1CompressorWorkTimel(models.Model):
    _name = 'tc1.compressor_work_time_l'
    _description = 'TC1压缩机工作时间L'

    name = fields.Char(string='车号')
    work_time = fields.Char(string='工作时间')


class TC2CompressorWorkTime(models.Model):
    _name = 'tc2.compressor_work_time'
    _description = 'TC2压缩机工作时间(原值)'

    name = fields.Char(string='车号')
    work_time = fields.Char(string='工作时间')


class TC2CompressorWorkTimeH(models.Model):
    _name = 'tc2.compressor_work_time_h'
    _description = 'TC2压缩机工作时间(H)'

    name = fields.Char(string='车号')
    work_time = fields.Char(string='工作时间')


class TC2CompressorWorkTimeL(models.Model):
    _name = 'tc2.compressor_work_time_l'
    _description = 'TC2压缩机工作时间(原值)'

    name = fields.Char(string='车号')
    work_time = fields.Char(string='工作时间')


class TcmsWorkTime(models.Model):
    _name = 'tcms.compressor_work_time'
    _description = '当日TCMS工作时间'

    name = fields.Char(string='车号')
    work_time = fields.Char(string='工作时间')


class RenewableElectricityH(models.Model):
    _name = 'renewable_electricity_h'
    _description = '再生电量H'

    name = fields.Char(string='车号')
    electricity = fields.Char(string='电量')


class RenewableElectricityL(models.Model):
    _name = 'renewable_electricity_l'
    _description = '再生电量L'

    name = fields.Char(string='车号')
    electricity = fields.Char(string='电量')


class AuxiliaryPowerConsumptionH(models.Model):
    _name = 'auxiliary_power_consumption_h'
    _description = '辅助能耗H'

    name = fields.Char(string='车号')
    consumption = fields.Char(string='能耗')


class AuxiliaryPowerConsumptionL(models.Model):
    _name = 'auxiliary_power_consumption_l'
    _description = '辅助能耗L'

    name = fields.Char(string='车号')
    consumption = fields.Char(string='能耗')


class PressureSwitch(models.Model):
    _name = 'tcms.pressure_switch'
    _description = '总风压力旁路开关'

    name = fields.Char(string='车号')
    switch = fields.Char(string='总风压力旁路开关')


class StopBrakeSideSwitch(models.Model):
    _name = 'stop_brake_side_switch'
    _description = '停放制动旁路开关'

    name = fields.Char(string='车号')
    switch = fields.Char(string='停放制动旁路开关')


class StopNoEaseSideSwitch(models.Model):
    _name = 'stop_no_ease_side_switch'
    _description = '制动不缓解旁路开关'

    name = fields.Char(string='车号')
    switch = fields.Char(string='制动不缓解旁路开关')


class TrainCloseSideSwitch(models.Model):
    _name = 'train_close_side_switch'
    _description = '列车门全关闭旁路开关'

    name = fields.Char(string='车号')
    switch = fields.Char(string='制动不缓解旁路开关')


class TrainCompleteSideSwitch(models.Model):
    _name = 'train_complete_side_switch'
    _description = '列车完整性旁路开关'

    name = fields.Char(string='车号')
    switch = fields.Char(string='制动不缓解旁路开关')


class BatteryBusVoltagePara(models.Model):
    _name = 'battery_bus_voltage_switch'
    _description = '蓄电池母线电压'

    name = fields.Char(string='车号')
    voltage = fields.Char(string='电压')


class BatteryBusCurrentPara(models.Model):
    _name = 'battery_bus_current_switch'
    _description = '蓄电池母线电流'

    name = fields.Char(string='车号')
    current = fields.Char(string='电流')
