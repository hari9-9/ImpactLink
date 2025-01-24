from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import hashlib
import base64
from .models import Product, ShortenedURL
from django.conf import settings

# ------------------- Logged-in User API -------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logged_in_user_email_view(request):
    """
    API endpoint to return the email of the authenticated user.

    Permissions:
        - Requires authentication (IsAuthenticated).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response containing the user's email.

    Example response:
        {
            "email": "user@example.com"
        }
    """
    print(request.user.email)
    print(request.user.id)
    
    return Response({"email": request.user.email})

# ------------------- Public API -------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def public_api_view(request):
    """
    Public API endpoint accessible to everyone.

    Permissions:
        - No authentication required (AllowAny).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response with a welcome message.

    Example response:
        {
            "message": "This API is accessible without login."
        }
    """
    return Response({"message": "This API is accessible without login."})

# ------------------- URL Shortening API -------------------

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shorten_url(request):
    """
    API endpoint to create a shortened URL for a given product URL.

    Permissions:
        - Requires authentication (IsAuthenticated).

    Args:
        request (HttpRequest): The HTTP request containing JSON with:
            - product_url (str): The product's original URL (required).
            - product_name (str): The name of the product (required).

    Returns:
        JsonResponse: JSON response containing the shortened URL.

    Raises:
        JsonResponse: If `product_url` or `product_name` is missing, returns a 400 error.

    Example request:
        {
            "product_url": "https://example.com/product1",
            "product_name": "Product 1"
        }

    Example response:
        {
            "short_url": "http://127.0.0.1:8000/redirect/abc123"
        }
    """
    # Parse the incoming JSON data
    data = request.data
    product_url = data.get("product_url")
    product_name = data.get("product_name")  # Accept product name

    if not product_url:
        return JsonResponse({"error": "Product URL is required."}, status=400)

    if not product_name:
        return JsonResponse({"error": "Product name is required."}, status=400)

    # Use transactions to ensure atomicity
    with transaction.atomic():
        # Check if the product already exists
        product, created = Product.objects.get_or_create(
            external_url=product_url,
            defaults={"name": product_name}  # Store the provided product name
        )

        # Generate a unique shortened URL
        unique_string = f"{request.user.id}-{product.id}"
        hash_object = hashlib.md5(unique_string.encode())
        short_url = base64.urlsafe_b64encode(hash_object.digest()[:6]).decode('utf-8')

        # Check if the shortened URL already exists for the user and product
        shortened_url, created = ShortenedURL.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"short_url": short_url}
        )

    # Build the full shortened URL (replace 'your-domain.com' with your actual domain)
    full_short_url = f"http://127.0.0.1:8000/redirect/{shortened_url.short_url}"

    return JsonResponse({"short_url": full_short_url}, status=201)

# ------------------- Product Statistics Helper Function -------------------

def get_product_statistics(user):
    """
    Retrieves product statistics for a given user.

    Args:
        user (CustomUser): The authenticated user whose product stats are being retrieved.

    Returns:
        list: A list of dictionaries containing product statistics.

    Example response:
        [
            {
                'product_name': 'Product 1',
                'original_url': 'https://example.com/product1',
                'shortened_url': 'http://127.0.0.1:8000/redirect/abc123',
                'total_clicks': 10
            }
        ]
    """
    shortened_urls = ShortenedURL.objects.filter(user=user)
    stats = []
    for entry in shortened_urls:
        stats.append({
            'product_name': entry.product.name,
            'original_url': entry.product.external_url,
            'shortened_url': f"{settings.SITE_URL}/redirect/{entry.short_url}",
            'total_clicks': entry.click_count
        })
    return stats

# ------------------- Product Statistics API -------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_product_statistics(request):
    """
    API endpoint to retrieve product statistics for the logged-in user.

    Permissions:
        - Requires authentication (IsAuthenticated).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response containing product statistics.

    Example response:
        {
            "products": [
                {
                    "product_name": "Product 1",
                    "original_url": "https://example.com/product1",
                    "shortened_url": "http://127.0.0.1:8000/redirect/abc123",
                    "total_clicks": 10
                }
            ]
        }
    """
    user = request.user
    product_stats = get_product_statistics(user)
    return Response({'products': product_stats})
