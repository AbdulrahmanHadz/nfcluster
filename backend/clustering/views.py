import json
from uuid import UUID

from django.http import Http404
from rest_framework import generics

from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from clustering.analysis.clustering import run_clustering
from clustering.models.models import ClusteringJob
from clustering.models.serialisers import (
    ClusteringJobSerialiser,
    PartialClusteringJobSerialiser,
)
from search.api.search_articles import search
from search.response.query_params import ClusterParamsLocalModel, DEFAULT_NUM_CLUSTERS


def get_clustering_job_object(pk):
    try:
        return ClusteringJob.objects.get(pk=pk)
    except ClusteringJob.DoesNotExist:
        raise Http404


@api_view(["POST"])
def cluster_articles(request, cluster_id):
    clustering_obj = get_clustering_job_object(cluster_id)
    num_clusters = request.data.get("num_clusters", DEFAULT_NUM_CLUSTERS)
    response = run_clustering(clustering_obj, num_clusters)
    return Response(response, status=response.pop("code", 500))


class ClusterJobList(generics.ListCreateAPIView):
    serializer_class = PartialClusteringJobSerialiser
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return ClusteringJob.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = search(
            request.data, params_class=ClusterParamsLocalModel, run_type="cluster"
        )
        return Response(response, status=response.pop("code", 500))


class ClusterJobView(APIView):
    def get(self, request: Request, cluster_id: UUID):
        clustering_obj = get_clustering_job_object(cluster_id)
        serializer = ClusteringJobSerialiser(clustering_obj)
        return Response(serializer.data, status=200)

    def post(self, request: Request, cluster_id: UUID):
        response = search(
            request.data,
            cluster_id=cluster_id,
            params_class=ClusterParamsLocalModel,
            run_type="cluster",
        )
        return Response(response, status=response.pop("code", 500))
