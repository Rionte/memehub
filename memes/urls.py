from django.urls import path
from . import views

urlpatterns = [
    path("", views.memes),
    path("contact", views.contact)
]