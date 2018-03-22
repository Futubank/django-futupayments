django-futupayments
===================

[![Build Status](https://travis-ci.org/Futubank/django-futupayments.svg?branch=master)](https://travis-ci.org/Futubank/django-futupayments)
[![Latest Version](https://img.shields.io/pypi/v/django-futupayments.svg?label=version)](https://pypi.python.org/pypi/django-futupayments/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/django-futupayments.svg)](https://pypi.python.org/pypi/django-futupayments/)
[![Development Status](https://img.shields.io/pypi/status/django-futupayments.svg)](https://pypi.python.org/pypi/django-futupayments/)
[![Supported Django versions](http://img.shields.io/badge/Django-%201.7-green.svg)](https://travis-ci.org/Futubank/django-futupayments)


Django-приложение для приёма платежей с банковских карт через Futubank.com.


Установка
=========
Ставим пакет:

```
pip install django-futupayments

```

После добавления futupayments в INSTALLED_APPS
```
python manage.py migrate
```

Базовая настройка
=================

settings.py:

```python
# подключаем приложение
INSTALLED_APPS = (
  # ...
  'futupayments',
)

# работаем в тестовом режиме
FUTUPAYMENTS_TEST_MODE = True

# эти значения можно получить в личном кабинете Futubank'а
FUTUPAYMENTS_MERCHANT_ID = "id_вашего_магазина"
FUTUPAYMENTS_SECRET_KEY = "секретный ключ вашего магазина"

```

Простой пример использования
============================
Делаем простенькую страничку для перечисления 100 рублей. Сначала `views.py`:

```python
from futupayments.forms import PaymentForm

def my_view(request):
   order_id = 12345
   payment_form = PaymentForm.create(
       request,
       # перечисление 100 рублей
       amount=100,
       # номер заказа – поле обязательное и уникальное
       order_id=order_id,
       # описание в свободной форме
       description=u'Заказ №{0}'.format(order_id),
       # данные клиента (если они есть)
       client_email='test@test.ru',
       client_phone='+7 912 9876543',
       client_name=u'Иоганн Кристоф Бах',
   )
   return render(request, 'my_template.html', {
       'payment_form': payment_form,
   })
```

Шаблон, `templates/my_template.html`:

```html
<form method="post" action="{{ payment_form.action }}">
    {{ payment_form }}
    <input type="submit" value="Перевести {{ payment_form.cleaned_data.amount }} {{ payment_form.cleaned_data.currency }} за заказ №{{ payment_form.cleaned_data.order_id }}">
</form>
```

Настройка уведомлений о платежах
================================
Чтобы работали уведомления о платежах, во-первых, добавляем в `urls.py` обработчик callback'ов:

```python
urlpatterns = [
    # ...
    url('^futupayments/', include('futupayments.urls')),
]
```

Получившийся URL — `http://вашсайт/futupayments/callback` надо прописать в личном кабинете Futubank'
(https://secure.futubank.com) на вкладке «Уведомления о транзакциях» в пункте «Уведомления с помощью POST-запросов».

Теперь после каждой транзакции будет создаваться новый экземпляр `futupayments.models.Payment`. Чтобы отслеживать
поступления платежей, можно воспользоваться сигналами:

```python
from futupayments.signals import on_callback

@receiver(on_callback)
def on_new_payment(sender, success, **kwargs):
    if success and sender.is_success():
        logging.info(
            u'поступила оплата заказа #%s в размере %s (транзакция #%s)',
            sender.order_id,
            sender.amount,
            sender.transaction_id,
        )

```
