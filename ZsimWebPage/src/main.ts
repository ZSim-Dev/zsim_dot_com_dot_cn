import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import i18n, { loadLocaleMessages } from './i18n'

const app = createApp(App)

app.use(router)
app.use(i18n)

const userPreferredLocale = localStorage.getItem('locale') || 'zh';

async function initializeApp() {
  await loadLocaleMessages(userPreferredLocale);
  app.mount('#app');
}

initializeApp();