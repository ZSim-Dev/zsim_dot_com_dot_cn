<script setup lang="ts">

</script>

<template>
  <div class="homepage">
    <div class="header">
      <div class="logo">
        <img src="/assets/zsim-logo.svg" alt="logo" class="logo" />
      </div>
      <p class="title">ZSim 模拟器</p>
      <p class="description">ZSim 是一个独立的绝区零自动模拟器，我们实现了模拟绝区零的战斗，并支持全脚本化的出招。</p>
    </div>

    <div class="main-content">
      <router-link to="/downloads" class="download-btn">下载桌面版</router-link>
      <div class="links">
        <router-link to="/docs" class="link-item">使用文档</router-link>
        <a href="/vote" class="link-item">功能投票</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.homepage {
  padding: 2rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeInPage 0.8s ease-out;
  min-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-top: 1.5rem;
}

@keyframes fadeInPage {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.main-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  width: 140px;
  height: 140px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 28px;
  margin: 0 auto 1.5rem;
  animation: floatLogo 3s ease-in-out infinite;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.logo::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: rotate(45deg);
  animation: shimmer 2s infinite;
}

@keyframes floatLogo {

  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }

  50% {
    transform: translateY(-10px) rotate(2deg);
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%) rotate(45deg);
  }

  100% {
    transform: translateX(100%) rotate(45deg);
  }
}

.download-btn {
  padding: 16px 48px;
  font-size: 1.3rem;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  position: relative;
  overflow: hidden;
}

.download-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.download-btn:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
}

.download-btn:hover::before {
  left: 100%;
}

.download-btn:active {
  transform: translateY(-1px) scale(0.98);
}

.links {
  margin-top: 1.5rem;
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.link-item {
  color: var(--vt-c-text-light-1);
  text-decoration: none;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  border-radius: 25px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
  backdrop-filter: blur(5px);
  position: relative;
  overflow: hidden;
}

.link-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
  transition: width 0.3s ease;
  z-index: -1;
}

.link-item:hover {
  transform: translateY(-2px);
  border-color: rgba(102, 126, 234, 0.3);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.link-item:hover::before {
  width: 100%;
}

.link-item:active {
  transform: translateY(0) scale(0.95);
}

.title {
  font-size: 3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 1rem 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: -0.02em;
}

.description {
  font-size: 1.2rem;
  color: var(--color-description);
  margin-top: 1rem;
  line-height: 1.6;
  max-width: 600px;
  text-align: center;
  opacity: 0.9;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .homepage {
    padding: 1rem;
    margin: 1rem auto;
  }

  .title {
    font-size: 2.2rem;
  }

  .description {
    font-size: 1rem;
  }

  .download-btn {
    padding: 14px 36px;
    font-size: 1.1rem;
  }

  .links {
    gap: 1rem;
  }

  .link-item {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}
</style>
