import Vue from 'vue'   //引入Vue
import Router from 'vue-router'  //引入vue-router
import UserLogin from "../components/UserLogin.vue";
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'User_Login',
      component: UserLogin
    },
    {
      path: '/register',
      name: 'User_Register',
      component: () => import('../components/UserRegister.vue')
    }
  ]
})