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
    author = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source, related_name="articles", on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    archived = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="articles")

    def __str__(self):
        return self.title


class Reminder(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"Reminder for {self.article.title} on {self.reminder_time}"
