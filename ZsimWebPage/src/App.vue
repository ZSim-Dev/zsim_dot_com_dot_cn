<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const menuOpen = ref(false)

const menuItems = [
  { label: '主页', action: () => goHome() },
  { label: '下载', action: () => goTo('/download') },
  { label: '文档', action: () => goTo('/docs') },
  { label: '投票', action: () => goTo('/vote') }
]

function goHome() {
  router.push({ name: 'Home' })
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

// 登录状态管理
const user = ref<string | null>(null)
const token = ref<string | null>(null)

function logout() {
  user.value = null
  token.value = null
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  window.location.reload()
}

async function fetchUser() {
  if (!token.value) return
  const res = await fetch(`/api/me`, {
    headers: { Authorization: `Bearer ${token.value}` }
  })
  if (res.ok) {
    const data = await res.json()
    user.value = data.username
    localStorage.setItem('user', user.value)
  } else {
    user.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    token.value = null
  }
}

onMounted(() => {
  const t = localStorage.getItem('token')
  if (t) {
    token.value = t
    fetchUser()
  }
})
</script>

<template>
  <header class="zsim-header fixed-header">
    <!-- 汉堡菜单按钮，仅在小屏显示 -->
    <button class="menu-toggle" @click.stop="menuOpen = !menuOpen" aria-label="展开菜单">
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </button>
    <div class="header-left" @click="goHome" style="cursor:pointer;">
      <img src="./assets/logo.svg" alt="logo" class="logo" />
      <span class="zsim-title">ZSim 模拟器</span>
    </div>
    <!-- 普通菜单，大屏显示 -->
    <nav class="header-menu">
      <button v-for="item in menuItems" :key="item.label" class="menu-btn" @click="item.action">{{ item.label
        }}</button>
    </nav>
    <div class="header-right">
      <button class="github-btn" @click="goTo('https://github.com/your-repo')">
        <svg t="1717920000000" class="github-icon" viewBox="0 0 1024 1024" width="24" height="24">
          <path
            d="M511.6 76.3C264.6 76.3 64 277.5 64 525.2c0 198.1 128.5 366.2 306.7 425.8 22.4 4.1 30.6-9.7 30.6-21.5 0-10.6-0.4-45.5-0.6-82.5-124.8 27.1-151.2-60.2-151.2-60.2-20.4-51.8-49.8-65.6-49.8-65.6-40.7-27.8 3.1-27.2 3.1-27.2 45 3.2 68.7 46.2 68.7 46.2 40 68.6 104.9 48.8 130.5 37.3 4.1-29 15.7-48.8 28.6-60-99.7-11.3-204.5-49.8-204.5-221.8 0-49 17.5-89 46.2-120.4-4.6-11.3-20-56.8 4.4-118.5 0 0 37.6-12.1 123.2 46.1 35.7-9.9 74-14.8 112.1-15 38 0.2 76.4 5.1 112.1 15 85.5-58.2 123.1-46.1 123.1-46.1 24.5 61.7 9.1 107.2 4.5 118.5 28.8 31.4 46.1 71.4 46.1 120.4 0 172.4-104.9 210.4-204.9 221.5 16.1 13.9 30.4 41.3 30.4 83.3 0 60.2-0.5 108.7-0.5 123.5 0 11.9 8 25.8 30.7 21.4C831.6 891.2 960 723.2 960 525.2c0-247.7-200.6-448.9-448.4-448.9z"
            fill="#181616" />
        </svg>
      </button>
      <template v-if="user">
        <span class="user-info">你好，{{ user }}</span>
        <button class="login-btn" @click="logout">登出</button>
      </template>
      <template v-else>
        <button class="login-btn" @click="router.push('/login')">登录</button>
      </template>
    </div>
    <!-- 弹出菜单，小屏显示 -->
    <transition name="mobile-menu-fade">
      <div v-if="menuOpen" class="mobile-menu" @click.self="menuOpen = false">
        <button v-for="item in menuItems" :key="item.label" class="menu-btn" @click="item.action">{{ item.label
          }}</button>
      </div>
    </transition>
  </header>
  <div class="main-content">
    <transition name="fade-page" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<style scoped>
.zsim-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 56px;
  padding: 0 16px;
  background: #fff;
  border-bottom: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  position: relative;
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
  color: #222;
  letter-spacing: 1px;
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
  color: #333;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 4px;
  transition: background 0.2s;
}

.menu-btn+.menu-btn {
  margin-left: 8px;
}

.menu-btn:hover {
  background: #f5f5f5;
}

.header-right {
  display: flex;
  align-items: center;
  margin-left: auto;
  gap: 8px;
}

.user-info {
  margin: 0 8px;
  color: #333;
  font-size: 15px;
}

.login-btn {
  background: #2c3e50;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 16px;
  margin-left: 4px;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.2s;
}

.login-btn.cancel {
  background: #aaa;
  color: #fff;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-btn:hover:not(:disabled) {
  background: #1a2533;
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
  background: #333;
  margin: 3px 0;
  border-radius: 2px;
  transition: all 0.2s;
}

/* 移动端弹出菜单 */
.mobile-menu {
  position: absolute;
  top: 56px;
  left: 0;
  width: 100vw;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 12px 0;
  z-index: 120;
}

.mobile-menu .menu-btn {
  width: 100%;
  text-align: left;
  padding: 10px 24px;
  font-size: 18px;
  border-radius: 0;
  margin: 0;
}

/* 动画样式 */
.mobile-menu-fade-enter-active,
.mobile-menu-fade-leave-active {
  transition: opacity 0.25s, transform 0.25s;
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

.fade-page-enter-active,
.fade-page-leave-active {
  transition: opacity 0.4s cubic-bezier(.4, 0, .2, 1), transform 0.4s cubic-bezier(.4, 0, .2, 1);
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
}
</style>
