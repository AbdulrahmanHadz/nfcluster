// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    css: ['~/assets/main.css'],
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        }
    },
    // hooks: {
    //     'pages:extend'(pages) {
    //         // add a route
    //         pages.push({
    //             name: 'profile',
    //             path: '/profile',
    //             file: '~/extra-pages/profile.vue'
    //         })
    //         // remove routes
    //         function removePagesMatching(pattern: RegExp, pages: NuxtPage[] = []) {
    //             const pagesToRemove = []
    //             for (const page of pages) {
    //                 if (pattern.test(page.file)) {
    //                     pagesToRemove.push(page)
    //                 } else {
    //                     removePagesMatching(pattern, page.children)
    //                 }
    //             }
    //             for (const page of pagesToRemove) {
    //                 pages.splice(pages.indexOf(page), 1)
    //             }
    //         }
    //         removePagesMatching(/\.ts$/, pages)
    //     }
    // },
    ssr: false
})
