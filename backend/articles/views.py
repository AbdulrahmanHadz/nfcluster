from django.http import Http404
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from clustering.analysis.clustering import run_analysis_article
from clustering.models.models import Article
from clustering.models.serialisers import (
    ArticleWithAnalysisSerialiser, ArticleAnalysisSerialiser, PartialArticleSerialiser
)


def get_article_object(pk):
    try:
        return Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404


@api_view(["GET"])
def get_article(request, article_id):
    article = get_article_object(article_id)
    serializer = ArticleWithAnalysisSerialiser(article)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def get_all_articles(request):
    ids = request.query_params.get("ids", None)
    if ids is not None:
        ids = ids.split(",")


    return Response(ids)

    objects = Article.objects.all()
    serialiser = PartialArticleSerialiser(objects, many=True)
    return Response(serialiser.data, status=200)


@api_view(["GET", "POST"])
def run_article_analysis(request, article_id):
    article = get_article_object(article_id)
    run_analysis_article(article)
    serialiser = ArticleAnalysisSerialiser(article)
    return Response(serialiser.data, status=200)


class ArticleList(generics.ListCreateAPIView):
    serializer_class = PartialArticleSerialiser
    filter_backends = [OrderingFilter]
    ordering_fields = ["published_at", "language", "url"]
    ordering = ["-published_at"]

    def get_queryset(self):
        return Article.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
