from django.urls import include, path
from rest_framework import routers

from . import views

urlpatterns = [
    path("", views.ClusterJobList.as_view(), name="list_create_clustering_jobs"),
    path(
        "<uuid:cluster_id>/",
        include(
            [
                path(
                    "",
                    views.ClusterJobView.as_view(),
                    name="view_create_clustering_job",
                ),
                path(
                    "analyse/",
                    views.cluster_articles,
                    name="run_analysis_clustering_job",
                ),
            ]
        ),
    ),
]
