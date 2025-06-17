<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push({ name: 'Home' })
}

function goTo(url: string) {
  if (url.startsWith('http')) {
    window.open(url, '_blank')
  } else {
    router.push(url)
  }
}
</script>

<template>
  <header class="zsim-header fixed-header">
    <div class="header-left" @click="goHome" style="cursor:pointer;">
      <img src="./assets/logo.svg" alt="logo" class="logo" />
      <span class="zsim-title">Zsim</span>
    </div>
    <nav class="header-menu">
      <button @click="goHome" class="menu-btn">主页</button>
      <button @click="goTo('/download')" class="menu-btn">下载</button>
      <button @click="goTo('/docs')" class="menu-btn">文档</button>
    </nav>
    <div class="header-right">
      <button class="github-btn" @click="goTo('https://github.com/your-repo')">
        <svg t="1717920000000" class="github-icon" viewBox="0 0 1024 1024" width="24" height="24">
          <path d="M511.6 76.3C264.6 76.3 64 277.5 64 525.2c0 198.1 128.5 366.2 306.7 425.8 22.4 4.1 30.6-9.7 30.6-21.5 0-10.6-0.4-45.5-0.6-82.5-124.8 27.1-151.2-60.2-151.2-60.2-20.4-51.8-49.8-65.6-49.8-65.6-40.7-27.8 3.1-27.2 3.1-27.2 45 3.2 68.7 46.2 68.7 46.2 40 68.6 104.9 48.8 130.5 37.3 4.1-29 15.7-48.8 28.6-60-99.7-11.3-204.5-49.8-204.5-221.8 0-49 17.5-89 46.2-120.4-4.6-11.3-20-56.8 4.4-118.5 0 0 37.6-12.1 123.2 46.1 35.7-9.9 74-14.8 112.1-15 38 0.2 76.4 5.1 112.1 15 85.5-58.2 123.1-46.1 123.1-46.1 24.5 61.7 9.1 107.2 4.5 118.5 28.8 31.4 46.1 71.4 46.1 120.4 0 172.4-104.9 210.4-204.9 221.5 16.1 13.9 30.4 41.3 30.4 83.3 0 60.2-0.5 108.7-0.5 123.5 0 11.9 8 25.8 30.7 21.4C831.6 891.2 960 723.2 960 525.2c0-247.7-200.6-448.9-448.4-448.9z" fill="#181616"/>
        </svg>
      </button>
    </div>
  </header>
  <div class="main-content">
    <router-view />
  </div>
</template>

<style scoped>
.zsim-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 32px;
  background: #fff;
  border-bottom: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  z-index: 100;
}
.main-content {
  padding-top: 56px;
}
.header-left {
  display: flex;
  align-items: center;
  margin-right: 0;
}
.logo {
  width: 32px;
  height: 32px;
  margin-right: 10px;
}
.zsim-title {
  font-size: 22px;
  font-weight: bold;
  color: #222;
  letter-spacing: 1px;
}
.header-menu {
  display: flex;
  margin-left: 0;
  gap: 0;
}
.menu-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #333;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 4px;
  transition: background 0.2s;
}
.menu-btn + .menu-btn {
  margin-left: 8px;
}
.menu-btn:hover {
  background: #f5f5f5;
}
.header-right {
  display: flex;
  align-items: center;
}
.github-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: background 0.2s;
}
.github-btn:hover {
  background: #f5f5f5;
}
.github-icon {
  display: block;
}
</style>
