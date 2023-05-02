import { VueWindowSizePlugin } from 'vue-window-size/plugin';

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.use(VueWindowSizePlugin)
})