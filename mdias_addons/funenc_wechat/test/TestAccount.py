# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestAccount(TransactionCase):

    def setUp(self):
        '''
        测试创建account
        :return:
        '''
        super(TestAccount, self).setUp()

        # create a account
        self.funenc_account = self.env['funenc.wechat.account'].create({
            'name': 'test_funenc',
            'code': 'test_001',
            'corp': 'wwc4cf9cc042245fb4',
            'account_secret': '3CD0M37kCrwMEKfCQ3BGvu6Dg4XknnskhIprSrjpPMw',
        })

    # def test_attendance_in_before_out(self):
    #     # Make sure check_out is before check_in
    #     with self.assertRaises(Exception):
    #         self.my_attend = self.attendance.create({
    #             'employee_id': self.test_employee.id,
    #             'check_in': time.strftime('%Y-%m-10 12:00'),
    #             'check_out': time.strftime('%Y-%m-10 11:00'),
    #         })
