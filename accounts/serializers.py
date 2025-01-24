from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    Handles serialization and deserialization of user objects, 
    including password write protection during output.
    """

    class Meta:
        """
        Meta options for UserSerializer.

        Attributes:
            model (CustomUser): The model associated with this serializer.
            fields (tuple): Fields to be serialized ('email', 'name', 'password').
            extra_kwargs (dict): Custom options for specific fields (password is write-only).
        """
        model = CustomUser
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates and returns a new user instance with encrypted password.

        Args:
            validated_data (dict): The validated data containing user details.

        Returns:
            CustomUser: The newly created user instance.
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Handles validation of user credentials during login requests.
    """

    email = serializers.EmailField(help_text="The user's email address.")
    password = serializers.CharField(write_only=True, help_text="The user's password.")

    def validate(self, data):
        """
        Validates user credentials.

        Authenticates the provided email and password. Raises validation 
        error if authentication fails.

        Args:
            data (dict): Dictionary containing 'email' and 'password' fields.

        Raises:
            serializers.ValidationError: If authentication fails.

        Returns:
            CustomUser: The authenticated user instance if credentials are valid.
        """
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user
