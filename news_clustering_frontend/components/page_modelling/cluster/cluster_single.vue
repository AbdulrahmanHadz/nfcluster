<script setup>
const route = useRoute();
const router = useRouter();
const clusterId = route.params.id
const chartData = ref(null);
const results = ref(null);
const title = ref(clusterId);

const categories = ref(["Simplified", "Detailed"]);
const selectedTab = ref(0);
const refreshText = ref(false);
const searchArticles = ref(null);
const clusters = ref(null);
const metrics = ref(null);

const compKey = ref(1);

if (route.query.tab && categories.value.map(x => x.toLowerCase()).includes(route.query.tab)) {
    selectedTab.value = categories.value.map(x => x.toLowerCase()).indexOf(route.query.tab);
}

useHead({ title: () => `Cluster - ${title.value}` })


async function fetchClusterData() {

    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/cluster/${clusterId}/`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });
    results.value = data.value

    if (!pending.value && !error.value && results.value) {
        title.value = `${results.value.params.q} - ${clusterId}`

        if (results.value.analysis) {
            clusters.value = results.value.analysis.clusters
            chartData.value = {
                labels: Object.keys(clusters.value).map(x => `Cluster ${x}`),
                datasets: [{
                    label: ['Articles'],
                    data: Object.values(clusters.value).map(x => x.length),
                    backgroundColor: generateRandomColoursArray(results.value.analysis.clusters),
                    hoverOffset: 40
                }]
            }

            metrics.value = results.value.analysis.metrics

            if (route.query.tab == 'detailed') {
                await fetchSearchData()
            }
        }
    }
}

await fetchClusterData()

function updateUrl(query) {
    const newParams = { ...useRoute().query, ...query }
    router.replace({
        query: newParams
    })
}

async function fetchSearchData() {
    if (results.value.search != null) {
        const { data, pending, error, refresh } = await useFetch(`${apiUrl}/search/${results.value.search.id}/`, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        searchArticles.value = data.value
    }
}

function changeTab(index) {
    selectedTab.value = index
    let tabToGo = categories.value[index].toLowerCase()
    updateUrl({ tab: tabToGo })

    if (selectedTab.value == 1 && !searchArticles.value) {
        fetchSearchData()
            .then(res => { })
    }
}


async function refreshAnalysis(event) {
    refreshText.value = true;

    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/cluster/${clusterId}/analyse/`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    setTimeout(() => {
        console.log('refreshing data after analysis')
        fetchClusterData()
            .then()
        refreshText.value = false;
        compKey.value++;
    }, 10000)
}
</script>

<template>
    <PageModellingClusterComponent :key="compKey" :results="results" :refreshText="refreshText" :selectedTab="selectedTab"
        :categories="categories" :chartData="chartData" :searchArticles="searchArticles" :clusters="clusters"
        :metrics="metrics" @refreshAnalysis="refreshAnalysis" @changeTab="changeTab" />
</template>
