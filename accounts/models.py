from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.

    Provides helper methods to create standard users and superusers.
    """

    def create_user(self, email, name, password=None):
        """
        Creates and returns a standard user with the given email, name, and password.

        Args:
            email (str): The email address of the user.
            name (str): The full name of the user.
            password (str, optional): The password for the user. Defaults to None.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            CustomUser: The created user instance.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and returns a superuser with the given email, name, and password.

        Args:
            email (str): The email address of the superuser.
            name (str): The full name of the superuser.
            password (str, optional): The password for the superuser. Defaults to None.

        Returns:
            CustomUser: The created superuser instance with elevated permissions.
        """
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends Django's AbstractBaseUser and PermissionsMixin.

    Fields:
        email (EmailField): The unique email address for the user.
        name (CharField): The full name of the user.
        is_active (BooleanField): Indicates whether the user is active. Defaults to True.
        is_staff (BooleanField): Indicates whether the user has staff privileges. Defaults to False.
        is_superuser (BooleanField): Indicates whether the user has superuser privileges. Defaults to False.

    Attributes:
        USERNAME_FIELD (str): The field to be used for authentication ('email').
        REQUIRED_FIELDS (list): The list of required fields besides email ('name').

    Methods:
        __str__(): Returns a string representation of the user (email).
    """

    email = models.EmailField(unique=True, help_text="The unique email address of the user.")
    name = models.CharField(max_length=50, help_text="The full name of the user.")
    is_active = models.BooleanField(default=True, help_text="Designates whether this user should be treated as active.")
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into the admin site.")
    is_superuser = models.BooleanField(default=False, help_text="Designates that this user has all permissions.")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: The email of the user.
        """
        return self.email
