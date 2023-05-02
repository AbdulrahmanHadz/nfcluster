<script setup>
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
const emit = defineEmits(["refreshAnalysis", "changeTab"])

const props = defineProps({
    results: {
        type: [Object, null],
        required: true
    },
    refreshText: {
        type: Boolean,
        default: false
    },
    selectedTab: {
        type: Number,
        default: 0
    },
    categories: {
        type: Array,
        required: true
    },
    chartData: {
        type: [Object, null],
        required: true
    },
    searchArticles: {
        type: [Object, null],
        required: true
    },
    clusters: {
        type: [Object, null],
        required: true
    },
    metrics: {
        type: [Object, null],
        required: true
    }
})

function refreshAnalysis(value) {
    emit("refreshAnalysis", value)
}

function changeTab(value) {
    emit("changeTab", value)
}
</script>

<template>
    <div>
        <div v-if="results">
            <div class="flex justify-between items-center">
                <div class="text-base">
                    <a :href="'/search/' + results.search.id"><span class="font-medium text-lg">Search: </span>
                        {{ results.params.q }}</a>
                    <p><span class="font-medium text-lg">Status: </span>{{ results.progress }}</p>
                    <p><span class="font-medium text-lg">Total articles clustered: </span>{{ results.total }}</p>
                </div>
                <div class="flex flex-col place-items-center">
                    <p v-if="refreshText" class="pb-1 text-base font-bold">Refreshing...</p>
                    <button @click="refreshAnalysis"
                        class="bg-blue-700 py-2 px-3 text-white rounded-3xl font-medium text-base z-10">Force
                        Analyse</button>
                </div>
            </div>


            <TabGroup v-if="results.status" @change="changeTab" :selectedIndex="selectedTab" class="w-full pt-4" as="div">
                <TabList class="flex space-x-1 rounded-3xl bg-blue-900/20 p-1">
                    <Tab v-for="category in categories" as="template" :key="category" v-slot="{ selected }">
                        <button :class="[
                            'w-full rounded-3xl py-2.5 text-md font-bold leading-5 text-blue-700',
                            'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none',
                            selected
                                ? 'bg-white shadow'
                                : 'text-blue-100 hover:bg-white/[0.12] hover:text-white',
                        ]">
                            {{ category }}
                        </button>
                    </Tab>
                </TabList>

                <TabPanels class="mt-2 w-full h-full focus:outline-0 hover:outline-0" v-if="clusters">
                    <TabPanel :key="1" class="rounded-xl p-3 hover:outline-none focus:outline-none">
                        <p class="pb-3 font-extrabold text-xl sm:font-black sm:text-2xl justify-start">Analysis
                            overview</p>
                        <div class="flex flex-col md:flex-row justify-between">
                            <ResultsChart v-if="chartData" :labels="categories" :chartData="chartData"
                                chartToShow="polar" />
                            <div class="truncate bg-gray-100 rounded-xl py-2 px-3 h-60 max-w-[80rem] min-w-[12rem]"
                                v-if="metrics">
                                <p>Num Samples: {{ metrics.n_samples }}</p>
                                <p>Num Features: {{ metrics.n_features }}</p>
                                <p>Vectorisation Duration: {{ metrics.vectorisation_duration.toFixed(3) }}</p>
                                <p>LSA Duration: {{ metrics.lsa_duration.toFixed(3) }}</p>
                                <p>Clustering Duration: {{ metrics.cluster_duration.toFixed(3) }}</p>
                                <p>Explained Variance: {{ metrics.explained_variance.toFixed(3) }}</p>
                                <p>DBI Score: {{ metrics.dbi_score.toFixed(3) }}</p>
                                <p>Silhouette Score: {{ metrics.silhouette_score.toFixed(3) }}</p>
                            </div>
                        </div>
                    </TabPanel>

                    <TabPanel :key="2" class="rounded-xl p-3 hover:outline-none focus:outline-none" v-if="searchArticles">
                        <div>
                            <p class="pb-3 font-extrabold text-xl sm:font-black sm:text-2xl">Completed</p>
                            <div class="overflow-auto min-h-[24rem]">
                                <div class="flex flex-row gap-4 place-items-start w-96 h-[calc(100vh_-_550px)]">
                                    <div v-for="cluster in clusters" class="pr-4">
                                        <p
                                            class="col-span-1 md:col-span-2 2xl:col-span-3 pb-1 font-bold text-lg sm:font-extrabold sm:text-xl">
                                            Cluster {{ getKeyByValue(clusters, cluster) }} ({{ cluster.length }}
                                            articles)</p>
                                        <div class="results-grid-cells w-80 flex justify-between items-start py-3 px-4 mb-10"
                                            v-for="article in searchArticles.completed.filter(x => cluster.includes(x.id))">
                                            <a :href="'/article/' + article.id" class="w-full flex">
                                                <div>
                                                    <div class="flex flex-col w-2 whitespace-normal text-lg">
                                                        <span class="font-bold ">Sentmient: </span>{{
                                                            article.analysis.sentiment }}
                                                    </div>
                                                </div>
                                            </a>
                                            <div class="w-[20rem] h-24 whitespace-normal text-right truncate">
                                                <a :href="article.url">{{
                                                    article.headline }}
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div v-if="searchArticles.failed.length > 0" class="pt-3">
                            <p class="pb-3 font-extrabold text-xl sm:font-black sm:text-2xl">Failed Articles</p>
                            <div
                                class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-2 place-items-start w-full">
                                <div v-for="failed in searchArticles.failed"
                                    class="rounded-xl bg-gray-500 truncate p-2 px-3 w-full text-white">
                                    <a :href="failed">{{
                                        failed }}
                                    </a>
                                </div>
                            </div>
                        </div>
                    </TabPanel>
                </TabPanels>
            </TabGroup>
        </div>
        <div v-else>
            <p class="font-extrabold text-2xl">Failed to fetch</p>
        </div>
    </div>
</template>