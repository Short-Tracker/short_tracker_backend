from django.contrib import admin
from .models import Message, Reply, MessageStatus

admin.site.register(Message)
admin.site.register(Reply)
admin.site.register(MessageStatus)