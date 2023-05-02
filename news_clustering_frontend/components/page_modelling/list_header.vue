<script setup>
const emit = defineEmits(['pageToGo', 'ordering']);

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
        default: 'articles'
    },
    orderingItems: {
        type: Array,
        default: [
            { "name": "Created - Ascending", "value": "created_at" },
            { "name": "Created - Descending", "value": "-created_at" },
            { "name": "Updated - Ascending", "value": "updated_at" },
            { "name": "Updated - Descending", "value": "-updated_at" },
        ]
    },
    emitEvent: {
        type: String,
        default: 'ordering'
    },
    dropdownName: {
        type: String,
        default: 'Ordering'
    },
    currentRoute: {
        type: String,
        required: true
    }
})

const orderingHandler = (value) => {
    emit('ordering', value)
    console.log("ordering " + value)
};

const paginationHandler = (page) => {
    emit('pageToGo', page)
    console.log("page to go " + page)
};

</script>

<template>
    <div class="flex justify-between items-center flex-grow">
        <Pagination :key="pageToSearch" :totalResults="totalResults" :pageSize="pageSize" :pageToSearch="pageToSearch"
            @pageToGo="paginationHandler" />

        <h1 class="font-extrabold text-xl sm:font-extrabold sm:text-2xl">{{ currentRoute }}</h1>

        <MenuDropdown :class="[totalResults < pageSize ? 'justify-end' : '']" @ordering="orderingHandler"
            :orderingItems="orderingItems" :emitEvent="emitEvent" :dropdownName="dropdownName" />
    </div>
</template>