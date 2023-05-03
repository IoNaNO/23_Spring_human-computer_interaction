import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name:'search',
        component: () => import('~/components/search.vue')
    },
    {
        path:'/favorite',
        name:'favorite',
        component: () => import('~/components/favorite.vue')
    },
    {
        path:'/settings',
        name:'settings',
        component:()=>import('~/components/settings.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
});

export default router