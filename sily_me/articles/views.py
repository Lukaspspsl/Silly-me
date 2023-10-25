
from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from django.views import View
from .serializers import ArticleSerializer, ReminderSerializer, SourceSerializer
from .models import Article as ArticleModel, Reminder, Source
from rest_framework.response import Response
from rest_framework import status
from newspaper import Article as NSarticle

class HomepageView(View):
    template_name = "homepage.html"

    def get(self, request):
        return render(request, self.template_name)


class ArticleCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer

    def fetch_and_save(self, url):
        article = NSarticle(url)
        article.download()
        article.parse()

        title = article.title
        body = article.text
        author = ", ".join(article.authors) if article.authors else None
        source_url = article.source_url
        source, created = Source.objects.get_or_create(name=source_url, url=source_url)

        saved_article = ArticleModel.objects.create(
            title=title,
            body=body,
            author=author,
            source=source,
            url=source_url
        )
        return saved_article

    def create(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"detail": "URL not provided."}, status=status.HTTP_400_BAD_REQUEST)
        article = self.fetch_and_save(url)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return ArticleModel.objects.all()


class SingleArticleView(generics.ListCreateAPIView):
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
