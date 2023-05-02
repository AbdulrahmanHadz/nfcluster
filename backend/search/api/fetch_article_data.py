from typing import List

from newsfetch.news import newspaper

from clustering.models.models import (
    Article,
    SearchJob,
    ArticleURL,
)
from news_clustering.misc import dedupe_list, json_dumps
from search.api.analyse_articles import analyse_article
from search.response.article import (
    ArticleLocalModel as ArticleApi,
)


def get_article_obj_from_url(url, articles):
    for article in articles:
        if article.url == url:
            return article


def get_article_data(task_id: str, articles: List[ArticleApi], *args, **kwargs):
    articles_urls = dedupe_list([article.url for article in articles])
    articles_exists_data = Article.objects.filter(url__in=articles_urls)

    article_url_objs = make_url_obj(articles_urls)
    search_job = SearchJob.objects.get(pk=task_id)
    search_job.urls.add(*article_url_objs)
    search_job.completed.add(*articles_exists_data)
    search_job.save()

    for article in articles:
        if article is None:
            continue

        try:
            on_db = Article.objects.get(url=article.url)
        except Article.DoesNotExist:
            news = newspaper(article.url)
            article.headline = news.headline
            article.published_at = news.date_publish
            article.keyword = json_dumps(news.keywords)
            article.description = news.description
            article.article = news.article
            article.author = json_dumps(news.authors)
            article.filename = news.filename
            article.language = news.language
            article.publication = news.publication
            article.source_domain = news.source_domain

            if article.article is not None and bool(article.article):
                on_db = make_article_obj(article)
                search_job.completed.add(on_db)
                analyse_article(task_id=on_db.id, article=on_db)
            else:
                failed_article = make_url_obj([article.url])
                search_job.failed.add(*failed_article)
        else:
            try:
                search_job.completed.get(url=on_db.url)
            except Article.DoesNotExist:
                search_job.completed.add(on_db)

            analyse_article(task_id=on_db.id, article=on_db)

        search_job.save()


def make_article_obj(data: ArticleApi):
    result, created = Article.objects.get_or_create(url=data.url, defaults=vars(data))
    result.save()
    return result


def make_url_obj(data):
    objs = []
    for url in data:
        result, created = ArticleURL.objects.get_or_create(
            url=url, defaults={"url": url}
        )
        result.save()
        objs.append(result)
    return objs
