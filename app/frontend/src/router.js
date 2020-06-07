import Vue from "vue";
import VueRouter from "vue-router";
import Page from "./pages/Page";
import Result from "./pages/Result"
import Index from "./pages/Index"

Vue.use(VueRouter);

const routes = [
    { path: "/index", component: Index },
    { path: "/", component: Index },
    { path: "/search/:method/:query", component: Result },
    { path: "/page/:id", component: Page }
];

export default new VueRouter({
    routes,
});
