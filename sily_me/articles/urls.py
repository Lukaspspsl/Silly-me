from django.contrib import admin
from django.urls import path
from .views import (
    ArticleCreateView,
    SingleArticleView,
    SourceCreateView,
    SingleSourceView
)

urlpatterns = [
    path("articles/", ArticleCreateView.as_view(), name="save-article"),
    path("articles/<int:pk>/", SingleArticleView.as_view(), name="article_detail"),
    path("sources/", SourceCreateView.as_view(), name="save-source"),
    path("sources/<int:pk>/", SingleSourceView.as_view(), name="sources")
    ]