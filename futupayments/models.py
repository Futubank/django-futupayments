# -*- coding: utf-8 -*-
from django.db import models


class Payment(models.Model):
    STATE_COMPLETE = 'COMPLETE'
    STATE_FAILED = 'FAILED'

    state_codes = (
        (STATE_COMPLETE, u'успешно'),
        (STATE_FAILED, u'ошибка'),
    )

    creation_datetime = models.DateTimeField(u'время', auto_now_add=True)
    transaction_id = models.BigIntegerField(u'ID транзакции в платежном шлюзе', db_index=True)
    amount = models.DecimalField(u'сумма операции',
                                 max_digits=10, decimal_places=2)
    order_id = models.CharField(u'ID операции в магазине', max_length=128)
    state = models.CharField(max_length=10, choices=state_codes)
    response_message = models.TextField(
        help_text=u'текст ошибки или сообщение об успешном совершении операции',
    )
    meta = models.TextField(blank=True, default='')

    def is_success(self):
        return self.state is self.STATE_COMPLETE

    def __unicode__(self):
        return u'#{0} {1}'.format(self.transaction_id, self.state)

    class Meta:
        ordering = (
            '-creation_datetime',
        )
        verbose_name = u'платёж через Futubank'
        verbose_name_plural = u'платежи через Futubank'
        unique_together = (
            ('state', 'transaction_id'),
        )
