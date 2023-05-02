<script setup>
const route = useRoute();
const router = useRouter();
const articleId = route.params.id
const results = ref(null);
const title = ref(articleId);

const refreshText = ref(false);

useHead({ title: () => `Article - ${title.value}` })


async function fetchArticleData() {

    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/article/${articleId}/`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });
    results.value = data.value

    if (!pending.value && !error.value && results.value) {
        title.value = `${results.value.headline}`
    }
}

await fetchArticleData()


async function refreshAnalysis(event) {
    refreshText.value = true;

    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/article/${articleId}/analyse/`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    setTimeout(() => {
        fetchArticleData()
            .then()
        refreshText.value = false;
    }, 10000)
}
</script>

<template>
    <div>
        <div v-if="results">
            <div class="flex justify-between items-center">
                <a :href="results.url">
                    <h1 class="font-black text-3xl pr-10">{{ results.headline }}</h1>
                </a>
                <div class="flex flex-col place-items-center">
                    <p v-if="refreshText" class="pb-1 text-base font-bold">Refreshing...</p>
                    <button @click="refreshAnalysis"
                        class="bg-blue-700 py-2 px-3 text-white rounded-3xl font-medium text-base">Force Analyse</button>
                </div>
            </div>


            <div class="overflow-auto min-h-[5rem] max-h-96 px-4 my-4">
                <article class="leading-normal">{{ results.article }}</article>
            </div>

            <div class="flex flex-row justify-between gap-3">
                <div class="h-min" v-if="results.author && results.author.length > 0">
                    <p class="text-lg font-semibold">Author(s)</p>
                    <p
                        class="text-sm w-24 sm:w-72 md:w-96 bg-slate-200 rounded-xl p-3 min-h-min h-min truncate sm:whitespace-normal">
                        {{
                            results.author.join(', ')
                        }}
                    </p>
                </div>
                <div :class="['h-min', results.author && results.author.length > 0 ? 'float-right text-write' : '']"
                    v-if="results.analysis">
                    <p class="text-lg font-semibold pb-2">Analysis</p>
                    <div
                        class="text-sm w-6/12 sm:w-8/12 md:w-11/12 max-w-xs bg-slate-200 rounded-xl p-3 min-h-min h-min truncate sm:whitespace-normal">
                        <div v-if="results.analysis.sentiment_analysis" class="flex flex-col">
                            <p>Polarity: {{ results.analysis.sentiment_analysis.polarity }} </p>
                            <p>Subjectivity: {{ results.analysis.sentiment_analysis.subjectivity }} </p>
                        </div>
                        <p v-if="results.analysis.sentiment">Sentiment: {{ results.analysis.sentiment }} </p>
                        <div class="flex flex-wrap pt-2 gap-2" v-if="results.analysis.sentiment_analysis.neg">
                            <div>
                                <p>Negative</p>
                                <p>{{ results.analysis.sentiment_analysis.neg }}</p>
                            </div>
                            <div>
                                <p>Neutral</p>
                                <p>{{ results.analysis.sentiment_analysis.neu }}</p>
                            </div>
                            <div>
                                <p>Positive</p>
                                <p>{{ results.analysis.sentiment_analysis.pos }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-gray-300 rounded-xl flex justify-between font-bold text-base pt-4">
                <p>Published {{ formatRelativeDate(results.published_at) }}</p>
                <p>Language {{ results.language }}</p>
            </div>
        </div>
        <div v-else>
            <p class="font-extrabold text-2xl">Failed to fetch</p>
        </div>
    </div>
</template>