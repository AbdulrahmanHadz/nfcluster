from django.contrib import admin

from clustering.models.models import SearchParams, ArticleURL, Article, ClusteringJob

admin.site.register(SearchParams)
admin.site.register(ArticleURL)
admin.site.register(Article)
# admin.site.register(ClusteringResult)
admin.site.register(ClusteringJob)
