import { createRouter, createWebHashHistory } from "vue-router";
import contrast from '../components/contrast/contrastMain.vue'
import process from '../components/process/processMain.vue'
import test from '../components/testModel/testModelMain.vue'

const routes =[
    {
        path:'/',
        component:() => import('@/components/mainPage.vue')
    },
    {
        path:'/contrast',
        component:contrast
    },
    {
        path:'/process',
        component:process
    },
    {
        path:'/test',
        component:test,
    },
]
export const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
})

export default router