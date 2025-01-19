from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404 , redirect
from .models import ShortenedURL
from .tasks import update_click_count

def redirect_view(request, short_url):
    # Fetch the shortened URL object
    url = get_object_or_404(ShortenedURL, short_url=short_url)

    # Trigger the Celery task asynchronously
    update_click_count.delay(short_url)

    # Redirect user to the original URL immediately
    return redirect(url.product.external_url)
