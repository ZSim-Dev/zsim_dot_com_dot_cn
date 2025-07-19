<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'

interface LatestReleaseCache {
  version: string
  download_url: string | null
  release_page_url: string | null
  available: boolean
}

const latestRelease = ref<LatestReleaseCache | null>(null)


// GitHub 发布页面的链接
const releasePageUrl = ref('https://github.com/ZZZSimulator/ZSim/releases')

// 稳定版下载配置
const stableVersion = ref({
  url: '#', // 后端控制的下载链接
  available: false // 后端控制是否可点击
})

onMounted(async () => {
  const response = await axios.get<LatestReleaseCache>('/api/github/latest-release')
  latestRelease.value = response.data
  const isInRelease = await axios.get<boolean>('/api/is_in_release')
  if (isInRelease.data) {
    stableVersion.value.url = latestRelease.value.download_url
    stableVersion.value.available = latestRelease.value.available
  }
  console.log(latestRelease.value)
})

</script>

<template>
  <div class="downloads-page">
    <header class="page-header">
      <h1>ZSim下载</h1>
      <p class="subtitle">获取最新版本。</p>
      <router-link to="/docs" class="docs-link">阅读开始文档 →</router-link>
    </header>

    <main class="content-container">
      <div class="version-display">
        当前最新版本: <strong><a :href="latestRelease?.release_page_url || 'https://github.com/ZZZSimulator/ZSim/releases/latest'" target="_blank">{{ latestRelease?.version || '加载中...' }}</a></strong>
      </div>

      <div class="actions-container">
        <a :href="releasePageUrl" target="_blank" class="action-btn release-btn">
          前往发布页面
        </a>
        <a :href="stableVersion.url" class="action-btn download-btn" :class="{ 'disabled': !stableVersion.available }">
          下载稳定版
        </a>
      </div>

      <div v-if="!stableVersion.available" class="notice">
        <p>目前暂未发布稳定版，请自行从发布页面下载代码或预发布版本运行。</p>
      </div>
    </main>
  </div>
</template>

<style scoped>
.downloads-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.page-header .subtitle {
  font-size: 1.1rem;
  color: var(--color-description);
  margin-bottom: 1rem;
}

.page-header .docs-link {
  color: var(--downloads-link);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.page-header .docs-link:hover {
  color: var(--downloads-link-hover);
}

.content-container {
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 3rem 2.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, border-color 0.3s ease;
  text-align: center;
}

@media (prefers-color-scheme: dark) {
  .content-container {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
  }
}

.version-display {
  color: var(--color-text);
  font-size: 1.2rem;
  margin-bottom: 2.5rem;
}

.version-display strong {
  font-weight: 600;
  color: var(--downloads-link);
}

.actions-container {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.release-btn {
  background-color: var(--color-background-mute);
  color: var(--color-text);
  border-color: var(--color-border-hover);
}

.release-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.download-btn {
  background-color: var(--downloads-link);
  color: white;
}

.download-btn:hover {
  background-color: var(--downloads-link-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.download-btn.disabled {
  background-color: var(--color-border);
  color: var(--color-description);
  cursor: not-allowed;
  pointer-events: none;
}

.download-btn.disabled:hover {
  transform: none;
  box-shadow: none;
}

.notice {
  margin-top: 2rem;
  padding: 1rem;
  background-color: var(--color-background);
  border-radius: 8px;
  color: var(--color-description);
  font-size: 0.9rem;
  border: 1px solid var(--color-border);
}

@media (max-width: 768px) {
  .downloads-page {
    padding: 1rem;
  }

  .content-container {
    padding: 2rem 1.5rem;
  }

  .actions-container {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>