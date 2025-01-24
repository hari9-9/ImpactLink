from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class UserSignupView(APIView):
    """
    Handles user registration via the API.

    Allows any user to create an account by providing required details.

    Attributes:
        permission_classes (list): Specifies that the endpoint is accessible without authentication.

    Methods:
        post(request): Handles the creation of a new user account.
    """
    
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to register a new user.

        Args:
            request (Request): The HTTP request containing user registration data.

        Returns:
            Response: HTTP 201 if successful, HTTP 400 if validation fails.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    """
    Handles user authentication via the API.

    Allows any user to log in using email and password credentials.

    Attributes:
        permission_classes (list): Specifies that the endpoint is accessible without authentication.

    Methods:
        post(request): Authenticates the user and provides JWT tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to authenticate a user and generate JWT tokens.

        Args:
            request (Request): The HTTP request containing login credentials.

        Returns:
            Response: JSON containing access and refresh tokens if authentication is successful.
                      Returns HTTP 400 if credentials are invalid.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    """
    Handles user logout via the API.

    Requires the user to provide a valid refresh token, which will be blacklisted to prevent further use.

    Methods:
        post(request): Blacklists the refresh token to log out the user.
    """

    def post(self, request):
        """
        Handles POST requests to log out a user by blacklisting their refresh token.

        Args:
            request (Request): The HTTP request containing the refresh token.

        Returns:
            Response: HTTP 205 if logout is successful.
                      Returns HTTP 400 in case of an invalid or missing token.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
