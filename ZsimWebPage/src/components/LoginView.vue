<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const phone = ref('')
const verificationCode = ref('')
const loading = ref(false)
const sendingCode = ref(false)
const countdown = ref(0)
const loginError = ref('')
const registerError = ref('')
const mode = ref<'login' | 'register' | 'phone'>('login')

// 计算倒计时显示文本
const codeButtonText = computed(() => {
  if (sendingCode.value) return '发送中...'
  if (countdown.value > 0) return `${countdown.value}s后重发`
  return '获取验证码'
})

// 验证手机号格式
const isValidPhone = computed(() => {
  return /^1[3-9]\d{9}$/.test(phone.value)
})

// 倒计时功能
function startCountdown() {
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

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
  if (!username.value || !password.value || !confirmPassword.value || !phone.value || !verificationCode.value) {
    registerError.value = '请填写所有必填字段'
    return
  }

  if (password.value !== confirmPassword.value) {
    registerError.value = '密码和确认密码不匹配'
    return
  }

  if (!/^1[3-9]\d{9}$/.test(phone.value)) {
    registerError.value = '请输入正确的手机号'
    return
  }

  if (!/^\d{6}$/.test(verificationCode.value)) {
    registerError.value = '请输入6位数字验证码'
    return
  }

  loading.value = true
  registerError.value = ''
  try {
    const res = await fetch(`/api/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        confirm_password: confirmPassword.value,
        phone: phone.value,
        code: verificationCode.value
      }),
    })
    const data = await res.json()
    if (!res.ok) {
      registerError.value = data.detail || '注册失败'
      loading.value = false
      return
    }
    // 注册成功后切换到登录模式
    mode.value = 'login'
    // 清空表单
    username.value = ''
    password.value = ''
    confirmPassword.value = ''
    phone.value = ''
    verificationCode.value = ''
    countdown.value = 0
  } catch (e) {
    registerError.value = '网络错误'
  } finally {
    loading.value = false
  }
}

// 发送验证码
async function sendVerificationCode() {
  if (!isValidPhone.value) {
    loginError.value = '请输入正确的手机号'
    return
  }

  sendingCode.value = true
  loginError.value = ''

  try {
    const res = await fetch('/api/send-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: phone.value })
    })

    const data = await res.json()
    if (!res.ok) {
      loginError.value = data.detail || '验证码发送失败'
      return
    }

    startCountdown()
    loginError.value = ''
  } catch (e) {
    loginError.value = '网络连接断开或服务离线'
  } finally {
    sendingCode.value = false
  }
}

// 手机号验证码登录
async function handlePhoneLogin() {
  if (!isValidPhone.value) {
    loginError.value = '请输入正确的手机号'
    return
  }

  if (!verificationCode.value) {
    loginError.value = '请输入验证码'
    return
  }

  loading.value = true
  loginError.value = ''

  try {
    const res = await fetch('/api/login-phone', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: phone.value,
        code: verificationCode.value
      })
    })

    const data = await res.json()
    if (!res.ok) {
      loginError.value = data.detail || '登录失败'
      return
    }

    localStorage.setItem('token', data.access_token)
    // 获取用户信息
    const meRes = await fetch('/api/me', {
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

function switchMode() {
  if (mode.value === 'register') {
    mode.value = 'login'
  } else {
    mode.value = 'register'
  }

  // 清空错误信息和表单
  loginError.value = ''
  registerError.value = ''
  username.value = ''
  password.value = ''
  confirmPassword.value = ''
  phone.value = ''
  verificationCode.value = ''
  countdown.value = 0
}
</script>

<template>
  <div class="login-page">
    <transition name="fade-login">
      <div class="login-box">
        <!-- 标题 -->
        <div class="login-header">
          <h1 class="login-title">
            {{ mode === 'login' ? '账号登录' : mode === 'phone' ? '手机登录' : '创建账号' }}
          </h1>
          <p class="login-subtitle">
            {{ mode === 'login' ? '使用用户名和密码登录' : mode === 'phone' ? '使用手机号和验证码登录' : '创建新的账号' }}
          </p>
        </div>

        <!-- 用户名密码登录 -->
        <div v-if="mode === 'login'" class="form-container">
          <div class="input-group">
            <input v-model="username" class="apple-input" type="text" placeholder="用户名" autocomplete="username" />
          </div>
          <div class="input-group">
            <input v-model="password" class="apple-input" type="password" placeholder="密码"
              autocomplete="current-password" @keyup.enter="handleLogin" />
          </div>
          <button class="apple-btn primary" :disabled="loading" @click="handleLogin">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>

        <!-- 手机号验证码登录 -->
        <div v-if="mode === 'phone'" class="form-container">
          <div class="input-group">
            <input v-model="phone" class="apple-input" type="tel" placeholder="手机号" maxlength="11" />
          </div>
          <div class="input-group code-group">
            <input v-model="verificationCode" class="apple-input code-input" type="text" placeholder="验证码" maxlength="6"
              @keyup.enter="handlePhoneLogin" />
            <button class="code-btn" :disabled="!isValidPhone || sendingCode || countdown > 0"
              @click="sendVerificationCode">
              {{ codeButtonText }}
            </button>
          </div>
          <button class="apple-btn primary" :disabled="loading" @click="handlePhoneLogin">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>

        <!-- 注册 -->
        <div v-if="mode === 'register'" class="form-container">
          <div class="input-group">
            <input v-model="username" class="apple-input" type="text" placeholder="用户名" autocomplete="username" />
          </div>
          <div class="input-group">
            <input v-model="password" class="apple-input" type="password" placeholder="密码"
              autocomplete="new-password" />
          </div>
          <div class="input-group">
            <input v-model="confirmPassword" class="apple-input" type="password" placeholder="确认密码"
              autocomplete="new-password" />
          </div>
          <div class="input-group">
            <input v-model="phone" class="apple-input" type="tel" placeholder="手机号" maxlength="11" />
          </div>
          <div class="input-group code-group">
            <input v-model="verificationCode" class="apple-input code-input" type="text" placeholder="验证码" maxlength="6"
              @keyup.enter="handleRegister" />
            <button class="code-btn" :disabled="!isValidPhone || countdown > 0 || loading"
              @click="sendVerificationCode">
              {{ codeButtonText }}
            </button>
          </div>
          <button class="apple-btn primary" :disabled="loading" @click="handleRegister">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>

        <!-- 错误信息 -->
        <div v-if="loginError" class="error-message">
          {{ loginError }}
        </div>
        <div v-if="registerError" class="error-message">
          {{ registerError }}
        </div>

        <!-- 登录模式切换 -->
        <div v-if="mode !== 'register'" class="login-mode-switch">
          <button :class="['mode-btn', { active: mode === 'login' }]"
            @click="mode = 'login'; loginError = ''; username = ''; password = ''">
            账号登录
          </button>
          <button :class="['mode-btn', { active: mode === 'phone' }]"
            @click="mode = 'phone'; loginError = ''; phone = ''; verificationCode = ''; countdown = 0">
            手机登录
          </button>
        </div>

        <!-- 切换到注册/登录 -->
        <div class="switch-container">
          <button class="switch-btn" @click="switchMode" :disabled="loading">
            {{ mode === 'register' ? '返回登录' : '注册账号' }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* Apple Design System Colors */
:root {
  --apple-blue: #007AFF;
  --apple-blue-hover: #0056CC;
  --apple-gray: #8E8E93;
  --apple-gray-light: #F2F2F7;
  --apple-gray-dark: #1C1C1E;
  --apple-red: #FF3B30;
  --apple-green: #34C759;
  --apple-background: #FFFFFF;
  --apple-surface: #F9F9F9;
  --apple-border: #D1D1D6;
  --apple-text: #000000;
  --apple-text-secondary: #6D6D70;
  --apple-input-bg: #FFFFFF;
  --apple-input-focus-bg: #FFFFFF;
  --apple-input-border: #C7C7CC;
  --apple-input-border-focus: #007AFF;
}

.login-page {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.login-box {
  background: var(--apple-background);
  border-radius: 20px;
  padding: 40px 32px;
  min-width: 360px;
  max-width: 400px;
  width: 100%;
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.1),
    0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* 标题区域 */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--apple-text);
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.login-subtitle {
  font-size: 16px;
  color: var(--apple-text-secondary);
  margin: 0;
  font-weight: 400;
}

/* 表单容器 */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 输入框组 */
.input-group {
  position: relative;
}

.apple-input {
  width: 100%;
  padding: 16px 20px;
  font-size: 16px;
  border: 1.5px solid var(--apple-input-border);
  border-radius: 12px;
  outline: none;
  background: var(--apple-input-bg);
  color: var(--apple-text);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.apple-input:focus {
  border-color: var(--apple-input-border-focus);
  background: var(--apple-input-focus-bg);
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
  transform: translateY(-1px);
}

.apple-input::placeholder {
  color: var(--apple-gray);
  font-weight: 400;
}

/* 验证码输入组 */
.code-group {
  display: flex;
  gap: 12px;
  align-items: stretch;
}

.code-input {
  flex: 1;
}

.code-btn {
  padding: 16px 20px;
  background: var(--apple-gray-light);
  border: 1.5px solid var(--apple-input-border);
  border-radius: 12px;
  color: var(--apple-blue);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  white-space: nowrap;
  min-width: 100px;
}

.code-btn:hover:not(:disabled) {
  background: var(--apple-blue);
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.code-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Apple 按钮 */
.apple-btn {
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.apple-btn.primary {
  background: var(--apple-blue);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.apple-btn.primary:hover:not(:disabled) {
  background: var(--apple-blue-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 122, 255, 0.4);
}

.apple-btn.primary:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3);
}

.apple-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* 错误信息 */
.error-message {
  background: rgba(255, 59, 48, 0.1);
  color: var(--apple-red);
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
  margin-top: 16px;
  border: 1px solid rgba(255, 59, 48, 0.2);
}

/* 登录模式切换 */
.login-mode-switch {
  display: flex;
  background: var(--apple-gray-light);
  border-radius: 12px;
  padding: 4px;
  margin-top: 24px;
  margin-bottom: 24px;
  gap: 4px;
}

.login-mode-switch .mode-btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--apple-text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.login-mode-switch .mode-btn.active {
  background: var(--apple-background);
  color: var(--apple-text);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 注册标题 */
.register-title {
  text-align: center;
  margin-bottom: 24px;
}

.register-title h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: var(--apple-text);
}

/* 切换按钮容器 */
.switch-container {
  margin-top: 24px;
  text-align: center;
}

.switch-btn {
  background: none;
  border: none;
  color: var(--apple-blue);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  padding: 12px 16px;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.switch-btn:hover:not(:disabled) {
  background: rgba(0, 122, 255, 0.1);
  transform: translateY(-1px);
}

.switch-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* 动画效果 */
.fade-login-enter-active,
.fade-login-leave-active {
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.fade-login-enter-from,
.fade-login-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}

.fade-login-enter-to,
.fade-login-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-page {
    padding: 16px;
  }

  .login-box {
    min-width: unset;
    padding: 32px 24px;
    border-radius: 16px;
  }

  .login-title {
    font-size: 24px;
  }

  .code-group {
    flex-direction: column;
    gap: 12px;
  }

  .code-btn {
    min-width: unset;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  :root {
    --apple-background: #1C1C1E;
    --apple-surface: #2C2C2E;
    --apple-border: #48484A;
    --apple-text: #FFFFFF;
    --apple-text-secondary: #98989D;
    --apple-gray-light: #2C2C2E;
    --apple-input-bg: #2C2C2E;
    --apple-input-focus-bg: #3A3A3C;
    --apple-input-border: #5A5A5E;
    --apple-input-border-focus: #007AFF;
  }

  .login-page {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  }
}
</style>
