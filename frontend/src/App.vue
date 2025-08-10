<script setup lang="ts">
  import Header from './components/Header.vue'
</script>

<template>
  <Header />
  <div class="main-content">
    <router-view #="{ Component }">
      <transition name="fade-page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style scoped>
  .main-content {
    padding-top: 56px;
  }

  .fade-page-enter-active,
  .fade-page-leave-active {
    transition:
      opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1),
      transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .fade-page-enter-from,
  .fade-page-leave-to {
    opacity: 0;
    transform: translateY(24px);
  }

  .fade-page-enter-to,
  .fade-page-leave-from {
    opacity: 1;
    transform: translateY(0);
  }
</style>
