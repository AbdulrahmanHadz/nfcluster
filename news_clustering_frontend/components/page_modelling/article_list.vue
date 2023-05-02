<script setup>
const route = useRoute();
const router = useRouter();
const clusterResults = ref(null);
const totalResults = ref(0);
const pageToSearch = ref(1);
const currentGroup = route.params.slug;
const ordering = ref('-published_at');
const results = ref(null);
const pageSize = ref(100);


useHead(({ title: () => `${capitalise(currentGroup)}s | Page ${pageToSearch.value}` }))


if (isNumeric(route.query.page)) {
    pageToSearch.value = parseInt(route.query.page)
}

if (["published_at", "language", "url", "-published_at", "-language", "-url"].includes(route.query.ordering)) {
    ordering.value = route.query.ordering
}

async function fetchData() {
    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/${currentGroup}/`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        query: {
            "page": pageToSearch.value,
            "ordering": ordering.value
        }
    });
    results.value = data.value

    if (!pending.value && !error.value && results.value) {
        const data2 = results.value
        clusterResults.value = data2.results.map(x => {
            x["href"] = `/${currentGroup}/${x["id"]}`;
            return x;
        })
        totalResults.value = data2.count
        pageSize.value = data2.page_size
    }
}

await fetchData()

function updateUrl(query) {
    const newParams = { ...useRoute().query, ...query }
    router.replace({
        query: newParams
    })
}

function updateOrder(value) {
    ordering.value = value
    updateUrl({ 'ordering': value })
    fetchData()
        .then(res => {
            console.log("res " + res)
        })
}

function updatePage(value) {
    pageToSearch.value = parseInt(value)
    updateUrl({ 'page': value })
    fetchData()
        .then(res => {
            console.log("res " + res)
        })
}

const orderingItems = [
    { "name": "Published - Ascending", "value": "published_at" },
    { "name": "Published - Descending", "value": "-published_at" },
    { "name": "Language - Ascending", "value": "language" },
    { "name": "Language - Descending", "value": "-language" },
    { "name": "Url - Ascending", "value": "url" },
    { "name": "Url - Descending", "value": "-url" },
]
</script>


<template>
    <div class="w-full h-full">
        <PageModellingListHeader :results="Boolean(results)" :totalPages="results.total_pages" :totalResults="totalResults"
            :pageSize="pageSize" :pageToSearch="pageToSearch" @pageToGo="updatePage" @ordering="updateOrder"
            :orderingItems="orderingItems" current-route="Article" />


        <div class="resuls-grid-layout">
            <div v-for="cluster in clusterResults">
                <div class="results-grid-cells h-52">
                    <NuxtLink :href="cluster.href">
                        <p class="truncate text-3xl sm:text-3xl font-black">{{
                            cluster.headline }}</p>
                        <p class="text-xl sm:text-2xl font-extrabold">Analysed? {{ cluster.analysis ? 'Yes' : 'No' }}</p>
                        <NuxtLink :href="cluster.url">
                            <p class="truncate text-l sm:text-xl font-bold">Article link</p>
                        </NuxtLink>
                        <p class="text-l sm:text-xl font-bold">Language: {{ cluster.language }}</p>
                        <p class="text-l sm:text-xl font-bold">{{ formatRelativeDate(cluster.published_at) }}</p>
                    </NuxtLink>
                </div>
            </div>
        </div>

        <PageModellingListFooter :results="Boolean(results)" :totalPages="results.total_pages" :totalResults="totalResults"
            :pageSize="pageSize" :pageToSearch="pageToSearch" @pageToGo="updatePage" resultsType="articles" />
    </div>
</template>
