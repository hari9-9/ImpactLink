from django.db import models
from django.conf import settings

class Product(models.Model):
    """
    Model representing a product that can be linked via a shortened URL.

    Attributes:
        name (CharField): The name of the product.
        external_url (URLField): The external URL of the product (must be unique).

    Methods:
        __str__(): Returns the name of the product as its string representation.
    """

    name = models.CharField(max_length=255, help_text="The name of the product.")
    external_url = models.URLField(unique=True, help_text="The unique external link to the product.")

    def __str__(self):
        """
        Returns the string representation of the product.

        Returns:
            str: The product's name.
        """
        return self.name


class ShortenedURL(models.Model):
    """
    Model representing a shortened URL for a product.

    Attributes:
        user (ForeignKey): The user who created the shortened URL.
        product (ForeignKey): The product associated with the shortened URL.
        short_url (CharField): The shortened URL identifier (must be unique).
        click_count (PositiveIntegerField): The total number of times the shortened URL was clicked.

    Methods:
        __str__(): Returns the shortened URL identifier as its string representation.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        help_text="The user who owns this shortened URL."
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        help_text="The product linked to this shortened URL."
    )
    short_url = models.CharField(
        max_length=10, 
        unique=True, 
        help_text="The unique shortened URL identifier."
    )
    click_count = models.PositiveIntegerField(
        default=0, 
        help_text="The number of times this shortened URL has been accessed."
    )

    def __str__(self):
        """
        Returns the string representation of the shortened URL.

        Returns:
            str: The shortened URL identifier.
        """
        return self.short_url
