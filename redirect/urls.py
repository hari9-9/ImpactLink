from django.urls import path
from .views import redirect_view

urlpatterns = [
    path('<str:short_url>/', redirect_view, name='redirect'),
]
