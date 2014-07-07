from __future__ import absolute_import
from django.http import HttpResponse, Http404
from django.shortcuts import render

from .forms import PaymentCallbackForm
from .models import Payment


def success(request):
    return render(request, 'futupayments/success.html')


def fail(request):
    return render(request, 'futupayments/fail.html')


def callback(request):
    if request.method.lower() != 'post':
        raise Http404
    try:
        payment = Payment.objects.get(
            transaction_id=request.POST.get('transaction_id'),
            state=request.POST.get('state'),
        )
    except (ValueError, TypeError, Payment.DoesNotExist):
        payment = None

    form = PaymentCallbackForm(request.POST, instance=payment)
    if not form.is_valid():
        resp = 'FAIL'
        from . import config
        if config.FUTUPAYMENTS_TEST_MODE:
            resp += u': {0}'.format(form.as_p())
        return HttpResponse(resp)

    payment = form.save()
    return HttpResponse(u'OK{0}'.format(payment.order_id))
