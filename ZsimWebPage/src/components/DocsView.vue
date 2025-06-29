<template>
  <div class="docs-container">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <nav class="toc-nav">
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

      <article class="markdown-container" v-html="renderedMarkdown"></article>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

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

onMounted(async () => {
  try {
    const res = await fetch('/src/docs/docs.md')
    const text = await res.text()
    mdContent.value = text

    // 生成目录
    generateTOC(text)

    // 渲染markdown
    const rendered = md.render(text)
    renderedMarkdown.value = addAnchorIds(rendered)

    // 处理目录点击
    handleTocClick()
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
  border: 1px solid rgba(229, 231, 235, 0.8);
  max-height: calc(100vh - 140px);
  overflow-y: auto;
}

.toc-title {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.toc-content {
  display: flex;
  flex-direction: column;
}

.toc-link {
  display: block;
  padding: 0.5rem 0;
  color: #6b7280;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  line-height: 1.4;
}

.toc-link:hover {
  color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.1);
  padding-left: 0.5rem;
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
  color: #9ca3af;
}

.toc-level-4,
.toc-level-5,
.toc-level-6 {
  padding-left: 3rem;
  font-size: 0.75rem;
  color: #9ca3af;
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
  border-bottom: 1px solid #e5e7eb;
}

.content-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 1rem 0;
}

.subtitle {
  font-size: 1.1rem;
  color: #6b7280;
  margin: 0;
}

/* Markdown 内容样式 */
.markdown-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(229, 231, 235, 0.8);
  line-height: 1.7;
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
  color: #111827;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.markdown-container :deep(h2) {
  font-size: 1.5rem;
  color: #374151;
}

.markdown-container :deep(h3) {
  font-size: 1.25rem;
  color: #4b5563;
}

.markdown-container :deep(p) {
  margin-bottom: 1rem;
  color: #374151;
}

.markdown-container :deep(pre) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.markdown-container :deep(code) {
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', monospace;
  font-size: 0.9em;
}

.markdown-container :deep(p code) {
  background: #f1f5f9;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  color: #e11d48;
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
  background: #f8fafc;
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
  border-radius: 0 8px 8px 0;
}

.markdown-container :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
}

.markdown-container :deep(th),
.markdown-container :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  text-align: left;
}

.markdown-container :deep(th) {
  background: #f9fafb;
  font-weight: 600;
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
