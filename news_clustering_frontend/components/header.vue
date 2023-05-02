<script setup>
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'
import { useSticky } from '~~/composables/useSticky';

const route = useRoute();
const currentRoute = route.path

const navigation = [
    { name: 'Search', href: '/', current: false },
    { name: 'Cluster Jobs', href: '/cluster', current: false },
    { name: 'Search Jobs', href: '/search', current: false },
    { name: 'Articles', href: '/article', current: false },
]

const header = ref(null);

onMounted(() => {
    // const { onScroll } = useSticky(header.value, 0)
    // setTimeout(() => onScroll(), 50)
})
</script>


<template>
    <div ref="header" id="header" class="sticky top-0">
        <Disclosure as="nav"
            class="bg-gray-900/90 backdrop-filter backdrop-blur-sm z-40 transition-colors duration-300 lg:z-50 border-b"
            v-slot="{ open }">
            <div class="max-w-full px-2 sm:px-6 lg:px-7">
                <div class="relative flex h-14 items-center justify-between">
                    <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
                        <!-- Mobile menu button-->
                        <DisclosureButton
                            class="inline-flex items-center justify-center rounded-xl p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                            <span class="sr-only">Open main menu</span>
                            <Bars3Icon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
                            <XMarkIcon v-else class="block h-6 w-6" aria-hidden="true" />
                        </DisclosureButton>
                    </div>
                    <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                        <!-- <div class="flex flex-shrink-0 items-center">
                                                    <a href="/">
                                                        <img class="block h-8 w-auto"
                                                            src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                                                            alt="Your Company" />
                                                    </a>
                                                </div> -->
                        <div class="hidden w-full sm:ml-6 sm:block">
                            <div class="flex items-center justify-center space-x-4">
                                <NuxtLink v-for="item in navigation" :key="item.name" :href="item.href"
                                    activeClass="bg-gray-900 text-white"
                                    :class="[item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white', 'rounded-3xl px-3 py-2 text-sm font-medium']"
                                    :aria-current="item.current ? 'page' : undefined">{{ item.name }}</NuxtLink>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <DisclosurePanel class="sm:hidden">
                <div class="space-y-1 px-2 pb-3">
                    <DisclosureButton v-for="item in navigation" :key="item.name" as="a" :href="item.href"
                        activeClass="bg-gray-900 text-white"
                        :class="[item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white', 'block rounded-xl px-3 py-2 text-base font-medium']"
                        :aria-current="item.current ? 'page' : undefined">{{ item.name }}</DisclosureButton>
                </div>
            </DisclosurePanel>
        </Disclosure>
    </div>
</template>
  


<style>
#header {
    z-index: 99;
    width: 100%;
}

.sticky {
    position: fixed;
}

#header-links {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>