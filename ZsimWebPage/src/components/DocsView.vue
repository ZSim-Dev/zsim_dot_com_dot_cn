<template>
  <div class="docs-container">
    <div class="sidebar">
      <div class="toc" v-html="tocHtml"></div>
    </div>
    <div class="docs-content">
      <div class="header">
        <h1>使用文档</h1>
        <p>了解如何使用 ZSim 模拟器的详细指南</p>
      </div>
      <div class="markdown-body">
        <VueMarkdownIt :source="mdContent" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import VueMarkdownIt from 'vue3-markdown-it'
import 'highlight.js/styles/github.css'

const mdContent = ref('')
const tocHtml = ref('')

onMounted(async () => {
  const res = await fetch('/src/docs/docs.md')
  const text = await res.text()
  mdContent.value = text
  generateTOC(text)
})

function generateTOC(mdText: string) {
  const headings = mdText.match(/^#{1,6} .+/gm)
  if (headings) {
    tocHtml.value = headings.map(heading => {
      const level = heading.match(/^#+/)?.[0].length || 1
      const title = heading.replace(/^#+\s/, '')
      const anchor = title.toLowerCase().replace(/\s+/g, '-')
      return `<a href="#${anchor}" class="toc-level-${level}">${title}</a>`
    }).join('')
  }
}
</script>

<style scoped>
.docs-container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.sidebar {
  width: 250px;
  padding-right: 2rem;
  position: sticky;
  top: 2rem;
  align-self: flex-start;
}

.toc {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  padding: 1rem;
}

.toc a {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  text-decoration: none;
}

.toc a:hover {
  color: #0066cc;
}

.toc-level-2 {
  padding-left: 1rem;
}

.toc-level-3 {
  padding-left: 2rem;
}

.docs-content {
  flex: 1;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.markdown-body {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  padding: 2rem;
}

.markdown-body :deep(pre) {
  background: #f6f8fa;
  padding: 1rem;
  border-radius: 6px;
  overflow: auto;
}

.markdown-body :deep(code) {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}
</style>
