<script setup>
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/20/solid';
import { useWindowSize } from 'vue-window-size';

const { width, _ } = useWindowSize();

const emit = defineEmits(['pageToGo'])
const route = useRoute();

const onClickHandler = (page) => {
    emit('pageToGo', page)
    console.log("page to go " + page)
};

const windowWidth = width;
const pageToGoTo = ref(1);
const maxPagesToShow = ref(5);

const props = defineProps({
    totalResults: {
        type: Number,
        default: 0
    },
    pageSize: {
        type: Number,
        default: 100
    },
    pageToSearch: {
        type: Number,
        default: 1
    }
});

const propsRef = toRefs(props);
pageToGoTo.value = propsRef.pageToSearch.value;

function updateWidth(newWidth) {
    if (newWidth <= 640) {
        maxPagesToShow.value = 1;
    }
    else if (newWidth <= 768) {
        maxPagesToShow.value = 3;
    }
    else if (newWidth <= 1280) {
        maxPagesToShow.value = 5;
    } else {
        maxPagesToShow.value = 10;
    }
}

watch(windowWidth, (newWidth) => {
    updateWidth(newWidth)
})

onMounted(() => {
    updateWidth(windowWidth.value)
})

</script>


<template>
    <div class="pagination-comp" v-if="totalResults > pageSize">
        <vue-awesome-paginate :total-items="totalResults" :items-per-page="pageSize" :max-pages-shown="maxPagesToShow"
            :show-breakpoint-buttons="false" v-model="pageToGoTo" :on-click="onClickHandler" type="link"
            link-url="?page=[page]">
            <template #prev-button>
                <ChevronLeftIcon class="h-5 w-full" aria-hidden="true" />
            </template>

            <template #next-button>
                <span>
                    <ChevronRightIcon class="h-5 w-full" aria-hidden="true" />
                </span>
            </template>
        </vue-awesome-paginate>
    </div>
</template>

<style>
.pagination-comp .pagination-container {
    background-color: white;
    border-radius: 0.75rem;
}

.pagination-comp .paginate-buttons {
    width: 40px;
    height: 40px;
    /* padding-top: 0.25rem;
    padding-bottom: 0.25rem;

    padding-right: 0.25rem;
    padding-left: 0.25rem; */

    margin-inline: 0px;
    cursor: pointer;
    border: none;
    background-color: transparent;
    border-radius: 0.75rem;
    /* margin-left: -1px; */
}

.pagination-comp .active-page {
    background-color: rgb(79 70 229);
    color: #fff;
}

.pagination-comp .paginate-buttons:hover {
    background-color: #e5e5e5;

    --tw-ring-offset-width: 0px;
    box-shadow: inset 0 0 0 calc(1px + var(--tw-ring-offset-width)) #e5e5e5;
}

.pagination-comp .active-page:hover {
    background-color: #362AD4;
    color: #fff;

    --tw-ring-offset-width: 0px;
    box-shadow: inset 0 0 0 calc(1px + var(--tw-ring-offset-width)) #362AD4;
}

.pagination-comp .back-button:active,
.pagination-comp .next-button:active {
    background-color: #dedede;
}
</style>