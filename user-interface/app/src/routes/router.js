import Vue from 'vue';
import VueRouter from 'vue-router';
import firebase from 'firebase/app';
import 'firebase/auth';

import { FeedbackPage, LoginPage, MapPage, ManagementPage, AdminPage, ConfigPage } from '../views';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginPage
    },   
    {
      path: '/config',
      name: 'config',
      component: ConfigPage,
    },
    {
      path: '/map',
      name: 'map',
      component: MapPage,
      props: true,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/management',
      name: 'management',
      component: ManagementPage,
      props: true,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: FeedbackPage,
      props: true,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPage,
      props: true,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '*',
      redirect: '/'
    },
  ]
});


router.beforeEach(async (to,from,next) =>{
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    if (requiresAuth && !await firebase.getCurrentUser()) next('login');
    else next();
});

export default router;
