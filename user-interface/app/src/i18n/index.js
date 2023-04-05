import en from '../../public/locales/en.json';
import pt from '../../public/locales/pt.json';

export const defaultLocale = process.env.VUE_APP_DEFAULT_LOCALE;

export const languages = {
  en: en,
  pt: pt,
}