from django.db import models
from django.contrib.auth.models import User
from articles.models import Article as ArticleModel

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    is_reminded = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.article} on {self.reminder_time}"