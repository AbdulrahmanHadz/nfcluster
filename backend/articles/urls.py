from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.ArticleList.as_view(), name="list_all_articles"),
    path("all/", views.get_all_articles, name="get_all_article_analysis"),
    path(
        "<uuid:article_id>/",
        include(
            [
                path("", views.get_article, name="get_article"),
                path(
                    "analyse/", views.run_article_analysis, name="run_article_analysis"
                ),
            ]
        ),
    ),
]
