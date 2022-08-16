from django.urls import path
from . import views

urlpatterns = [
    path("", views.ComputersView.as_view(), name="computers"),
    path("<int:id>/", views.ComputerDetailView.as_view(), name="computer_detail"),
    path("software/", views.SoftwareView.as_view(), name="software"),
    path(
        "software/<int:id>/", views.SoftwareDetailView.as_view(), name="software_detail"
    ),
]
