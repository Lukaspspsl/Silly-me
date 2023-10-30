
from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from django.views import View
from .serializers import ArticleSerializer, ReminderSerializer, SourceSerializer
from .models import Article as ArticleModel, Reminder, Source, Article
from rest_framework.response import Response
from rest_framework import status
from newspaper import Article as NewsArticle
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleForm


def homepage_view(request):
    form = ArticleForm()
    articles = []
    if request.user.is_authenticated:
        articles = ArticleModel.objects.filter(user=request.user)
    return render(request, "homepage.html", {"form": form, "articles": articles})



class ArticleCreateView(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ArticleSerializer

    def fetch(self, url):
        article = NewsArticle(url)
        article.download()
        article.parse()

        title = article.title
        body = article.text
        author = ", ".join(article.authors) if article.authors else None
        source_url = article.source_url
        source, created = Source.objects.get_or_create(name=source_url, url=source_url)

        article_data = {
            "title": title,
            "body": body,
            "author": author,
            "source": source,
            "url": source_url
        }

        return article_data

    def create(self, request):
        """Create an article from a URL. Also serves as a view for the list of all saved articles."""
        url = request.data.get("url")
        if not url:
            return Response({"detail": "URL not provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_authenticated:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_403_FORBIDDEN)

        article = self.fetch(url)

        article_instance = ArticleModel(user=request.user, **article)
        article_instance.save()

        serializer = ArticleSerializer(article_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return ArticleModel.objects.filter(user=self.request.user)



class SingleArticleView(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ArticleSerializer

    def view_single_article(self, id):
        try:
            article = ArticleModel.objects.get(pk=id)
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArticleModel.DoesNotExist:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete_article(self, id):
        try:
            article = ArticleModel.objects.get(pk=id)
            article.delete()
            return Response({"detail": "Article deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ArticleModel.DoesNotExist:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        return self.view_single_article(id)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        return self.delete_article(id)



class ReminderCreateView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer



class SingleReminderView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer



class SourceCreateView(generics.ListCreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer



class SingleSourceView(generics.ListCreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
