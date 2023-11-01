from django.urls import path
from . import views

urlpatterns = [
path("send/<int:article_id>/", views.send_reminder_view, name="send_reminder"),
]