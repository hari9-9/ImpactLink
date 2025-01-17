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
