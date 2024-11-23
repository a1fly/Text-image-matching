import Vue from 'vue';
import Router from 'vue-router';
import Login from '../components/UserLogin.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
});