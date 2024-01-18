from django.contrib import admin

from .models import Message, MessageStatus, Reply

admin.site.register(Message)
admin.site.register(Reply)
admin.site.register(MessageStatus)