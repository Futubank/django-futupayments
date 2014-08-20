# -*- coding: utf-8 -*-
from django.db import models


class Payment(models.Model):
    STATE_COMPLETE = 'COMPLETE'
    STATE_FAILED = 'FAILED'

    STATE_CHOICES = (
        (STATE_COMPLETE, 'успешно'),
        (STATE_FAILED, 'ошибка'),
    )

    creation_datetime = models.DateTimeField(
        'время',
        auto_now_add=True,
    )
    transaction_id = models.CharField(
        'ID транзакции в платежном шлюзе',
        max_length=150,
        db_index=True,
    )
    testing = models.BooleanField(
        'тестовая транзакция',
        default=True,
    )
    amount = models.DecimalField(
        'сумма операции',
        max_digits=10,
        decimal_places=2,
    )
    currency = models.CharField(
        'валюта',
        max_length=3,
    )
    order_id = models.CharField(
        'ID операции в магазине',
        max_length=128,
    )
    state = models.CharField(
        'состояние',
        max_length=10,
        choices=STATE_CHOICES,
    )
    message = models.TextField(
        'текст ошибки или сообщение об успешном совершении операции',
        blank=True,
    )
    meta = models.TextField(
        blank=True,
    )

    def is_success(self):
        return self.state == self.STATE_COMPLETE

    def __unicode__(self):
        return '#{0} {1}'.format(self.transaction_id, self.state)

    class Meta:
        ordering = (
            '-creation_datetime',
        )
        verbose_name = 'платёж через Futubank'
        verbose_name_plural = 'платежи через Futubank'
        unique_together = (
            ('state', 'transaction_id'),
        )
