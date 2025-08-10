<script setup lang="ts">
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useI18n } from 'vue-i18n'

  const { t } = useI18n()
  const router = useRouter()
  const username = ref('')
  const password = ref('')
  const confirmPassword = ref('')
  const email = ref('')
  const verificationCode = ref('')
  const loading = ref(false)
  const sendingCode = ref(false)
  const countdown = ref(0)
  const loginError = ref('')
  const registerError = ref('')
  const mode = ref<'login' | 'register' | 'email'>('login')

  // 计算倒计时显示文本
  const codeButtonText = computed(() => {
    if (sendingCode.value) return t('login.sending')
    if (countdown.value > 0) return t('login.resend', { count: countdown.value })
    return t('login.get_code')
  })

  // 验证邮箱格式
  const isValidEmail = computed(() => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)
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
        loginError.value = data.detail || t('login.login_failed')
        loading.value = false
        return
      }
      localStorage.setItem('token', data.access_token)
      // 获取用户信息
      const meRes = await fetch(`/api/me`, {
        headers: { Authorization: `Bearer ${data.access_token}` },
      })
      if (meRes.ok) {
        const meData = await meRes.json()
        localStorage.setItem('user', meData.username)
      }
      window.location.replace('/') // 登录成功后刷新首页
    } catch (e) {
      loginError.value = t('login.network_error')
    } finally {
      loading.value = false
    }
  }

  async function handleRegister() {
    if (
      !username.value ||
      !password.value ||
      !confirmPassword.value ||
      !email.value ||
      !verificationCode.value
    ) {
      registerError.value = t('login.fill_all_fields')
      return
    }

    if (password.value !== confirmPassword.value) {
      registerError.value = t('login.password_mismatch')
      return
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      registerError.value = t('login.invalid_email')
      return
    }

    if (!/^\d{6}$/.test(verificationCode.value)) {
      registerError.value = t('login.invalid_code')
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
          email: email.value,
          code: verificationCode.value,
        }),
      })
      const data = await res.json()
      if (!res.ok) {
        registerError.value = data.detail || t('login.register_failed')
        loading.value = false
        return
      }
      // 注册成功后自动登录
      await handleLogin()
    } catch (e) {
      registerError.value = t('login.network_error_simple')
    } finally {
      loading.value = false
    }
  }

  // 发送验证码
  async function sendVerificationCode(purpose: 'login' | 'register') {
    if (!isValidEmail.value) {
      const errorMsg = t('login.invalid_email')
      if (purpose === 'register') {
        registerError.value = errorMsg
      } else {
        loginError.value = errorMsg
      }
      return
    }

    sendingCode.value = true
    registerError.value = ''
    loginError.value = ''

    try {
      const res = await fetch('/api/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.value, purpose }),
      })

      const data = await res.json()
      if (!res.ok) {
        const errorMsg = data.detail || t('login.code_send_failed')
        if (purpose === 'register') {
          registerError.value = errorMsg
        } else {
          loginError.value = errorMsg
        }
        return
      }

      startCountdown()
    } catch (e) {
      const errorMsg = t('login.network_error')
      if (purpose === 'register') {
        registerError.value = errorMsg
      } else {
        loginError.value = errorMsg
      }
    } finally {
      sendingCode.value = false
    }
  }

  // 邮箱验证码登录
  async function handleEmailLogin() {
    if (!isValidEmail.value) {
      loginError.value = t('login.invalid_email')
      return
    }

    if (!verificationCode.value) {
      loginError.value = t('login.invalid_code')
      return
    }

    loading.value = true
    loginError.value = ''

    try {
      const res = await fetch('/api/login-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email.value,
          code: verificationCode.value,
        }),
      })

      const data = await res.json()
      if (!res.ok) {
        loginError.value = data.detail || t('login.login_failed')
        return
      }

      localStorage.setItem('token', data.access_token)
      // 获取用户信息
      const meRes = await fetch('/api/me', {
        headers: { Authorization: `Bearer ${data.access_token}` },
      })
      if (meRes.ok) {
        const meData = await meRes.json()
        localStorage.setItem('user', meData.username)
      }
      window.location.replace('/') // 登录成功后刷新首页
    } catch (e) {
      loginError.value = t('login.network_error')
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
    email.value = ''
    verificationCode.value = ''
    countdown.value = 0
  }

  // Login mode switch handlers
  function switchToLoginMode() {
    mode.value = 'login'
    loginError.value = ''
    username.value = ''
    password.value = ''
  }

  function switchToEmailMode() {
    mode.value = 'email'
    loginError.value = ''
    email.value = ''
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
            {{
              mode === 'login'
                ? t('login.account_login')
                : mode === 'email'
                  ? t('login.email_login')
                  : t('login.create_account')
            }}
          </h1>
          <p class="login-subtitle">
            {{
              mode === 'login'
                ? t('login.account_login_subtitle')
                : mode === 'email'
                  ? t('login.email_login_subtitle')
                  : t('login.create_account_subtitle')
            }}
          </p>
        </div>

        <!-- 用户名密码登录 -->
        <div v-if="mode === 'login'" class="form-container">
          <div class="input-group">
            <input
              v-model="username"
              class="apple-input"
              type="text"
              :placeholder="t('login.username')"
              autocomplete="username"
            />
          </div>
          <div class="input-group">
            <input
              v-model="password"
              class="apple-input"
              type="password"
              :placeholder="t('login.password')"
              autocomplete="current-password"
              @keyup.enter="handleLogin"
            />
          </div>
          <button class="apple-btn primary" :disabled="loading" @click="handleLogin">
            {{ loading ? t('login.logging_in') : t('login.login_button') }}
          </button>
        </div>

        <!-- 邮箱验证码登录 -->
        <div v-if="mode === 'email'" class="form-container">
          <div class="input-group">
            <input
              v-model="email"
              class="apple-input"
              type="email"
              :placeholder="t('login.email')"
            />
          </div>
          <div class="input-group code-group">
            <input
              v-model="verificationCode"
              class="apple-input code-input"
              type="text"
              :placeholder="t('login.verification_code')"
              maxlength="6"
              @keyup.enter="handleEmailLogin"
            />
            <button
              class="code-btn"
              :disabled="!isValidEmail || sendingCode || countdown > 0"
              @click="sendVerificationCode('login')"
            >
              {{ codeButtonText }}
            </button>
          </div>
          <button class="apple-btn primary" :disabled="loading" @click="handleEmailLogin">
            {{ loading ? t('login.logging_in') : t('login.login_button') }}
          </button>
        </div>

        <!-- 注册 -->
        <div v-if="mode === 'register'" class="form-container">
          <div class="input-group">
            <input
              v-model="username"
              class="apple-input"
              type="text"
              :placeholder="t('login.username')"
              autocomplete="username"
            />
          </div>
          <div class="input-group">
            <input
              v-model="password"
              class="apple-input"
              type="password"
              :placeholder="t('login.password')"
              autocomplete="new-password"
            />
          </div>
          <div class="input-group">
            <input
              v-model="confirmPassword"
              class="apple-input"
              type="password"
              :placeholder="t('login.confirm_password')"
              autocomplete="new-password"
            />
          </div>
          <div class="input-group">
            <input
              v-model="email"
              class="apple-input"
              type="email"
              :placeholder="t('login.email')"
            />
          </div>
          <div class="input-group code-group">
            <input
              v-model="verificationCode"
              class="apple-input code-input"
              type="text"
              :placeholder="t('login.verification_code')"
              maxlength="6"
              @keyup.enter="handleRegister"
            />
            <button
              class="code-btn"
              :disabled="!isValidEmail || countdown > 0 || loading"
              @click="sendVerificationCode('register')"
            >
              {{ codeButtonText }}
            </button>
          </div>
          <button class="apple-btn primary" :disabled="loading" @click="handleRegister">
            {{ loading ? t('login.registering') : t('login.register_button') }}
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
          <button :class="['mode-btn', { active: mode === 'login' }]" @click="switchToLoginMode">
            {{ t('login.account_login') }}
          </button>
          <button :class="['mode-btn', { active: mode === 'email' }]" @click="switchToEmailMode">
            {{ t('login.email_login') }}
          </button>
        </div>

        <!-- 切换到注册/登录 -->
        <div class="switch-container">
          <button class="switch-btn" @click="switchMode" :disabled="loading">
            {{ mode === 'register' ? t('login.back_to_login') : t('login.register_account') }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
  .login-page {
    min-height: 70vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: transparent;
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
    color: var(--apple-text);
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
    color: var(--apple-text);
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
    background: rgba(255, 59, 48, 0.15);
    color: var(--apple-red);
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    text-align: center;
    margin-top: 16px;
    border: 1px solid rgba(255, 59, 48, 0.3);
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
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
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
    .login-page {
      background: transparent;
    }
  }
</style>
