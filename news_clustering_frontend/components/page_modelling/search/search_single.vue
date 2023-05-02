<script setup>
const route = useRoute();
const searchId = route.params.id
const results = ref(null);
const title = ref(searchId);

const refreshText = ref(false);

useHead({ title: () => `Search - ${title.value}` })


async function fetchSearchData() {

    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/search/${searchId}/`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });
    results.value = data.value

    if (!pending.value && !error.value && results.value) {
        title.value = `${results.value.params.q} - ${searchId}`
    }
}

await fetchSearchData()


async function refreshAnalysis(event) {
    refreshText.value = true;

    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/search/${searchId}/analyse/`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    setTimeout(() => {
        fetchSearchData()
            .then()
        refreshText.value = false;
    }, 3000)
}
</script>

<template>
    <div>
        <div v-if="results">
            <div class="flex justify-between items-center">
                <div class="text-base">
                    <p><span class="font-medium text-lg">Status: </span>{{ results.status ? 'Completed' : 'In Progress' }}
                    </p>
                    <p><span class="font-medium text-lg">Total articles: </span>{{ results.total }}</p>
                    <p><span class="font-medium text-lg">Search for: </span>{{ results.params.q }}</p>
                    <p><span class="font-medium text-lg">Searched At: </span>{{ formatRelativeDate(results.created_at) }}
                    </p>
                </div>
                <div class="flex flex-col place-items-center">
                    <p v-if="refreshText" class="pb-1 text-base font-bold">Refreshing...</p>
                    <button @click="refreshAnalysis"
                        class="bg-blue-700 py-2 px-3 text-white rounded-3xl font-medium text-base">Force Analyse</button>
                </div>
            </div>

            <div class="rounded-xl p-3">
                <div>
                    <p class="pb-3 font-extrabold text-xl sm:font-black sm:text-2xl">Completed ({{
                        results.completed.length }} articles)</p>
                    <div class="overflow-auto min-h-[24rem] min-w-fit">
                        <div class="flex flex-wrap gap-4 place-items-start w-full h-[calc(100vh_-_550px)]">
                            <div v-for="article in results.completed"
                                class="results-grid-cells w-80 flex items-start py-3 px-4">
                                <NuxtLink :href="'/article/' + article.id" class="w-full flex">
                                    <div>
                                        <div class="flex flex-col w-2 whitespace-normal text-lg" v-if="article.analysis">
                                            <span class="font-bold ">Sentmient: </span>{{
                                                article.analysis.sentiment }}
                                        </div>
                                        <div v-else>
                                            <p>article link</p>
                                        </div>
                                    </div>
                                </NuxtLink>
                                <div class="w-[20rem] h-24 whitespace-normal text-right truncate">
                                    <NuxtLink :href="article.url">{{
                                        article.headline }}
                                    </NuxtLink>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="results.failed.length > 0" class="pt-3">
                    <p class="pb-3 font-extrabold text-xl sm:font-black sm:text-2xl">Failed ({{ results.failed.length }}
                        articles)</p>
                    <div
                        class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-2 place-items-start w-full">
                        <div v-for="failed in results.failed"
                            class="rounded-xl bg-gray-500 truncate p-2 px-3 w-full text-white">
                            <NuxtLink :href="failed">{{
                                failed }}
                            </NuxtLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <p class="font-extrabold text-2xl">Failed to fetch</p>
        </div>
    </div>
</template>