import uuid

from django.db import models


class SearchParams(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    q = models.TextField(null=True)
    qintitle = models.TextField(null=True)
    sources = models.TextField(null=True)
    domains = models.TextField(null=True)
    exclude_domains = models.TextField(null=True)
    from_param = models.TextField(null=True)
    to = models.TextField(null=True)
    language = models.CharField(max_length=255, null=True)
    sort_by = models.TextField(null=True)

    num_clusters = models.IntegerField(null=True)


class ArticleURL(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    url = models.URLField(unique=True)

    def __str__(self):
        return str(self.url)


class ArticleAnalysis(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tokenised = models.TextField(null=True)
    sentiment = models.TextField(null=True)
    sentiment_analysis = models.TextField(null=True)
    keywords = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    headline = models.TextField(null=True)
    description = models.TextField(null=True)
    article = models.TextField(null=True)
    author = models.TextField(null=True)
    keyword = models.TextField(null=True)
    url = models.URLField(unique=True)
    published_at = models.DateTimeField(null=True)
    language = models.CharField(max_length=255, null=True)
    filename = models.URLField(null=True)
    publication = models.CharField(max_length=255, null=True)
    source_domain = models.CharField(max_length=255, null=True)

    analysis = models.OneToOneField(
        ArticleAnalysis, on_delete=models.CASCADE, null=True
    )


class ClusteringMetrics(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    n_samples = models.TextField(null=True)
    n_features = models.TextField(null=True)

    vectorisation_duration = models.TextField(null=True)
    lsa_duration = models.TextField(null=True)
    cluster_duration = models.TextField(null=True)

    explained_variance = models.TextField(null=True)
    dbi_score = models.TextField(null=True)
    silhouette_score = models.TextField(null=True)

    unique_labels = models.TextField(null=True)
    k_predict = models.TextField(null=True)
    X_lsa = models.TextField(null=True)


class ClusteringAnalysis(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    clusters = models.TextField(null=True)
    metrics = models.OneToOneField(
        ClusteringMetrics, on_delete=models.CASCADE, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SearchJob(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    params = models.OneToOneField(SearchParams, on_delete=models.CASCADE, null=True)
    urls = models.ManyToManyField(ArticleURL)
    completed = models.ManyToManyField(
        Article, related_name="%(app_label)s_%(class)s_completed_search"
    )
    failed = models.ManyToManyField(
        ArticleURL, related_name="%(app_label)s_%(class)s_failed_search"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.completed.count()

    @property
    def status(self):
        return (
            False
            if self.total == 0
            else (self.failed.count() + self.completed.count()) == self.urls.count()
        )


class ClusteringJob(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    analysis = models.OneToOneField(
        ClusteringAnalysis, on_delete=models.CASCADE, null=True
    )
    search = models.OneToOneField(SearchJob, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.search.completed.count()

    @property
    def status(self):
        return bool(self.analysis)

    @property
    def params(self):
        return self.search.params

    @property
    def search_status(self):
        return self.search.status

    @property
    def progress(self):
        if not self.search.status and not self.status:
            return f"Search in progress: {self.search.completed.count() + self.search.failed.count()}/{self.search.urls.count()} completed."
        if self.search.status and not self.status:
            return f"Search completed, clustering in progress."
        if self.search.status and self.status:
            return f"Search and clustering completed."
        if not self.search.status and self.status:
            return f"Clustering completed, search in progress. Clustered (latest run) {self.search.completed.count()}/{self.search.urls.count()} articles."
