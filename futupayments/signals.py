# -*- coding: utf-8 -*-

from django.dispatch import Signal


on_callback = Signal(providing_args=['success'])
