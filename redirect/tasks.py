from celery import shared_task
from django.db.models import F
from .models import ShortenedURL
from django.shortcuts import get_object_or_404
@shared_task
def update_click_count(short_code):
    """ Update the click count asynchronously using RabbitMQ. """
    shortened_url = get_object_or_404(ShortenedURL, short_url=short_code)
    shortened_url.click_count += 1
    shortened_url.save()
    return f"Click count updated for {short_code}"
