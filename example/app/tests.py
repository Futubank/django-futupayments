# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class TestMainUsage(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(10)

    def test_pay(self):
        self.selenium.get(self.live_server_url+reverse('home')+'?order_id=1')
        self.assertRaises(NoSuchElementException, self.selenium.find_element_by_css_selector, '.errorlist')

        self.selenium.find_element_by_css_selector('[type=submit]').click()
        self.assertEquals(self.selenium.current_url, 'https://secure.futubank.com/testing-pay/')
        self.assertEquals(self.selenium.title, '[ТЕСТ] Оплата покупки')

    def tearDown(self):
        self.selenium.quit()


