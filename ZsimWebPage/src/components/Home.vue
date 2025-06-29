<script setup lang="ts">
const download_link: string = 'https://github.com/zhiqiang0/ZSimulator/releases';

function handleDownload() {
  window.open(download_link, '_blank');
}
</script>

<template>
  <div class="homepage">
    <div class="header">
      <div class="logo"></div>
      <p class="title">ZSim 模拟器</p>
      <p class="description">ZSim 是一个独立的绝区零自动模拟器，我们实现了模拟绝区零的战斗，并支持全脚本化的出招。</p>
    </div>

    <div class="main-content">
      <button class="download-btn" @click="handleDownload">下载桌面版</button>
      <div class="links">
        <router-link to="/docs" class="link-item">使用文档</router-link>
        <a href="/vote" class="link-item">功能投票</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.homepage {
  padding: 0 2rem;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  animation: fadeInPage 0.5s ease-in-out;
  /* 添加垂直居中布局 */
  min-height: calc(100vh - 120px); /* 减去header高度 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

@keyframes fadeInPage {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.main-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.logo {
  width: 120px;
  height: 120px;
  background: #f0f0f0;
  border-radius: 24px;
  margin: 0 auto 1rem;
  animation: pulseLogo 2s infinite ease-in-out alternate;
}

@keyframes pulseLogo {
  from {
    transform: scale(1);
  }

  to {
    transform: scale(1.05);
  }
}

.download-btn {
  padding: 12px 60px;
  font-size: 1.2rem;
  background: var(--vt-c-indigo);
  color: whitesmoke;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.3s, transform 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}

.download-btn:hover {
  opacity: 0.85;
  transform: translateY(-2px);
}

.download-btn:active {
  transform: scale(0.95);
}

.links {
  margin-top: 1rem;
  display: flex;
  gap: 2rem;
}

.link-item {
  color: var(--vt-c-text-light-1);
  text-decoration: none;
  padding: 8px 16px;
  border: 1px solid var(--color-border);
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.3s, transform 0.3s ease;
}

.link-item:hover {
  background-color: var(--color-border-hover);
  transform: translateY(-2px);
}

.link-item:active {
  transform: scale(0.95);
}

.title {
  font-size: 2.6rem;
  font-weight: 600;
  color: var(--vt-c-text-light-1);
  margin: 0.5rem 0;
}

.description {
  font-size: 1.1rem;
  color: var(--vt-c-text-light-2);
  margin-top: 1rem;
}
</style>
