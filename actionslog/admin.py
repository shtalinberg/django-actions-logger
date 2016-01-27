# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import LogAction


@admin.register(LogAction)
class LogActionAdmin(admin.ModelAdmin):
    """docstring for  """
    pass

