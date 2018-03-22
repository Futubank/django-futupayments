import base64
import hashlib
import json
import platform
import random
import string
import time

import django
from django import forms
from django.core.exceptions import ValidationError

from . import config, get_version
from .models import Payment

__all__ = ['PaymentForm', 'PaymentCallbackForm']


class PaymentCallbackForm(forms.ModelForm):
    testing = forms.CharField(required=False)

    def clean(self):
        key = config.FUTUPAYMENTS_SECRET_KEY
        data = dict(self.data.items())
        signature = data.pop('signature') if 'signature' in self.data else None
        if signature != get_signature(key, data):
            raise ValidationError('Incorrect signature')
        self.cleaned_data['testing'] = self.cleaned_data.get('testing') == '1'
        return self.cleaned_data

    class Meta:
        model = Payment
        fields = (
            'transaction_id',
            'testing',
            'amount',
            'currency',
            'order_id',
            'state',
            'message',
            'meta',
        )


class PaymentForm(forms.Form):
    MAX_DESCRIPTION_LENGTH = 250

    @classmethod
    def create(
        cls,
        request,
        amount,
        order_id,
        description,
        client_email='',
        client_phone='',
        client_name='',
        meta=None,
        cancel_url=None,
        testing=None,
    ):
        if (
            cancel_url is not None and
            not cancel_url.lower().startswith(('http://', 'https://'))
        ):
            cancel_url = request.build_absolute_uri(cancel_url)

        if testing is None:
            testing = config.FUTUPAYMENTS_TEST_MODE

        data = {
            'testing': str(int(testing)),
            'amount': amount,
            'description': description[:cls.MAX_DESCRIPTION_LENGTH],
            'order_id': str(order_id),
            'cancel_url': cancel_url or request.build_absolute_uri(),
            'meta': meta or '',
            'currency': 'RUB',
            'client_email': client_email,
            'client_phone': client_phone,
            'client_name': client_name,
            'salt': ''.join(
                random.choice(string.ascii_letters)
                for _ in range(32)
            ),
            'unix_timestamp': int(time.time()),
            'merchant': config.FUTUPAYMENTS_MERCHANT_ID,
            'fail_url': request.build_absolute_uri(
                config.FUTUPAYMENTS_FAIL_URL,
            ),
            'success_url': request.build_absolute_uri(
                config.FUTUPAYMENTS_SUCCESS_URL,
            ),
            'sysinfo': json.dumps({
                'json_enabled': True,
                'language': 'Python {}'.format(platform.python_version()),
                'plugin': 'django - futupayments v.{}'.format(get_version()),
                'cms': 'Django Framework v.{}'.format(django.get_version()),
            }),
        }
        data['signature'] = get_signature(config.FUTUPAYMENTS_SECRET_KEY, data)
        form = cls(data)
        form.action = config.FUTUPAYMENTS_HOST + '/pay'
        assert form.is_valid(), form.as_p()
        return form

    testing = forms.CharField(widget=forms.HiddenInput)
    merchant = forms.CharField(widget=forms.HiddenInput)
    amount = forms.DecimalField(widget=forms.HiddenInput)
    currency = forms.CharField(widget=forms.HiddenInput)
    description = forms.CharField(widget=forms.HiddenInput, required=False,
                                  max_length=MAX_DESCRIPTION_LENGTH)
    meta = forms.CharField(widget=forms.HiddenInput, required=False)
    order_id = forms.CharField(widget=forms.HiddenInput)
    success_url = forms.URLField(widget=forms.HiddenInput)
    fail_url = forms.URLField(widget=forms.HiddenInput)
    cancel_url = forms.URLField(widget=forms.HiddenInput)
    unix_timestamp = forms.IntegerField(widget=forms.HiddenInput)
    salt = forms.CharField(widget=forms.HiddenInput)
    client_email = forms.EmailField(widget=forms.HiddenInput, required=False)
    client_phone = forms.CharField(widget=forms.HiddenInput, required=False, max_length=30)  # noqa
    client_name = forms.CharField(widget=forms.HiddenInput, required=False)
    sysinfo = forms.CharField(max_length=255, widget=forms.HiddenInput, required=False)  # noqa
    signature = forms.CharField(widget=forms.HiddenInput)


def get_signature(secret_key: str, params: dict) -> str:
    return double_sha1(secret_key, '&'.join(
        '='.join((k, base64.b64encode(str(params[k]).encode()).decode()))
        for k in sorted(params)
        if params[k] and k != 'signature'
    ))


def double_sha1(secret_key: str, s: str) -> str:
    secret_key = secret_key.encode()
    for i in range(2):
        s = s.encode()
        s = hashlib.sha1(secret_key + s).hexdigest()
    return s
