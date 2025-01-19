from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404 , redirect
from .models import ShortenedURL
from .tasks import update_click_count
from django.conf import settings
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 60)  # Default 1 hour

def redirect_view(request, short_url):

    cache_key = f"short_url_{short_url}"  # Create unique cache key

    # Try to fetch the URL from cache
    url_data = cache.get(cache_key)

    if not url_data:
        # If not cached, query the database and store result in cache
        url = get_object_or_404(ShortenedURL, short_url=short_url)
        url_data = url.product.external_url

        # Store in Redis cache
        cache.set(cache_key, url_data, timeout=CACHE_TTL)

    # Trigger the Celery task asynchronously to update click count
    update_click_count.delay(short_url)

    # Redirect the user to the original URL immediately
    return redirect(url_data)