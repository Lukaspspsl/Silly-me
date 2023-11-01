from django.utils import timezone
from django.http import HttpResponse
from django_q.tasks import schedule
from articles.models import Article as ArticleModel
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail


def set_email(article_id):
    article = get_object_or_404(ArticleModel, pk=article_id)
    subject = f'Reminder for {article.title}'
    message = f'Hello,\n\nHere is the content of the article you wanted to be reminded of:\n\n{article.content}'
    from_email = 'silyme9@gmail.com'
    recipient_list = [article.user.email]
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Error sending email: {e}")


def send_reminder_view(request, article_id):
    article = get_object_or_404(ArticleModel, pk=article_id)

    if request.user == article.user:
        schedule(
            "set_email",
            article_id,
            schedule_type='O',
            next_run=timezone.now() + timezone.timedelta(minutes=1)
        )
        return HttpResponse("Remainder set.")
    else:
        messages.error(request, "You are not authorized to send this email.")

    return redirect("homepage")

