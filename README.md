# ZSim Website

English | [中文](./README.zh.md)

This is the official website for ZSim, a comprehensive simulation platform for the game ZZZ (Zenless Zone Zero).

## Project Structure

This is a full-stack web application with:

- **Frontend**: Vue 3 with TypeScript, Vite, and Vue Router
- **Backend**: Python FastAPI with SQLite database
- **Features**:
  - Simulation platform for ZZZ
  - Documentation viewer
  - User authentication (email/SMS)
  - Feature voting system
  - Download links

## Development Setup

### Frontend (Vue 3)

```bash
cd frontend
npm install
npm run dev
```

### Backend (FastAPI)

```bash
cd backend
uv sync
.venv\Scripts\activate  # On Unix like: .venv/bin/activate
cd ..
uv run uvicorn backend.main:app --reload
```

#### Notes

1. If this is your first time starting the backend service, copy `backend/config.example.toml` to `backend/config.toml`.
2. For local development, you can set `send_real_email = false` in `backend/config.toml` to disable real email sending.
3. On macOS, if you encounter a `permission denied: .venv/bin/activate` error, try running `chmod +x .venv/bin/activate` to fix the permission issue.

## Documentation

- [中文快速入门指南](./frontend/docs/doc.zh.md)
- [English Quick Start Guide](./frontend/docs/doc.en.md)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
