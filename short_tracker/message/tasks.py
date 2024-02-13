from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Message


@shared_task
def delete_solved_queries():
    print("Delete")
    threshold_time = timezone.now() - timedelta(
        hours=settings.SOLVED_MESSAGE_DELETE
    )
    messages_to_delete = Message.objects.filter(
        message_status='solved',
        message_date__lte=threshold_time
    )
    messages_to_delete.delete()
    print("Delete", messages_to_delete)
