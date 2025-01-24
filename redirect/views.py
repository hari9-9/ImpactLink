from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import ShortenedURL
from .tasks import update_click_count
from django.conf import settings
from django.core.cache import cache

# Default cache time-to-live (TTL) of 1 hour if not specified in settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 60)

def redirect_view(request, short_url):
    """
    Handles redirection of shortened URLs.

    This function checks if the short URL exists in the cache; if not, it queries the database.
    It tracks the user's visit using their IP and prevents multiple click counts within 1 hour.

    Args:
        request (HttpRequest): The incoming HTTP request.
        short_url (str): The unique shortened URL identifier.

    Returns:
        HttpResponseRedirect: Redirects the user to the original long URL.

    Caching:
        - Stores the original URL in cache for quick access.
        - Tracks visitor IPs to prevent repeated click counting within a time window.

    Example:
        When a user visits `http://domain.com/abc123`, they will be redirected 
        to the corresponding original product URL.
    """

    cache_key = f"short_url_{short_url}"  # Unique cache key for storing the URL
    visitor_key = f"visitor_{short_url}_{get_client_ip(request)}"  # Unique key per visitor

    # Try to fetch the original URL from cache
    url_data = cache.get(cache_key)

    if not url_data:
        # If URL is not found in cache, retrieve from the database and store it in cache
        url = get_object_or_404(ShortenedURL, short_url=short_url)
        url_data = url.product.external_url

        # Store the URL in cache to improve performance
        cache.set(cache_key, url_data, timeout=CACHE_TTL)

    # Check if the visitor has already accessed the link within the cache timeout
    if not cache.get(visitor_key):
        # If visitor is not found in cache, increment click count and cache the visit
        update_click_count.delay(short_url)  # Asynchronously update click count
        cache.set(visitor_key, 'visited', timeout=CACHE_TTL)
    
    # Redirect the user to the original URL
    return redirect(url_data)


def get_client_ip(request):
    """
    Retrieves the real client IP address from the request, considering proxy servers.

    This function checks if the request is coming through a proxy by examining the 
    `HTTP_X_FORWARDED_FOR` header, which contains the client's original IP.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        str: The client's IP address.

    Example:
        If behind a proxy, `HTTP_X_FORWARDED_FOR` may contain a list of IPs,
        the function extracts the first one (real client IP).
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()  # Extract the first IP in case of multiple proxies
    else:
        ip = request.META.get('REMOTE_ADDR', '')  # Fallback to REMOTE_ADDR if no proxy is detected
    return ip
