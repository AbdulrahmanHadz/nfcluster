import logging
from uuid import UUID

from newsapi.newsapi_exception import NewsAPIException
from django.conf import settings

from newsapi import NewsApiClient

from clustering.analysis.clustering import schedule_clustering
from clustering.models.models import ClusteringJob, SearchJob, SearchParams
from news_clustering.misc import create_task
from search.api.fetch_article_data import get_article_data
from search.response.article import ArticleLocalModel as ArticleApi
from search.response.query_params import SearchParamsLocalModel

newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)


def search_for_articles(search_params: SearchParamsLocalModel, **kwargs):
    try:
        # googlenews = GNews(
        #     language=search_params.language, country=search_params.region, exclude_websites=search_params.exclude_domains, max_results=search_params.max_results
        # )
        # googlenews = GoogleNews(lang=search_params.language, start=search_params.from_param, end=search_params.to)
        # googlenews.search(search_params.q)
        # while len(googlenews.results()) < search_params.max_results:
        #     for page in range(2, 100):
        #         googlenews.get_page(page)
        #         time.sleep(2)

        # if search_params.num_pages is not None and search_params.num_pages > 1:
        #     for page in range(2, search_params.num_pages + 1):
        #         googlenews.get_page(page)

        # results = googlenews.results()

        results = newsapi.get_everything(
            q=search_params.q,
            qintitle=search_params.qintitle,
            sources=search_params.sources,
            domains=search_params.domains,
            exclude_domains=search_params.exclude_domains,
            from_param=search_params.from_param,
            to=search_params.to,
            language=search_params.language,
            sort_by=search_params.sort_by,
            page=search_params.page,
            page_size=search_params.page_size,
        )
        return {"status": "ok", "code": 200, "articles": results["articles"]}

    except NewsAPIException as e:
        try:
            code = int(e.get_code())
        except ValueError:
            code = 500

        return {
            "status": e.get_status() or "error",
            "code": code,
            "message": e.get_message() or "Error retrieving articles",
            "articles": [],
        }


def fetch_search_obj(
    cluster_id: UUID = None,
    search_id: UUID = None,
):
    try:
        return SearchJob.objects.get(pk=search_id)
    except SearchJob.DoesNotExist:
        try:
            clustering_job = ClusteringJob.objects.get(pk=cluster_id)
            return clustering_job.search
        except ClusteringJob.DoesNotExist:
            pass
    return None


def search(
    search_params: dict,
    cluster_id: UUID = None,
    search_id: UUID = None,
    params_class=SearchParamsLocalModel,
    run_type: str = "cluster",
    **kwargs
):
    search_params = params_class(**search_params)
    if search_params.q is None:
        return {
            "status": "error",
            "code": 400,
            "message": "'q' cannot be empty.",
        }

    search_job = fetch_search_obj(
        cluster_id,
        search_id,
    )

    if search_job is not None:
        if search_job.params is not None:
            if search_job.params.q != search_params.q:
                return {
                    "status": "error",
                    "code": 400,
                    "message": "Cannot add more articles to this api "
                    "if the api parameters are not the same.",
                }

    try:
        job_id = start_new_search_task(
            search_params=search_params,
            cluster_id=cluster_id,
            search_id=search_id,
            run_type=run_type,
        )
    except Exception as e:
        logging.exception("Error fetching articles.")
        return {"status": "error", "code": 500, "message": str(e)}

    return {"status": "ok", "code": 200, "id": job_id}


def search_params_as_model(search_params: SearchParamsLocalModel):
    search_obj = SearchParams.objects.create(
        **{
            k: v
            for k, v in vars(search_params).items()
            if k in [f.name for f in SearchParams._meta.get_fields()]
            and k != "num_clusters"
        }
    )
    search_obj.save()
    return search_obj


def create_search_obj(search_params: SearchParamsLocalModel):
    search_obj = search_params_as_model(search_params)

    search_job = SearchJob.objects.create(params=search_obj)
    search_job.save()
    return search_job


def create_cluster_obj(search_obj: SearchJob):
    model = ClusteringJob.objects.create(search=search_obj)
    model.save()
    return model


def start_new_search_task(
    search_params: SearchParamsLocalModel,
    cluster_id: UUID = None,
    search_id: UUID = None,
    run_type="cluster",
    **kwargs
):
    cluster_obj = None

    if search_id is not None:
        try:
            search_job = SearchJob.objects.get(pk=search_id)
        except SearchJob.DoesNotExist:
            search_job = create_search_obj(search_params)

        task_id = search_job.id
        searchid = task_id
    else:
        try:
            model = ClusteringJob.objects.get(pk=cluster_id)
        except ClusteringJob.DoesNotExist:
            search_obj = create_search_obj(search_params)
            model = create_cluster_obj(search_obj)
            if run_type == "cluster":
                cluster_obj = model

        task_id = model.id
        searchid = model.search.id

    create_task(
        searchid,
        func=start_search,
        search_params=search_params,
        cluster_obj=cluster_obj,
    )
    return task_id


def start_search(
    task_id: str,
    search_params: SearchParamsLocalModel,
    cluster_obj=None,
    *args,
    **kwargs
):
    articles = search_for_articles(search_params)
    if articles["status"] != "ok":
        return articles

    results = [
        ArticleApi(
            headline=article["title"],
            author=article["author"],
            published_at=article["publishedAt"],
            url=article["url"],
        )
        for article in articles["articles"]
    ]

    # results = [
    #     ArticleApi(
    #         headline=article["title"],
    #         # author=article["author"],
    #         published_at=article["datetime"] or "1970-01-01T00:00:00",
    #         url=article["link"],
    #     )
    #     for article in articles["articles"]
    # ]

    get_article_data(task_id=task_id, articles=results)

    if cluster_obj is not None:
        schedule_clustering(cluster_obj, search_params.num_clusters)


def refresh_search_data(search_obj):
    articles = [ArticleApi(url=url.url) for url in search_obj.urls.all()]
    create_task(search_obj.id, func=get_article_data, articles=articles)
    return {"code": 200, "status": "ok", "id": search_obj.id}
