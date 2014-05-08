# -*- coding: utf-8 -*-
from django.db import models


class Payment(models.Model):
    STATE_COMPLETE = 'COMPLETE'
    STATE_FAILED = 'FAILED'

    STATE_CHOICES = (
        (STATE_COMPLETE, u'успешно'),
        (STATE_FAILED, u'ошибка'),
    )

    creation_datetime = models.DateTimeField(
        u'время',
        auto_now_add=True,
    )
    transaction_id = models.BigIntegerField(
        u'ID транзакции в платежном шлюзе',
        db_index=True,
    )
    testing = models.BooleanField(
        u'тестовая транзакция',
        default=True,
    )
    amount = models.DecimalField(
        u'сумма операции',
        max_digits=10,
        decimal_places=2,
    )
    currency = models.CharField(
        u'валюта',
        max_length=3,
    )
    order_id = models.CharField(
        u'ID операции в магазине',
        max_length=128,
    )
    state = models.CharField(
        u'состояние',
        max_length=10,
        choices=STATE_CHOICES,
    )
    message = models.TextField(
        u'текст ошибки или сообщение об успешном совершении операции',
        blank=True,
    )
    meta = models.TextField(
        blank=True,
    )

    def is_success(self):
        return self.state == self.STATE_COMPLETE

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
