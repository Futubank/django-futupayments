from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import PaymentCallbackForm
from .models import Payment
from . import config


def success(request):
    return render(request, 'futupayments/success.html')


def fail(request):
    return render(request, 'futupayments/fail.html')


@require_POST
@csrf_exempt
def callback(request):
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
        if config.FUTUPAYMENTS_TEST_MODE:
            resp += ': {0}'.format(form.as_p())
        return HttpResponse(resp)

    payment = form.save()
    return HttpResponse('OK{0}'.format(payment.order_id))
