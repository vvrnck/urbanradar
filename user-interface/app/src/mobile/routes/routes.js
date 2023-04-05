import Vue from 'vue'
import Router from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import MapPage from '../views/MapPage.vue'
import firebase from 'firebase/app';
import 'firebase/auth';

Vue.use(Router)

const routes = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '*',
      redirect: '/'
    },
    {
      path: '/',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/map',
      name: 'map',
      component: MapPage
    },
  ]
})

routes.beforeEach((to, from, next) => {
  const currentUser = firebase.auth().currentUser
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !currentUser) next('login')
  else next()
})

export default routes
