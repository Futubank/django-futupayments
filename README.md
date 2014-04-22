django-futupayments
===================

Приём платежей с пластиковых карт через Futubank.com

Установка
=========
Ставим пакет:

```
pip install -e git+https://github.com/shantilabs/django-futupayments.git#egg=futupayments
```

Базовая настройка
=================

settings.py:

```python
# эти значения можно получить в личном кабинете Futubank'а
FUTUPAYMENTS_MERCHANT_ID = id_вашего_магазина
FUTUPAYMENTS_SECRET_KEY = "секретный ключ вашего магазина"

INSTALLED_APPS = (
  # ...
  'futupayments',
)
```

Простой пример использования
============================
Делаем простенькую страничку для перечисления 100 рублей. Сначала views.py:

```python
def my_view(request):
   # внутри config зовётся reverse(), поэтому импорт локальный
   from futupayments.forms import PaymentForm
   from futupayments.config import FUTUPAYMENTS_URL
   order_id = 12345
   payment_form = PaymentForm.create(
       request,
       # перечисление 100 рублей
       amount=100,
       # номер заказа – поле обязательное и уникальное
       order_id=order_id,
       # описание в свободной форме
       description=u'Заказ №{0}'.format(order_id),
   )
   return render(request, 'my_template.html', {
       'payment_form_url': FUTUPAYMENTS_URL,
       'payment_form': payment_form,
   })
```

Шаблон, templates/my_template.html:

```html
<form method="post" action="{{ payment_form_url }}">
    {{ payment_form }}
    <input type="submit" value="Перевести {{ payment_form.cleaned_data.amount }} {{ payment_form.cleaned_data.currency }} за заказ №{{ payment_form.cleaned_data.order_id }}">
</form>
```

Настройка уведомлений о платежах
================================
Чтобы работали уведомления о платежах, во-первых, добавляем в urls.py обработчик callback'ов:

```python
urlpatterns = patterns(
    # ...
    url('^futupayments/', include('futupayments.urls')),
)
```

Получившийся URL — **http://вашсайт/futupayments/** надо прописать в личном кабинете Futubank'а.

Теперь после каждой транзакции будет создаваться новый экземляр futupayments.models.Payment. Чтобы отслеживать
поступления платежей, можно воспользоваться сигналами:

```python
from futupayments.models import Payment

@receiver(post_save, sender=[Payment])
def on_new_payment(sender, instance, **kwargs):
    if instance.is_success():
        logging.info(
            u'поступила оплата заказа #%s в размере %s (транзакция #%s)',
            instance.order_id,
            instance.amount,
            instance.transaction_id,
        )

```