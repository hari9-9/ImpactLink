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
    cache_key = f"short_url_{short_url}"  # Create unique cache key for URL
    visitor_key = f"visitor_{short_url}_{get_client_ip(request)}"  # Unique visitor key

    # Try to fetch the URL from cache
    url_data = cache.get(cache_key)

    if not url_data:
        # If not cached, query the database and store result in cache
        url = get_object_or_404(ShortenedURL, short_url=short_url)
        url_data = url.product.external_url

        # Store in Redis cache
        cache.set(cache_key, url_data, timeout=CACHE_TTL)

    # Check if this visitor has already visited within the last hour
    if not cache.get(visitor_key):
        # If not found in cache, trigger Celery task and add to cache
        update_click_count.delay(short_url)
        cache.set(visitor_key, 'visited', timeout=CACHE_TTL)

    # Redirect the user to the original URL
    return redirect(url_data)



def get_client_ip(request):
    """ Get the real client IP address, considering proxies """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()# First IP in list is the original client
    else:
        ip = request.META.get('REMOTE_ADDR', '')# Fallback to REMOTE_ADDR if no proxy
    return ip
