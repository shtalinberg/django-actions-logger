# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import LogAction
from .forms import LogActionForm

@admin.register(LogAction)
class LogActionAdmin(admin.ModelAdmin):

    form = LogActionForm
    list_display = (
        'id', 'created_at', 'remote_ip', 'user', 'action',
        'object_repr', 'content_type', 'object_id', 'changes',
        'object_extra_info', 'action_info'
    )
    list_filter = ('action', 'created_at',)
    search_fields = ["user__username", "user__email", 'session_key', 'remote_ip']
    raw_id_fields = ["user"]

    date_hierarchy = 'created_at'
