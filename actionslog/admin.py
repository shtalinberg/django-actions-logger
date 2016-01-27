# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import LogAction


@admin.register(LogAction)
class LogActionAdmin(admin.ModelAdmin):
    """docstring for  """
    list_display = ('id', 'created_at','remote_ip', 'user', 'action',
        'object_repr', 'content_type', 'object_id' , 'changes', 'object_extra_info', 'action_info')
    list_filter = ('action', 'created_at',)
    search_fields = ["user__username", "user__email", 'remote_ip']
    raw_id_fields = ["user"]

    date_hierarchy = 'created_at'
