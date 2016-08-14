# coding:utf-8

from unittest import TestCase
from phone import Phone


class TestPhone(TestCase):

    def setUp(self):
        self.p = Phone()

    def tearDown(self):
        pass

    def test_get_phone_no_type(self):

        self.assertEqual(self.p.get_phone_no_type(1), '移动')
        self.assertEqual(self.p.get_phone_no_type(2), '联通')
        self.assertEqual(self.p.get_phone_no_type(3), '电信')
        self.assertEqual(self.p.get_phone_no_type(6), '移动虚拟运营商')
        self.assertEqual(self.p.get_phone_no_type(5), '联通虚拟运营商')
        self.assertEqual(self.p.get_phone_no_type(4), '电信虚拟运营商')
        self.assertEqual(self.p.get_phone_no_type(7), None)

    def test_find_on_assert_error(self):

        try:
            self.p.find(123)
            self.assertTrue(False)
        except AssertionError:
            pass

    def test_find_on_ok(self):

        res = self.p.find(1521147)
        self.assertEqual(res['zip_code'], '421000')
        self.assertEqual(res['area_code'], '0734')
        self.assertEqual(res['city'], '衡阳')
        self.assertEqual(res['province'], '湖南')
        self.assertEqual(res['phone_type'], '移动')

    def test_find_on_no_res(self):

        res = self.p.find(1991147)
        self.assertEqual(res, None)


