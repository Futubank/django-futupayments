# -*- coding: utf-8 -*-
from django.contrib import admin

import models


class PaymentAdmin(admin.ModelAdmin):
    list_display_links = (
        'creation_datetime',
    )
    list_display = (
        'transaction_id',
        'creation_datetime',
        'amount',
        'order_id',
        'state',
        'response_message',
        'meta',
    )

    readonly_fields = (
        'creation_datetime',
        'transaction_id',
        'amount',
        'order_id',
        'state',
        'response_message',
        'meta',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(models.Payment, PaymentAdmin)
