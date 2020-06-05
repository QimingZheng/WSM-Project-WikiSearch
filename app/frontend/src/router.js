import Vue from "vue";
import VueRouter from "vue-router";
import Page from "./pages/Page";
import Result from "./pages/Result"
import Search from "./pages/Search"

Vue.use(VueRouter);

const routes = [
    { path: "/index", component: Search },
    { path: "/", component: Search },
    { path: "/result", component: Result },
    { path: "/page/:id", component: Page }
];

export default new VueRouter({
    routes,
});
