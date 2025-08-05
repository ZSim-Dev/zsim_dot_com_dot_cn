# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a full-stack web application with a Vue 3 frontend and a Python FastAPI backend:

- `frontend/` - Frontend Vue 3 application
- `backend/` - Python FastAPI backend API
- `cct.ps1` - PowerShell script (likely for deployment or setup)

## Common Development Commands

### Frontend (Vue 3)

- Install dependencies: `npm install` (in ZsimWebPage directory)
- Development server: `npm run dev` (starts Vite dev server with hot reload)
- Build for production: `npm run build` (compiles and minifies for production)
- Type checking: `npm run type-check` (runs vue-tsc)
- Unit tests: `npm run test:unit` (runs Vitest)
- Format code: `npm run format` (runs Prettier)

### Backend (FastAPI)

- Install dependencies: `uv sync` (in backend directory)
- Development server: `python main.py` (starts Uvicorn server with hot reload on port 8000)

## Code Architecture

### Frontend Architecture

- Vue 3 with TypeScript
- Vue Router for client-side routing
- Vue I18n for internationalization (Chinese/English)
- Vite for build tooling
- Component-based architecture with:
  - Home page
  - Documentation viewer
  - Login system
  - Feature voting
  - Downloads page
- Markdown documentation rendering with vue3-markdown-it

### Backend Architecture

- FastAPI for REST API
- SQLite for authentication database
- CORS enabled for frontend integration
- Modular structure:
  - Authentication system (email/SMS verification)
  - GitHub release API integration
  - Feature voting system
- API endpoints under `/api` prefix

### Key Integrations

- Frontend proxies `/api` requests to backend (http://localhost:8000)
- Internationalization with JSON locale files
- GitHub releases integration for download information