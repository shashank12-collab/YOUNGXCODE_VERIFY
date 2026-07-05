from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "verify/<str:internship_id>/",
        views.verify_certificate,
        name="verify_certificate",
    ),
]