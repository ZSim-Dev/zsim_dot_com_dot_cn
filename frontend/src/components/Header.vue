<template>
  <header class="zsim-header fixed-header">
    <!-- 汉堡菜单按钮，仅在小屏显示 -->
    <button class="menu-toggle" @click.stop="menuOpen = !menuOpen" aria-label="展开菜单">
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </button>
    <div class="header-left" @click="goHome" style="cursor: pointer">
      <img src="/zsim-logo.svg" alt="logo" class="logo" />
      <span class="zsim-title">{{ t('message.nav-title') }}</span>
    </div>
    <!-- 普通菜单，大屏显示 -->
    <nav class="header-menu">
      <button v-for="item in menuItems" :key="item.label" class="menu-btn" @click="item.action">
        {{ t(item.label) }}
      </button>
    </nav>
    <div class="header-right">
      <GitHubButton class="desktop-only" />
      <LanguageSwitcher />
      <UserAuth @close-menu="menuOpen = false" />
    </div>
    <!-- 弹出菜单，小屏显示 -->
    <transition name="mobile-menu-fade">
      <div v-if="menuOpen" class="mobile-menu" @click.self="menuOpen = false">
        <button v-for="item in menuItems" :key="item.label" class="menu-btn" @click="item.action">
          {{ t(item.label) }}
        </button>
        <div class="mobile-menu-divider"></div>
        <div class="mobile-menu-btn-group">
          <GitHubButton />
        </div>
        <UserAuth show-mobile-auth @close-menu="menuOpen = false" />
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from './LanguageSwitcher.vue'
import UserAuth from './UserAuth.vue'
import GitHubButton from './GitHubButton.vue'

const { t } = useI18n()
const router = useRouter()
const menuOpen = ref(false)

const menuItems = [
  { label: 'message.home', action: () => goHome() },
  { label: 'message.download', action: () => goTo('/downloads') },
  { label: 'message.docs', action: () => goTo('/docs') },
  { label: 'message.vote', action: () => goTo('/vote') },
]

function goHome() {
  router.push('/')
  menuOpen.value = false
}

function goTo(url: string) {
  if (url.startsWith('http')) {
    window.open(url, '_blank')
  } else {
    router.push(url)
  }
  menuOpen.value = false
}
</script>

<style scoped>
.zsim-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 56px;
  padding: 0 16px;
  background: var(--header-bg);
  border-bottom: 1px solid var(--header-border);
  box-shadow: 0 2px 8px var(--header-shadow);
  position: relative;
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease;
}

.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  margin-right: 0;
  padding-left: 12px;
}

.logo {
  width: 32px;
  height: 32px;
  margin-right: 10px;
}

.zsim-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 1px;
  transition: color 0.3s ease;
}

.header-menu {
  display: flex;
  padding-left: 28px;
  margin-left: 0;
  gap: 0;
}

.menu-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 4px;
  transition:
    background 0.3s ease,
    color 0.3s ease;
}

.menu-btn + .menu-btn {
  margin-left: 8px;
}

.menu-btn:hover {
  background: var(--hover-bg);
}

.header-right {
  display: flex;
  align-items: center;
  margin-left: auto;
  gap: 8px;
}

/* 汉堡按钮样式 */
.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  background: none;
  border: none;
  margin-left: 8px;
  cursor: pointer;
  z-index: 110;
}

.menu-toggle .bar {
  width: 22px;
  height: 2px;
  background: var(--text-primary);
  color: var(--text-primary);
  margin: 3px 0;
  border-radius: 2px;
  transition: all 0.3s ease;
}

/* 移动端弹出菜单 */
.mobile-menu {
  position: absolute;
  top: 56px;
  left: 0;
  width: 100vw;
  background: var(--header-bg);
  box-shadow: 0 2px 8px var(--header-shadow);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 12px 0;
  z-index: 120;
  border-bottom: 1px solid var(--header-border);
  transition: background-color 0.3s ease;
}

.mobile-menu .menu-btn {
  width: 100%;
  text-align: left;
  padding: 10px 24px;
  font-size: 18px;
  border-radius: 0;
  margin: 0;
}

.mobile-menu-divider {
  width: 100%;
  height: 1px;
  background: var(--header-border);
  margin: 8px 0;
}

.mobile-menu-btn-group {
  width: 100%;
  padding: 10px 24px;
}

/* 动画样式 */
.mobile-menu-fade-enter-active,
.mobile-menu-fade-leave-active {
  transition:
    opacity 0.25s,
    transform 0.25s;
}

.mobile-menu-fade-enter-from,
.mobile-menu-fade-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}

.mobile-menu-fade-enter-to,
.mobile-menu-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* 响应式：小于720px时调整布局 */
@media (max-width: 720px) {
  .header-menu {
    display: none;
  }

  .menu-toggle {
    display: flex;
  }

  .header-left {
    margin-right: 0;
  }

  .header-right {
    margin-left: auto;
  }

  .desktop-only {
    display: none;
  }
}
</style>
