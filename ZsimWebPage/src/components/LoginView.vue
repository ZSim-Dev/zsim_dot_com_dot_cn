<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const loginError = ref('')
const registerError = ref('')
const mode = ref<'login' | 'register'>('login')

async function handleLogin() {
  loading.value = true
  loginError.value = ''
  try {
    const res = await fetch(`/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        username: username.value,
        password: password.value,
      }),
    })
    const data = await res.json()
    if (!res.ok) {
      loginError.value = data.detail || '登录失败'
      loading.value = false
      return
    }
    localStorage.setItem('token', data.access_token)
    // 获取用户信息
    const meRes = await fetch(`/api/me`, {
      headers: { Authorization: `Bearer ${data.access_token}` }
    })
    if (meRes.ok) {
      const meData = await meRes.json()
      localStorage.setItem('user', meData.username)
    }
    window.location.replace('/') // 登录成功后刷新首页
  } catch (e) {
    loginError.value = '网络连接断开或服务离线'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  loading.value = true
  registerError.value = ''
  try {
    const res = await fetch(`/api/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })
    const data = await res.json()
    if (!res.ok) {
      registerError.value = data.detail || '注册失败'
      loading.value = false
      return
    }
    // 注册成功后自动登录
    await handleLogin()
  } catch (e) {
    registerError.value = '网络错误'
  } finally {
    loading.value = false
  }
}

function switchMode() {
  mode.value = mode.value === 'login' ? 'register' : 'login'
  loginError.value = ''
  registerError.value = ''
}
</script>

<template>
  <div class="login-page">
    <transition name="fade-login">
      <div class="login-box">
        <h2>{{ mode === 'login' ? '用户登录' : '用户注册' }}</h2>
        <input v-model="username" class="login-input" type="text" placeholder="用户名" autocomplete="username" />
        <input v-model="password" class="login-input" type="password" placeholder="密码" autocomplete="current-password"
          @keyup.enter="mode === 'login' ? handleLogin() : handleRegister()" />
        <button class="login-btn" :disabled="loading" @click="mode === 'login' ? handleLogin() : handleRegister()">
          {{ loading ? (mode === 'login' ? '登录中...' : '注册中...') : (mode === 'login' ? '登录' : '注册') }}
        </button>
        <button class="switch-btn" @click="switchMode" :disabled="loading">
          {{ mode === 'login' ? '没有账号？注册' : '已有账号？登录' }}
        </button>
        <div v-if="mode === 'login' && loginError" class="login-error">{{ loginError }}</div>
        <div v-if="mode === 'register' && registerError" class="login-error">{{ registerError }}</div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  background: #fff;
  border-radius: 8px;
  padding: 32px 24px 24px 24px;
  min-width: 280px;
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.login-box h2 {
  margin-bottom: 18px;
  text-align: center;
  color: #222;
}

.login-input {
  margin-bottom: 12px;
  padding: 8px 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  transition: border 0.2s;
}

.login-input:focus {
  border: 1.5px solid #2c3e50;
}

.login-btn {
  background: #2c3e50;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 0;
  cursor: pointer;
  font-size: 16px;
  margin-top: 8px;
  transition: background 0.2s;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-btn:hover:not(:disabled) {
  background: #1a2533;
}

.switch-btn {
  background: none;
  border: none;
  color: #2c3e50;
  margin-top: 8px;
  cursor: pointer;
  font-size: 15px;
  text-decoration: underline;
  transition: color 0.2s;
}

.switch-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.switch-btn:hover:not(:disabled) {
  color: #1a2533;
}

.login-error {
  color: #d32f2f;
  margin-top: 10px;
  text-align: center;
  font-size: 14px;
}

.fade-login-enter-active,
.fade-login-leave-active {
  transition: opacity 0.4s, transform 0.4s;
}

.fade-login-enter-from,
.fade-login-leave-to {
  opacity: 0;
  transform: translateY(24px);
}

.fade-login-enter-to,
.fade-login-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
