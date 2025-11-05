from django.urls import path
from . import views


urlpatterns = [
    path('registro/', views.register_client, name='register_client'),
    path('login/', views.login, name='login'),
]