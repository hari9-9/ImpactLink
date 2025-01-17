from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .models import ShortenedURL

def redirect_view(request, short_url):
    """
    Redirects to the original product URL for a given short URL.
    """
    # Look up the ShortenedURL object
    shortened_url = get_object_or_404(ShortenedURL, short_url=short_url)

    # Increment the click count
    shortened_url.click_count += 1
    shortened_url.save()

    # Redirect to the original product URL
    return HttpResponseRedirect(shortened_url.product.external_url)
