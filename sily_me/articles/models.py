from django.db import models
from django.contrib.auth.models import User


class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(default="No text")
    author = models.CharField(max_length=150, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source, related_name="articles", on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    archived = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="articles")

    def __str__(self):
        return self.title

