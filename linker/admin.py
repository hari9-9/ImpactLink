from django.contrib import admin

# Register your models here.
from .models import Product, ShortenedURL

# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'external_url')  # Columns displayed in the admin list view
    search_fields = ('name', 'external_url')       # Add search functionality
    list_filter = ('name',)                        # Add filters

# Register ShortenedURL model
@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'short_url', 'click_count')  # Columns displayed in the admin list view
    search_fields = ('short_url',)                                       # Add search functionality
    list_filter = ('user', 'product')                                    # Add filters
