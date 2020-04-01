import Vue from 'vue'
import Router from 'vue-router'
import Auth from '@/components/Auth'
import Home from "../components/Home";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'auth',
      component: Auth
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
  ]
})
