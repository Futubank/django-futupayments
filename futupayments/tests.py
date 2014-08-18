# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import time
from unittest import skipIf
from random import randint

from django.test import TestCase
from django.http import HttpRequest
try:
    from django.test.utils import override_settings
except ImportError:
    override_settings = False
from .forms import *
from .forms import get_signature, double_sha1


class TestFormsCase(TestCase):

    def test_paymentform_creation_with_simple_data(self):
        responce = HttpRequest()
        responce.META['SERVER_NAME'] = 'test.com'
        responce.META['SERVER_PORT'] = '80'
        order = randint(1, 99999999)
        form = PaymentForm.create(
            responce,
            amount=100,
            order_id=order,
            description='Заказ №{}'.format(order),
        )
        form = form.as_p()

        self.assertNotIn('error', form)
        self.assertIn('test.com', form)
        self.assertIn('100', form)
        self.assertIn('Заказ №', form)
        self.assertIn('currency', form)
        self.assertIn('unix_timestamp', form)
        self.assertIn('salt', form)
        self.assertIn('sysinfo', form)
        self.assertIn('signature', form)
        self.assertIn(str(int(time.time()))[:-1], form)

    def test_paymentform_creation_with_full_data(self):
        responce = HttpRequest()
        responce.META['SERVER_NAME'] = 'test.com'
        responce.META['SERVER_PORT'] = '80'
        order = randint(1, 99999999)
        form = PaymentForm.create(
            responce,
            amount=100,
            order_id=order,
            description='Заказ №{}'.format(order),
            client_email='test@test.ru',
            client_phone='+7 912 9876543',
            client_name='Иоганн Кристоф Бах',
            cancel_url='cancel/url',
            meta='Some meta info',
        )
        form = form.as_p()

        self.assertNotIn('error', form)
        self.assertIn('test.com', form)
        self.assertIn('+7 912 9876543', form)
        self.assertIn('test@test.ru', form)
        self.assertIn('Иоганн Кристоф Бах', form)
        self.assertIn('cancel/url', form)
        self.assertIn('Some meta info', form)

    @skipIf((not override_settings), 'django 1.3')
    def test_paymentform_creation_with_settings(self):
        responce = HttpRequest()
        responce.META['SERVER_NAME'] = 'test.com'
        responce.META['SERVER_PORT'] = '80'

        order = randint(1, 99999999)

        with override_settings(
                FUTUPAYMENTS_SUCCESS_URL='/uniq_success',
                FUTUPAYMENTS_FAIL_URL='uniq_fail',
                FUTUPAYMENTS_TEST_MODE=True,
            ):
            form = PaymentForm.create(
                responce,
                amount=100,
                order_id=order,
                description='Заказ №{}'.format(order),
                client_email='test@test.ru',
                client_phone='+7 912 9876543',
                client_name='Иоганн Кристоф Бах',
                cancel_url='cancel/url',
                meta='Some meta info',
            )

        form = form.as_p()

        self.assertIn('uniq_fail', form)
        self.assertIn('uniq_success', form)


class TestUtilsCase(TestCase):

    def test_get_signature(self):
        self.assertEqual(get_signature('secret_key', {'param1': 'тест', 'param2': 2, 'param3': 'test'}),
                          '0d86fe6782bd0c6a75ed77692791f8ca6681445f')

    def test_double_sha1(self):
        self.assertEqual(double_sha1('secret_key', 'привет hi'), 'd9aa509a9e9b296bceaa4dbc0ea64d81b5a04836')
