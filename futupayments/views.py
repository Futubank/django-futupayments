from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from futupayments.forms import PaymentCallbackForm
from futupayments.models import Payment


def success(request):
    return render(request, 'futupayments/success.html')


def fail(request):
    return render(request, 'futupayments/fail.html')


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
        if settings.DEBUG:
            resp += u': {0}'.format(form.as_p())
        return HttpResponse(resp)

    payment = form.save()
    return HttpResponse(u'OK: #{0}'.format(payment.transaction_id))
