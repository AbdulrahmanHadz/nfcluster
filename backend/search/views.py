from uuid import UUID

from django.http import Http404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from clustering.models.models import SearchJob
from clustering.models.serialisers import (
    SearchJobSerialiser,
    PartialSearchJobSerialiser,
    SearchJobWithAnalysisSerialiser,
)
from search.api.search_articles import refresh_search_data, search


def get_searching_job_object(pk) -> SearchJob:
    try:
        return SearchJob.objects.get(pk=pk)
    except SearchJob.DoesNotExist:
        raise Http404


class SearchJobList(generics.ListCreateAPIView):
    serializer_class = PartialSearchJobSerialiser
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return SearchJob.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = search(request.data, run_type="search")
        return Response(response, status=response.pop("code", 500))


class SearchJobView(APIView):
    def get(self, request: Request, search_id: UUID):
        searching_obj = get_searching_job_object(search_id)
        serializer = SearchJobSerialiser(searching_obj)
        return Response(serializer.data, status=200)

    def post(self, request: Request, search_id: UUID):
        response = search(request.data, search_id=search_id, run_type="search")
        return Response(response, status=response.pop("code", 500))


@api_view(["GET", "POST"])
def fetch_article_data(request, search_id: UUID):
    searching_obj = get_searching_job_object(search_id)
    data = refresh_search_data(searching_obj)
    return Response(data, status=data.pop("code", 500))


@api_view(["GET"])
def view_articles_analysis(request, search_id: UUID):
    searching_obj = get_searching_job_object(search_id)
    serialiser = SearchJobWithAnalysisSerialiser(searching_obj)
    return Response(serialiser.data, status=200)
