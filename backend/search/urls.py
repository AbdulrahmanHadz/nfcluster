from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path("", views.SearchJobList.as_view(), name="all_post_search_jobs"),
    path(
        "<uuid:search_id>/",
        include(
            [
                path(
                    "",
                    views.SearchJobView.as_view(),
                    name="search_post_search_job",
                ),
                path(
                    "analyse/",
                    views.fetch_article_data,
                    name="refresh_search_data",
                ),
                path(
                    "analysis/",
                    views.view_articles_analysis,
                    name="view_articles_analysis",
                ),
            ]
        ),
    ),
]
