import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter)
import userLogin from '../components/UserLogin.vue';
import userReg from '../components/UserRegister.vue';
import Mainhome from '../components/Mainhome.vue';
import WriteInfo from "@/components/writeInfo.vue";
import ViewInfo from "@/components/View_Info.vue";
import SmartSearch from "@/components/SmartSearch.vue";

const routes = [
    {path: '/login', component: userLogin},
    {path: "/reg", component: userReg},
    {path: "/home", component: Mainhome},
    {path: "/write", component: WriteInfo},
    {path: "/view", component: ViewInfo},
    {path: "/search", component: SmartSearch},

]

const router = new VueRouter({
    mode: 'history',
    routes:routes
});

export default router