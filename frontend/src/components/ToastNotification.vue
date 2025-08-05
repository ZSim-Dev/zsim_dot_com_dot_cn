<template>
  <Teleport to="body">
    <Transition name="toast-transition">
      <div v-if="show" class="toast-overlay" @click="close">
        <div class="toast-content" @click.stop>
          <div class="toast-message">{{ message }}</div>
          <button class="toast-button" @click="close">{{ t('common.ok') }}</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const show = ref(false)
const message = ref('')
let timer: ReturnType<typeof setTimeout> | null = null

// 监听 show 变化，3秒后自动关闭
watch(show, (newShow) => {
  if (newShow) {
    // 清除之前的定时器
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
    // 设置新的定时器
    timer = setTimeout(() => {
      close()
      timer = null
    }, 3000)
  }
})

const close = () => {
  show.value = false
}

const showToast = (msg: string) => {
  message.value = msg
  show.value = true
}

// 监听 show 变化，3秒后自动关闭
watch(show, (newShow) => {
  if (newShow) {
    setTimeout(() => {
      close()
    }, 3000)
  }
})

defineExpose({
  showToast,
  close
})
</script>

<style scoped>
.toast-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.toast-content {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.toast-message {
  font-size: 1rem;
  color: var(--color-text);
  margin-bottom: 1rem;
  line-height: 1.5;
}

.toast-button {
  background-color: var(--vt-c-indigo);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.toast-button:hover {
  background-color: #3c4a5c;
}

.toast-button:active {
  transform: scale(0.95);
}

/* 过渡动画 */
.toast-transition-enter-active,
.toast-transition-leave-active {
  transition: opacity 0.3s ease;
}

.toast-transition-enter-from,
.toast-transition-leave-to {
  opacity: 0;
}

.toast-transition-enter-to,
.toast-transition-leave-from {
  opacity: 1;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .toast-content {
    margin: 0 1rem;
    padding: 1.25rem;
  }
  
  .toast-message {
    font-size: 0.95rem;
  }
  
  .toast-button {
    padding: 0.625rem 1.5rem;
    font-size: 0.95rem;
  }
}
</style>