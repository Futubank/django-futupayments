from django.test import LiveServerTestCase
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse


class TestMainUsage(LiveServerTestCase):
    def setUp(self):
        from selenium import webdriver
        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(10)

    def test_pay(self):
        from selenium.common.exceptions import NoSuchElementException
        self.selenium.get(self.live_server_url + reverse('home') + '?order_id=1')
        self.assertRaises(NoSuchElementException, self.selenium.find_element_by_css_selector, '.errorlist') # noqa

        self.selenium.find_element_by_css_selector('[type=submit]').click()
        self.assertEquals(self.selenium.current_url, 'https://secure.futubank.com/testing-pay/')  # noqa
        self.assertEquals(self.selenium.title, '[ТЕСТ] Оплата покупки')

    def tearDown(self):
        self.selenium.quit()


