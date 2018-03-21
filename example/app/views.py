from django.shortcuts import render

from futupayments.forms import PaymentForm


def home(request):
    payment_form = None
    order_id = request.GET.get('order_id')
    if order_id:
       payment_form = PaymentForm.create(
           request,
           amount=100,
           order_id=order_id,
           description='Заказ №{}'.format(order_id),
           client_email='test@test.ru',
           client_phone='+7 912 9876543',
           client_name='Иоганн Кристоф Бах',
           meta='Some meta info',
       )
    return render(request, 'home.html', {
       'payment_form': payment_form,
    })
