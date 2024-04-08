/*
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2022-11-20 18:21:36
 * @LastEditTime: 2023-01-26 12:53:24
 */
import {createRouter, createWebHashHistory, createWebHistory} from "vue-router";
import HomeView from "../views/HomeView.vue";
import MainView from "../views/MainView.vue"

const router = createRouter({
    // history: createWebHistory(import.meta.env.BASE_URL),
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView,
        },
        {
            path: "/main",
            name: "main",
            component: MainView,
            // query: this.$route.query,
            // hash: this.$route.hash,
        },
        // {
        //   path: "/about",
        //   name: "about",
        //   // route level code-splitting
        //   // this generates a separate chunk (About.[hash].js) for this route
        //   // which is lazy-loaded when the route is visited.
        //   component: () => import("../views/AboutView.vue"),
        // },
    ],
});

export default router;
