import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false,
  locale: 'zh', // set locale
  fallbackLocale: 'en', // set fallback locale
  messages: {
    // Initially empty
  }
});

export async function loadLocaleMessages(locale: string) {
  if (i18n.global.availableLocales.includes(locale)) {
    i18n.global.locale.value = locale;
    return;
  }

  const messages = await import(`./locales/${locale}.json`);
  i18n.global.setLocaleMessage(locale, messages.default);
  i18n.global.locale.value = locale;
}

export default i18n;