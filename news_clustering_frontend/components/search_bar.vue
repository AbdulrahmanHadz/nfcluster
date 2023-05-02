<script setup>
import SearchIcon from '../assets/icons/SearchIcon.vue';
const emit = defineEmits('updateResponseMessage');

const query_search = ref(null);


async function onSubmit() {
    if (query_search.value != null && query_search.value.length == 0) {
        query_search.value = null;
    }
    console.log(query_search.value);

    if (query_search.value == null) {
        return;
    }

    const { data, pending, error, refresh } = await useFetch(`${apiUrl}/cluster/`, {
        method: "POST",
        body: { "q": query_search.value },
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    if (data) {
        emit('updateResponseMessage', data.value)
    }
}

</script>

<template>
    <div class="w-full">
        <form class="w-full" @submit.prevent="onSubmit">
            <div class="relative justify-center items-center w-full">
                <div class="hidden absolute inset-y-0 left-0 sm:flex items-center pl-3 pointer-events-none">
                    <SearchIcon class="w-5 h-5 text-gray-300" />
                </div>
                <input type="search" id="search"
                    class="block w-full p-4 sm:pl-10 sm:pr-[5.3rem] text-sm rounded-xl bg-gray-800 border-gray-500 placeholder-gray-300 text-white focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Search for a topic" v-model="query_search">
                <button type="submit"
                    class="text-white absolute right-2.5 top-2 focus:ring-4 focus:outline-none font-medium rounded-3xl text-sm bg-blue-600 hover:bg-blue-700 focus:ring-blue-800">
                    <div class="hidden sm:block px-4 py-2">
                        Cluster Search
                    </div>
                    <div class="block sm:hidden px-2 py-2">
                        <SearchIcon class="w-5 h-5 text-gray-300" />
                    </div>
                </button>
            </div>
        </form>
    </div>
</template>