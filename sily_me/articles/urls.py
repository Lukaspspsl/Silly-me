from django.contrib import admin
from django.urls import path
from .views import (
    ArticleCreateView,
    SingleArticleView,
    ReminderCreateView,
    SingleReminderView,
    SourceCreateView,
    SingleSourceView
)

urlpatterns = [
    path("articles/", ArticleCreateView.as_view(), name="save-article"),
    path("articles/<int:pk>/", SingleArticleView.as_view(), name="articles"),
    path("reminders/", ReminderCreateView.as_view(), name="save-reminder"),
    path("reminders/<int:pk>/", SingleReminderView.as_view(), name="reminders"),
    path("sources/", SourceCreateView.as_view(), name="save-source"),
    path("sources/<int:pk>/", SingleSourceView.as_view(), name="sources")
    ]