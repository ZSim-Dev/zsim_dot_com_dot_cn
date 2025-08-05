# ZSim官网

[English](./README.md) | 中文

这是ZSim的官方网站，一个为游戏 设计的综合性模拟平台。

## 项目结构

这是一个全栈Web应用程序，包含：
- **前端**：使用Vue 3、TypeScript、Vite和Vue Router
- **后端**：使用Python FastAPI和SQLite数据库
- **功能特性**：
  - ZZZ模拟平台
  - 文档查看器
  - 用户认证（邮箱/短信）
  - 功能投票系统
  - 下载链接

## 开发环境设置

### 前端 (Vue 3)
```bash
cd frontend
npm install
npm run dev
```

### 后端 (FastAPI)
```bash
cd backend
uv sync
python main.py
```

## 文档

- [中文快速入门指南](./frontend/docs/doc.zh.md)
- [English Quick Start Guide](./frontend/docs/doc.en.md)

## 许可证

该项目根据GNU通用公共许可证v3.0授权 - 详情请参见[LICENSE](./LICENSE)文件。