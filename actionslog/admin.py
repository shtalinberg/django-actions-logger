# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import LogAction


@admin.register(LogAction)
class LogActionAdmin(admin.ModelAdmin):
    """docstring for  """
    list_display = ('id', 'created_at','remote_ip', 'user', 'action', 'object_repr')
    search_fields = ['user__email', 'remote_ip']

    date_hierarchy = 'created_at'
    list_filter = ('action', 'created_at',)
