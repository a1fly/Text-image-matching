import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter)
import userLogin from '../components/UserLogin.vue';
import userReg from '../components/UserRegister.vue';

const routes = [
    {path: '/login', component: userLogin},
    {path: "/reg", component: userReg},

]

const router = new VueRouter({
    mode: 'history',
    routes:routes
});

export default router