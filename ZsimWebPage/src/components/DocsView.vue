<template>
  <div class="docs-container" :class="{ 'dark-mode': isDarkMode }">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <nav class="toc-nav" :class="{ 'dark-mode': isDarkMode }">
        <h3 class="toc-title">目录</h3>
        <div class="toc-content" v-html="tocHtml"></div>
      </nav>
    </aside>

    <!-- 主要内容区域 -->
    <main class="docs-content">
      <div class="content-header">
        <h1>使用文档</h1>
        <p class="subtitle">了解如何使用 ZSim 模拟器的详细指南</p>
      </div>

      <article class="markdown-container" :class="{ 'dark-mode': isDarkMode }" v-html="renderedMarkdown"></article>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, inject, watch } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import 'highlight.js/styles/github-dark.css'

// 注入深色模式状态（如果父组件提供）
const isDarkMode = inject('isDarkMode', ref(false))

const mdContent = ref('')
const renderedMarkdown = ref('')
const tocHtml = ref('')

// 配置 markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>' +
          hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
          '</code></pre>'
      } catch (__) { }
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
  }
})

/**
 * 生成目录导航
 * @param mdText markdown文本内容
 */
function generateTOC(mdText: string): void {
  const headings = mdText.match(/^#{1,6} .+/gm)
  if (headings) {
    const tocItems = headings.map(heading => {
      const level = heading.match(/^#+/)?.[0].length || 1
      const title = heading.replace(/^#+\s/, '')
      const anchor = title.toLowerCase()
        .replace(/[^\w\s-]/g, '') // 移除特殊字符
        .replace(/\s+/g, '-') // 空格替换为连字符
        .trim()

      return {
        level,
        title,
        anchor
      }
    })

    // 生成嵌套的目录HTML
    tocHtml.value = tocItems.map(item =>
      `<a href="#${item.anchor}" class="toc-link toc-level-${item.level}" data-level="${item.level}">
        ${item.title}
      </a>`
    ).join('')
  }
}

/**
 * 为markdown内容添加锚点ID
 * @param html 渲染后的HTML内容
 */
function addAnchorIds(html: string): string {
  return html.replace(/<h([1-6])>(.*?)<\/h[1-6]>/g, (match, level, content) => {
    const anchor = content.toLowerCase()
      .replace(/<[^>]*>/g, '') // 移除HTML标签
      .replace(/[^\w\s-]/g, '') // 移除特殊字符
      .replace(/\s+/g, '-') // 空格替换为连字符
      .trim()
    return `<h${level} id="${anchor}">${content}</h${level}>`
  })
}

/**
 * 处理目录点击事件
 */
function handleTocClick(): void {
  nextTick(() => {
    const tocLinks = document.querySelectorAll('.toc-link')
    tocLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault()
        const href = (e.target as HTMLAnchorElement).getAttribute('href')
        if (href) {
          const targetId = href.substring(1)
          const targetElement = document.getElementById(targetId)
          if (targetElement) {
            targetElement.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            })
          }
        }
      })
    })
  })
}

/**
 * 动态切换代码高亮主题
 */
function updateCodeTheme(): void {
  const existingLink = document.querySelector('link[data-hljs-theme]')
  if (existingLink) {
    existingLink.remove()
  }
  
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.setAttribute('data-hljs-theme', 'true')
  link.href = isDarkMode.value 
    ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css'
    : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css'
  document.head.appendChild(link)
}

// 监听深色模式变化
watch(isDarkMode, () => {
  updateCodeTheme()
}, { immediate: true })

onMounted(async () => {
  try {
    const res = await fetch('/docs/docs.md')
    const text = await res.text()
    mdContent.value = text

    // 生成目录
    generateTOC(text)

    // 渲染markdown
    const rendered = md.render(text)
    renderedMarkdown.value = addAnchorIds(rendered)

    // 处理目录点击
    handleTocClick()
    
    // 初始化代码主题
    updateCodeTheme()
  } catch (error) {
    console.error('加载文档失败:', error)
    renderedMarkdown.value = '<p>文档加载失败，请稍后重试。</p>'
  }
})
</script>

<style scoped>
.docs-container {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  gap: 2rem;
  min-height: calc(100vh - 120px);
}

.docs-container h1{
  flex: 1;
  color: var(--color-heading);
}

.docs-container p{
  color: var(--color-text);
}

/* 侧边栏样式 */
.sidebar {
  width: 280px;
  flex-shrink: 0;
}

.toc-nav {
  position: sticky;
  top: 100px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--color-border);
  max-height: calc(100vh - 140px);
  overflow-y: auto;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .toc-nav {
    background: rgba(40, 40, 40, 0.95);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
  }
}

