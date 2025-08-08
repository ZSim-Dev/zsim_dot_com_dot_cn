<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import { loadLocaleMessages } from '@/i18n'

  const { locale } = useI18n()

  async function switchLanguage(lang: string) {
    await loadLocaleMessages(lang)
    localStorage.setItem('locale', lang)
  }
</script>

<template>
  <div class="language-switcher">
    <button @click="switchLanguage('zh')" :class="{ active: locale === 'zh' }">中</button>
    <button @click="switchLanguage('en')" :class="{ active: locale === 'en' }">EN</button>
  </div>
</template>

<style scoped>
  .language-switcher {
    display: flex;
    align-items: center;
    margin-left: 8px;
    background-color: var(--color-background-mute);
    border-radius: 16px;
    padding: 4px;
  }

  .language-switcher button {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 14px;
    transition:
      background-color 0.3s,
      color 0.3s;
  }

  .language-switcher button.active {
    background-color: var(--color-background);
    color: var(--text-primary);
    font-weight: 600;
  }
</style>
