<template>
  <div class="user-auth">
    <!-- 桌面端用户认证 -->
    <div class="desktop-auth desktop-only">
      <template v-if="user">
        <span class="user-info">{{ t('message.hello') }}，{{ user }}</span>
        <button class="login-btn" @click="logout">{{ t('message.logout') }}</button>
      </template>
      <template v-else>
        <button class="login-btn" @click="goToLogin">{{ t('message.login') }}</button>
      </template>
    </div>
    
    <!-- 移动端用户认证 -->
    <div class="mobile-auth" v-if="showMobileAuth">
      <template v-if="user">
        <div class="mobile-user-info">{{ t('message.hello') }}，{{ user }}</div>
        <button class="menu-btn mobile-logout-btn" @click="logout">
          {{ t('message.logout') }}
        </button>
      </template>
      <template v-else>
        <button class="menu-btn mobile-login-btn" @click="goToLogin">
          {{ t('message.login') }}
        </button>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

interface Props {
  showMobileAuth?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showMobileAuth: false
})

const emit = defineEmits<{
  closeMenu: []
}>()

const { t } = useI18n()
const router = useRouter()

// 用户状态管理
const user = ref<string | null>(null)
const token = ref<string | null>(null)

function logout() {
  user.value = null
  token.value = null
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  emit('closeMenu')
  window.location.reload()
}

function goToLogin() {
  router.push('/login')
  emit('closeMenu')
}

async function fetchUser() {
  if (!token.value) return
  try {
    const res = await fetch(`/api/me`, {
      headers: { Authorization: `Bearer ${token.value}` },
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
  } catch (error) {
    console.error('Failed to fetch user:', error)
    user.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    token.value = null
  }
}

// 初始化
onMounted(() => {
  const storedToken = localStorage.getItem('token')
  if (storedToken) {
    token.value = storedToken
    fetchUser()
  }
})

// 暴露用户状态给父组件使用
defineExpose({
  user,
  token,
  logout,
  fetchUser
})
</script>

<style scoped>
.user-auth {
  display: contents;
}

.desktop-auth {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-info {
  margin: 0 8px;
  color: var(--text-secondary);
  font-size: 15px;
  transition: color 0.3s ease;
}

.login-btn {
  background: var(--button-bg);
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 16px;
  margin-left: 4px;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.3s ease;
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
  background: var(--button-hover);
}

.mobile-auth {
  width: 100%;
}

.mobile-user-info {
  width: 100%;
  text-align: left;
  padding: 10px 24px;
  font-size: 16px;
  color: var(--text-secondary);
}

.mobile-login-btn,
.mobile-logout-btn {
  width: 100%;
  text-align: left;
  padding: 10px 24px;
  font-size: 16px;
  border-radius: 0;
  margin: 0;
  background: var(--button-bg);
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}

.mobile-login-btn:hover,
.mobile-logout-btn:hover {
  background: var(--button-hover);
}

/* 响应式样式 */
@media (max-width: 720px) {
  .desktop-only {
    display: none;
  }
}
</style>
