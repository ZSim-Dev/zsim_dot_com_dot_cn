# ZSim 官网

[English](./README.md) | 中文

这是 ZSim 的官方网站，一个为游戏 设计的综合性模拟平台。

## 项目结构

这是一个全栈 Web 应用程序，包含：

- **前端**：使用 Vue 3、TypeScript、Vite 和 Vue Router
- **后端**：使用 Python FastAPI 和 SQLite 数据库
- **功能特性**：
  - ZZZ 模拟平台
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
.venv\Scripts\activate  # On Unix like: .venv/bin/activate
cd ..
uv run uvicorn backend.main:app --reload
```

#### 注意事项

1. 如果是首次启动后端服务，请将 `backend/config.example.toml` 复制为 `backend/config.toml`
1. 可以将 `backend/config.toml` 中的 `send_real_email` 改为 `false` 方便本地开发
1. Mac OS 遇到 `permission denied: .venv/bin/activate` 权限问题，可以尝试使用 `chmod +x .venv/bin/activate` 来解决

## 文档

- [中文快速入门指南](./frontend/docs/doc.zh.md)
- [English Quick Start Guide](./frontend/docs/doc.en.md)

## 许可证

该项目根据 GNU 通用公共许可证 v3.0 授权 - 详情请参见[LICENSE](./LICENSE)文件。
