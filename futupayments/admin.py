# -*- coding: utf-8 -*-
from django.contrib import admin

import models


class PaymentAdmin(admin.ModelAdmin):
    list_display_links = (
        'creation_datetime',
    )
    list_display = (
        'testing',
        'transaction_id',
        'creation_datetime',
        'amount',
        'currency',
        'order_id',
        'state',
        'message',
        'meta',
    )
    readonly_fields = (
        'testing',
        'creation_datetime',
        'transaction_id',
        'amount',
        'currency',
        'order_id',
        'state',
        'message',
        'meta',
    )
    list_filter = (
        'testing',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(models.Payment, PaymentAdmin)
