import Vue from 'vue';
import VueI18n from 'vue-i18n';
import { languages, defaultLocale } from './';

Vue.use(VueI18n);

const messages = Object.assign({}, languages);

var i18n = new VueI18n({
  locale: defaultLocale,
  fallbackLocale: 'en',
  messages
})

window.i18n = i18n;

export default i18n;