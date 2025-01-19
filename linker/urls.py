from django.urls import path
from .views import logged_in_user_email_view, public_api_view , shorten_url , user_product_statistics

urlpatterns = [
    path('user-email/', logged_in_user_email_view, name='user-email'),
    path('public-api/', public_api_view, name='public-api'),
    path('shorten/', shorten_url, name='shorten_url'),
    path('product-stats/', user_product_statistics, name='product-stats'),
]
