import json
from json import JSONEncoder
from time import time

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer

from clustering.models.models import ClusteringAnalysis, ClusteringMetrics
from news_clustering.misc import create_task, json_dumps
from search.api.analyse_articles import analyse_article
from search.response.query_params import ClusterParamsLocalModel, DEFAULT_NUM_CLUSTERS


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def tokenise_articles(clustering_obj):
    create_task(
        f"clustering_obj_analysis_{clustering_obj.id}",
        func=run_analysis_clustering_job,
        clustering_obj=clustering_obj,
    )
    return clustering_obj


def run_analysis_clustering_job(clustering_obj, *args, **kwargs):
    articles = clustering_obj.search.completed.all()

    for article in articles:
        run_analysis_article(article)


def run_analysis_article(article):
    create_task(
        f"article_analysis_{article.id}",
        func=analyse_article,
        article=article,
        force_analyse=True,
    )


def process_clustering(
    clustering_obj, articles_text, articles_id, num_clusters, *args, **kwargs
):
    vectoriser = TfidfVectorizer(stop_words="english", min_df=0.0001)
    t0 = time()
    X_tfidf = vectoriser.fit_transform(articles_text)
    vectorisation_duration = time() - t0
    n_samples = X_tfidf.shape[0]
    n_features = X_tfidf.shape[1]

    if n_samples <= (DEFAULT_NUM_CLUSTERS * 2):
        n_clusters = n_samples
    else:
        n_clusters = clustering_obj.search.params.num_clusters or num_clusters

    print(f"vectorisation done in {vectorisation_duration:.3f} s")
    print(f"n_samples: {n_samples}, n_features: {n_features}")

    lsa = Pipeline(
        steps=[
            ("svd", TruncatedSVD(n_components=100)),
            ("normaliser", Normalizer(copy=False)),
        ]
    )
    t0 = time()
    X_lsa = lsa.fit_transform(X_tfidf)
    explained_variance = lsa[0].explained_variance_ratio_.sum()
    lsa_duration = time() - t0

    print(f"LSA done in {lsa_duration:.3f} s")

    t0 = time()
    kmeans = KMeans(n_clusters=n_clusters)

    k_fit = kmeans.fit(X_lsa)
    k_predict = kmeans.predict(X_lsa)
    cluster_duration = time() - t0
    clusters = kmeans.labels_.tolist()
    pred_labels = kmeans.labels_

    dbi_score = metrics.davies_bouldin_score(X_lsa, pred_labels)
    silhouette_score = metrics.silhouette_score(X_lsa, pred_labels, metric="euclidean")
    # ari_score = adjusted_rand_score(np.ndarray.flatten(X_lsa), pred_labels)

    article_frames = {"article": articles_text, "cluster": clusters, "id": articles_id}
    frame = pd.DataFrame(article_frames, index=articles_id)

    frame_data_str = frame.to_json(default_handler=str)
    frame_data = json.loads(frame_data_str)
    clusters_data = frame_data["cluster"]
    article_clusters = {}
    for key, value in clusters_data.items():
        if value not in article_clusters:
            article_clusters[value] = [key]
        else:
            article_clusters[value].append(key)

    unique_labels = np.unique(k_predict)

    # for i in unique_labels:
    #     plt.scatter(X_lsa[k_predict == i, 0], X_lsa[k_predict == i, 1], label=i)
    # plt.legend()
    # plt.show()

    metrics_obj = ClusteringMetrics.objects.create(
        n_samples=json_dumps(n_samples),
        n_features=json_dumps(n_features),
        vectorisation_duration=vectorisation_duration,
        lsa_duration=lsa_duration,
        explained_variance=json_dumps(explained_variance),
        dbi_score=json_dumps(dbi_score),
        silhouette_score=json_dumps(silhouette_score),
        cluster_duration=json_dumps(cluster_duration),
        unique_labels=json_dumps(unique_labels.tolist()),
        k_predict=json.dumps(k_predict, cls=NumpyArrayEncoder),
        X_lsa=json.dumps(X_lsa, cls=NumpyArrayEncoder),
    )
    metrics_obj.save()

    analysis_obj = ClusteringAnalysis.objects.create(
        clusters=json_dumps(article_clusters), metrics=metrics_obj
    )
    analysis_obj.save()
    clustering_obj.analysis = analysis_obj
    clustering_obj.save()


def run_clustering(clustering_obj, num_clusters):
    # if not clustering_obj.search.status:
    #     return {
    #         "status": "error",
    #         "code": 500,
    #         "message": f"Search has not yet finished for `{clustering_obj.search.id}`.",
    #     }

    schedule_clustering(clustering_obj, num_clusters)

    return {
        "status": "ok",
        "code": 200,
        "id": str(clustering_obj.id),
    }


def schedule_clustering(clustering_obj, num_clusters):
    articles = clustering_obj.search.completed.all()
    articles_text = []
    articles_id = []

    for article in articles:
        if article.article is not None and len(article.article) > 0:
            articles_text.append(article.article)
            articles_id.append(article.id)

    create_task(
        f"cluster_analysis_{clustering_obj.id}",
        func=process_clustering,
        clustering_obj=clustering_obj,
        articles_text=articles_text,
        articles_id=articles_id,
        num_clusters=num_clusters,
    )
