import json

from rest_framework import serializers

from clustering.models.models import (
    ArticleURL,
    Article,
    ClusteringAnalysis,
    ClusteringMetrics,
    SearchJob,
    ClusteringJob,
    SearchParams,
    ArticleAnalysis,
)
from news_clustering.misc import json_load
from search.response.query_params import DEFAULT_NUM_CLUSTERS


class PrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        value = super(PrimaryKeyRelatedField, self).to_representation(value)
        return {"id": str(value)}


class JSONField(serializers.RelatedField):
    def to_representation(self, value):
        try:
            return json_load(value)
        except json.JSONDecodeError:
            return value


class ArticleURLSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ArticleURL
        fields = ["url"]


class ArticleSerialiser(serializers.ModelSerializer):
    author = JSONField(read_only=True)
    keyword = JSONField(read_only=True)
    analysis = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleAnalysisSerialiser(serializers.ModelSerializer):
    article = PrimaryKeyRelatedField(read_only=True)
    tokenised = JSONField(read_only=True)
    sentiment_analysis = JSONField(read_only=True)
    keywords = JSONField(read_only=True)

    class Meta:
        model = ArticleAnalysis
        fields = "__all__"


class PartialArticleAnalysisSerialiser(serializers.ModelSerializer):
    article = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ArticleAnalysis
        fields = ["article", "id"]


class AnalysisFromArticleSerialiser(serializers.ModelSerializer):
    tokenised = JSONField(read_only=True)
    sentiment_analysis = JSONField(read_only=True)
    keywords = JSONField(read_only=True)
    # sentiment = JSONField(read_only=True)

    class Meta:
        model = ArticleAnalysis
        fields = "__all__"


class ArticleWithAnalysisSerialiser(serializers.ModelSerializer):
    analysis = AnalysisFromArticleSerialiser(read_only=True)
    author = JSONField(read_only=True)
    keyword = JSONField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class SearchParamsSerialiser(serializers.ModelSerializer):
    num_clusters = serializers.IntegerField()

    def get_num_clusters(self, obj):
        if hasattr(obj, "num_clusters"):
            if obj.num_clusters is not None:
                return obj.num_clusters
        return DEFAULT_NUM_CLUSTERS

    class Meta:
        model = SearchParams
        fields = "__all__"


class PartialSearchParamsSerialiser(serializers.ModelSerializer):
    num_clusters = serializers.IntegerField()

    def get_num_clusters(self, obj):
        if hasattr(obj, "num_clusters"):
            if obj.num_clusters is not None:
                return obj.num_clusters
        return DEFAULT_NUM_CLUSTERS

    class Meta:
        model = SearchParams
        fields = [
            "q",
            "sources",
            "domains",
            "exclude_domains",
            "from_param",
            "to",
            "language",
            "sort_by",
            "num_clusters",
        ]


class SearchJobSerialiser(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    params = PartialSearchParamsSerialiser(read_only=True)

    urls = serializers.StringRelatedField(many=True)
    completed = ArticleWithAnalysisSerialiser(many=True)
    failed = serializers.StringRelatedField(many=True)

    clustering = PrimaryKeyRelatedField(read_only=True, source="clusteringjob")

    class Meta:
        model = SearchJob
        fields = "__all__"


class SearchJobWithAnalysisSerialiser(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    completed = ArticleWithAnalysisSerialiser(many=True)

    clustering = PrimaryKeyRelatedField(read_only=True, source="clusteringjob")

    class Meta:
        model = SearchJob
        fields = ["total", "status", "completed", "clustering"]


class ClusteringMetricsSerialiser(serializers.ModelSerializer):
    n_samples = JSONField(read_only=True)
    n_features = JSONField(read_only=True)
    vectorisation_duration = JSONField(read_only=True)
    lsa_duration = JSONField(read_only=True)
    explained_variance = JSONField(read_only=True)
    dbi_score = JSONField(read_only=True)
    silhouette_score = JSONField(read_only=True)
    cluster_duration = JSONField(read_only=True)
    unique_labels = JSONField(read_only=True)

    class Meta:
        model = ClusteringMetrics
        exclude = ["k_predict", "X_lsa"]


class ClusteringAnalysisSerialiser(serializers.ModelSerializer):
    clusters = JSONField(read_only=True)
    metrics = ClusteringMetricsSerialiser(read_only=True)

    class Meta:
        model = ClusteringAnalysis
        fields = "__all__"


class ClusteringJobSerialiser(serializers.ModelSerializer):
    search = PrimaryKeyRelatedField(read_only=True)
    params = PartialSearchParamsSerialiser(read_only=True)
    total = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    analysis = ClusteringAnalysisSerialiser(read_only=True)
    progress = serializers.ReadOnlyField()
    search_status = serializers.ReadOnlyField()

    class Meta:
        model = ClusteringJob
        fields = "__all__"


class PartialSearchJobSerialiser(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    params = PartialSearchParamsSerialiser(read_only=True)
    clustering = PrimaryKeyRelatedField(read_only=True, source="clusteringjob")

    class Meta:
        model = SearchJob
        fields = [
            "id",
            "total",
            "status",
            "params",
            "clustering",
            "created_at",
            "updated_at",
        ]


class PartialClusteringJobSerialiser(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    params = PartialSearchParamsSerialiser(read_only=True)

    class Meta:
        model = ClusteringJob
        fields = [
            "id",
            "total",
            "status",
            "params",
            "created_at",
            "updated_at",
            "search_status",
            "progress",
        ]


class PartialArticleSerialiser(serializers.ModelSerializer):
    analysis = PrimaryKeyRelatedField(read_only=True)
    author = JSONField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "headline",
            "url",
            "author",
            "language",
            "published_at",
            "analysis",
        ]
