<script setup>
const route = useRoute();
const router = useRouter();
const clusterResults = ref(null);
const totalResults = ref(0);
const pageToSearch = ref(1);
const currentGroup = route.params.slug;
const ordering = ref('-created_at');
const results = ref(null);
const pageSize = ref(100);
const resultsType = currentGroup == 'cluster' ? 'clustering jobs' : 'search jobs';


useHead(({ title: () => `${capitalise(currentGroup)} Jobs | Page ${pageToSearch.value}` }))

if (isNumeric(route.query.page)) {
    pageToSearch.value = parseInt(route.query.page)
}

if (["created_at", "updated_at", "-created_at", "-updated_at"].includes(route.query.ordering)) {
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
        clusterResults.value = data2.results.filter(x => x.params).map(x => {
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
</script>


<template>
    <div class="w-full h-full">
        <PageModellingListHeader :results="Boolean(results)" :totalPages="results.total_pages" :totalResults="totalResults"
            :pageSize="pageSize" :pageToSearch="pageToSearch" @pageToGo="updatePage" @ordering="updateOrder"
            :currentRoute="capitalise(currentGroup) + ' Jobs'" />

        <div class="resuls-grid-layout">
            <div v-for="cluster in clusterResults">
                <div v-if="cluster.params" class="results-grid-cells h-52">
                    <NuxtLink :href="cluster.href">
                        <p class="truncate text-3xl sm:text-3xl font-black">{{ cluster.params.q }}</p>
                        <p class="text-xl sm:text-2xl font-extrabold">{{ cluster.total }} articles</p>
                        <p class="text-xl sm:text-2xl font-extrabold">Completed? {{ cluster.status ? 'Yes' : 'No' }}</p>
                        <p class="text-l sm:text-xl font-bold" v-if="cluster.params.num_clusters">Clusters: {{
                            cluster.params.num_clusters }}</p>
                        <p class="text-l sm:text-xl font-bold">{{ formatRelativeDate(cluster.updated_at) }}</p>
                    </NuxtLink>
                </div>
            </div>
        </div>

        <PageModellingListFooter :results="Boolean(results)" :totalPages="results.total_pages" :totalResults="totalResults"
            :pageSize="pageSize" :pageToSearch="pageToSearch" @pageToGo="updatePage" :resultsType="resultsType" />
    </div>
</template>

