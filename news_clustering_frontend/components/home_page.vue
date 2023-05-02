<script setup>
const responseMessage = ref(null);
const clusterId = ref(null);

useHead({ title: 'Search' })

function searchMessage(value) {
    if (value.status == 'ok') {
        clusterId.value = value.id
    } else {
        responseMessage.value = value.message
    }
}

</script>

<template>
    <div class="w-9/12 max-w-screen-sm min-w-0 sm:w-10/12 flex flex-col">
        <div class="pb-4 text-xl font-extrabold">
            <p v-if="responseMessage">{{ responseMessage }}</p>
            <NuxtLink v-if="clusterId" :href="'/cluster/' + clusterId">Search successful, click to go to cluster.</NuxtLink>
        </div>
        <div class="flex flex-row w-full">
            <SearchBar @updateResponseMessage="searchMessage" />
        </div>
    </div>
</template>