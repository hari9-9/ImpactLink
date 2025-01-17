from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# API accessible only to logged-in users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logged_in_user_email_view(request):
    print(request.user.email)
    print(request.user.id)
    
    return Response({"email": request.user.email})

# API accessible to everyone
@api_view(['GET'])
@permission_classes([AllowAny])
def public_api_view(request):
    return Response({"message": "This API is accessible without login."})

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import hashlib
import base64
from .models import Product, ShortenedURL

@csrf_exempt  # Disable CSRF for simplicity; consider proper CSRF handling in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shorten_url(request):
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
