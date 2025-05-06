from celery import shared_task

from .models import Comment


@shared_task
def delete_rejected_comments():
    Comment.objects.filter(status=Comment.STATUS_REJECTED).delete()
