from django.urls import path
from .views import logged_in_user_email_view, public_api_view

urlpatterns = [
    path('user-email/', logged_in_user_email_view, name='user-email'),
    path('public-api/', public_api_view, name='public-api'),
]
