<script setup>
definePageMeta({
    validate: async (route) => {
        return ["cluster", "article", "search"].includes(route.params.slug)
    }
})

const route = useRoute()
const slug = route.params.slug
const routeId = route.params.id

</script>

<template>
    <div class="w-9/12 min-w-min sm:w-10/12 py-2">
        <div class="w-full h-full">
            <PageModellingSearchList v-if="['cluster', 'search'].includes(slug) && !routeId"></PageModellingSearchList>
            <PageModellingArticleList v-if="['article'].includes(slug) && !routeId"></PageModellingArticleList>
            <div class="pt-3" v-if="routeId">
                <div class="flex flex-col px-4 py-3 bg-gray-300 rounded-xl">
                    <PageModellingClusterSingle v-if="slug == 'cluster' && routeId"></PageModellingClusterSingle>
                    <PageModellingSearchSingle v-else-if="slug == 'search' && routeId"></PageModellingSearchSingle>
                    <PageModellingArticleSingle v-else-if="slug == 'article' && routeId"></PageModellingArticleSingle>
                </div>
            </div>
        </div>
        <div class="footer-padding"></div>
    </div>
</template>