<script setup>
const emit = defineEmits(['pageToGo']);

const props = defineProps({
    results: {
        type: Boolean,
        default: false
    },
    totalPages: {
        type: Number,
        default: 0
    },
    totalResults: {
        type: Number,
        default: 0
    },
    pageSize: {
        type: Number,
        default: 5
    },
    pageToSearch: {
        type: Number,
        default: 1
    },
    resultsType: {
        type: String,
        default: ''
    }
})
const propsRef = toRefs(props);

const showPagination = propsRef.results.value && propsRef.totalPages.value > 1


const onClickHandler = (page) => {
    emit('pageToGo', page)
    console.log("page to go " + page)
};

</script>

<template>
    <div>
        <div class="footer-padding"></div>
        <div
            class="fixed flex flex-row items-center left-1/2 -translate-x-2/4 bg-white/90 bottom-0 p-2 z-1 backdrop-blur-sm rounded-3xl mb-2">
            <div class="px-3 w-max text-lg font-extrabold">{{ totalResults }} <span
                    :class="showPagination ? 'hidden sm:inline' : 'inline'">{{ resultsType }}</span>
            </div>
            <Pagination v-if="showPagination" :key="pageToSearch" :totalResults="totalResults" :pageSize="pageSize"
                :pageToSearch="pageToSearch" @pageToGo="onClickHandler" />
        </div>
    </div>
</template>