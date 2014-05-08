# -*- coding: utf-8 -*-
import random
import string
import time
import base64
from hashlib import sha1

from django import forms
from django.core.exceptions import ValidationError
from futupayments.models import Payment


class PaymentCallbackForm(forms.ModelForm):
    timestamp = forms.CharField()
    salt = forms.CharField()
    signature = forms.CharField()

    def clean(self):
        from futupayments import config
        key = config.FUTUPAYMENTS_SECRET_KEY
        data = self.cleaned_data
        if self.cleaned_data['signature'] != get_signature(key, data):
            raise ValidationError('Incorrect signature')
        return self.cleaned_data

    class Meta:
        model = Payment
        exclude = (
            'creation_datetime',
        )


class PaymentForm(forms.Form):
    MAX_DESCRIPTION_LENGTH = 250

    @classmethod
    def create(cls, request, amount, order_id, description,
               client_email='', client_phone='', meta=None,
               cancel_url=None):
        from futupayments import config
        data = {
            'amount': amount,
            'description': description[:cls.MAX_DESCRIPTION_LENGTH],
            'order_id': str(order_id),
            'cancel_url': cancel_url or request.build_absolute_uri(),
            'meta': meta or '',
            'currency': 'RUB',
            'client_email': client_email,
            'client_phone': client_phone,
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
        }
        key = config.FUTUPAYMENTS_SECRET_KEY
        data['signature'] = get_signature(key, data)
        form = cls(data)
        assert form.is_valid(), form.as_p()
        return form

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
    client_phone = forms.CharField(widget=forms.HiddenInput, required=False,
                                   min_length=10, max_length=30)
    signature = forms.CharField(widget=forms.HiddenInput)


def get_signature(secret_key, params):
    u"""
    >>> params = {
    ...     "merchant": 43210,
    ...     "amount": '174.7',
    ...     "currency": 'RUB',
    ...     "description": u'Заказ №73138754',
    ...     "order_id": '73138754',
    ...     "success_url": 'http://myshop.ru/success/',
    ...     "fail_url": 'http://myshop.ru/fail/',
    ...     "cancel_url": 'http://myshop.ru/cart/',
    ...     "signature": '',
    ...     "timestamp": '20140418151950',
    ...     "meta": '{"tracking": 1234}',
    ...     "salt": '00000000000000000000000000000000',
    ... }
    >>> get_signature('C0FFEE', params)
    'cb3743cc37d87f5a4255fc3a99c223c0e869c145'
    """
    return double_sha1(secret_key, '&'.join(
        force_str(k) + '=' + base64.b64encode(force_str(params[k]))
        for k in sorted(params)
        if params[k] and k != 'signature'
    ))


def force_str(v):
    return v.encode('utf-8') if isinstance(v, unicode) else str(v)


def double_sha1(secret_key, s):
    """
    >>> double_sha1('C0FFEE', 'example')
    '27d204596505ff298ca79fb3bb949501cd7b2fa7'
    """
    for i in range(2):
        s = sha1(secret_key + s).hexdigest()
    return s


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print 'doctests passed'