.toc-title {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: 0.5rem;
  transition: color 0.3s ease, border-color 0.3s ease;
}

.toc-content {
  display: flex;
  flex-direction: column;
}

.toc-link {
  display: block;
  padding: 0.5rem 0;
  color: var(--color-text);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  line-height: 1.4;
  opacity: 0.8;
}

.toc-link:hover {
  color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.1);
  padding-left: 0.5rem;
  opacity: 1;
}

@media (prefers-color-scheme: dark) {
  .toc-link:hover {
    background-color: rgba(59, 130, 246, 0.2);
  }
}

.toc-level-1 {
  font-weight: 600;
  margin-top: 0.5rem;
}

.toc-level-2 {
  padding-left: 1rem;
  font-size: 0.85rem;
}

.toc-level-3 {
  padding-left: 2rem;
  font-size: 0.8rem;
  opacity: 0.6;
}

.toc-level-4,
.toc-level-5,
.toc-level-6 {
  padding-left: 3rem;
  font-size: 0.75rem;
  opacity: 0.6;
}

/* 主内容区域 */
.docs-content {
  flex: 1;
  min-width: 0;
}

.content-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);
  transition: border-color 0.3s ease;
}

.content-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 1rem 0;
}

.subtitle {
  font-size: 1.1rem;
  color: var(--color-text);
  margin: 0;
  opacity: 0.8;
  transition: color 0.3s ease;
}

/* Markdown 内容样式 */
.markdown-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--color-border);
  line-height: 1.7;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .markdown-container {
    background: rgba(40, 40, 40, 0.95);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
  }
}

/* 深度选择器用于样式化渲染的markdown内容 */
.markdown-container :deep(h1),
.markdown-container :deep(h2),
.markdown-container :deep(h3),
.markdown-container :deep(h4),
.markdown-container :deep(h5),
.markdown-container :deep(h6) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  line-height: 1.3;
  scroll-margin-top: 100px;
}

.markdown-container :deep(h1) {
  font-size: 2rem;
  color: var(--color-heading);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: 0.5rem;
  transition: color 0.3s ease, border-color 0.3s ease;
}

.markdown-container :deep(h2) {
  font-size: 1.5rem;
  color: var(--color-heading);
  transition: color 0.3s ease;
}

.markdown-container :deep(h3) {
  font-size: 1.25rem;
  color: var(--color-heading);
  opacity: 0.9;
  transition: color 0.3s ease;
}

.markdown-container :deep(p) {
  margin-bottom: 1rem;
  color: var(--color-text);
  transition: color 0.3s ease;
}

.markdown-container :deep(pre) {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1.5rem;
  overflow-x: auto;
  margin: 1.5rem 0;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.markdown-container :deep(code) {
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', monospace;
  font-size: 0.9em;
}

.markdown-container :deep(p code) {
  background: var(--color-background-mute);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  color: #e11d48;
  transition: background-color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .markdown-container :deep(p code) {
    color: #fca5a5;
  }
}

/* 深色模式样式覆盖 */
.dark-mode .toc-nav {
  background: rgba(40, 40, 40, 0.95) !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
}

.dark-mode .markdown-container {
  background: rgba(40, 40, 40, 0.95) !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
}

.dark-mode .toc-link:hover {
  background-color: rgba(59, 130, 246, 0.2) !important;
}

.dark-mode .markdown-container :deep(p code) {
  color: #fca5a5 !important;
}

.markdown-container :deep(ul),
.markdown-container :deep(ol) {
  margin: 1rem 0;
  padding-left: 2rem;
}

.markdown-container :deep(li) {
  margin-bottom: 0.5rem;
}

.markdown-container :deep(blockquote) {
  border-left: 4px solid #3b82f6;
  background: var(--color-background-soft);
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
  border-radius: 0 8px 8px 0;
  transition: background-color 0.3s ease;
}

.markdown-container :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
}

.markdown-container :deep(th),
.markdown-container :deep(td) {
  border: 1px solid var(--color-border);
  padding: 0.75rem;
  text-align: left;
  transition: border-color 0.3s ease;
}

.markdown-container :deep(th) {
  background: var(--color-background-soft);
  font-weight: 600;
  transition: background-color 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .docs-container {
    flex-direction: column;
    padding: 1rem;
  }

  .sidebar {
    width: 100%;
    order: 2;
  }

  .toc-nav {
    position: static;
    margin-top: 2rem;
  }

  .docs-content {
    order: 1;
  }
}

@media (max-width: 768px) {
  .content-header h1 {
    font-size: 2rem;
  }

  .markdown-container {
    padding: 1.5rem;
  }
}
</style>
