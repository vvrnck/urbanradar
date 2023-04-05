import Vue from 'vue';
import App from './App.vue';

import firebase from 'firebase/app';
import 'firebase/auth';        // for authentication
import 'firebase/analytics';
// import 'firebase/storage';     // for storage
// import 'firebase/database';    // for realtime database
// import 'firebase/firestore';   // for cloud firestore
// import 'firebase/messaging';   // for cloud messaging
// import 'firebase/functions';   // for cloud functions
import router from './routes/router';
import vuetify from './vuetify/vuetify';
import store from './store/store';
import i18n from './i18n/i18n';
import wb from "./registerServiceWorker";

import Mobile from './mobile/App.vue'
import routes from './mobile/routes/routes'
import { isMobile } from './utils';

const tour = require('./tour/tour');

Vue.prototype.$workbox = wb;
Vue.config.productionTip = false;

// Inicializa o Firebase
var config = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
  authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
  databaseURL: process.env.VUE_APP_FIREBASE_DATABASE_URL,
  projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.VUE_APP_FIREBASE_APP_ID,
  measurementId: process.env.VUE_APP_FIREBASE_MEASUREMENT_ID
}

try {
  firebase.initializeApp(config);

  firebase.getCurrentUser = () => {
    return new Promise((resolve, reject) => {
        const unsubscribe = firebase.auth().onAuthStateChanged(user => {
            unsubscribe();
            resolve(user);
        }, reject);
    })
  };
  
  firebase.analytics();
} catch (e) {
  console.error("NO ENV VARIABLES!")
}



if (isMobile()) {
	new Vue({
		i18n,
		router: routes,
		store,
		vuetify,
		render: h => h(Mobile)
	}).$mount('#app');
} else {
	new Vue({
		router,
		vuetify,
		store,
		i18n,
		render: h => h(App),
	}).$mount('#app')
}


