# SupportMind Frontend

React, Vite, and TypeScript frontend for the SupportMind chat API.

## Setup

Copy `.env.example` to `.env.local` and set `VITE_API_URL` to the backend base
URL. Then install dependencies and start the development server:

```bash
npm install
npm run dev
```

The Vite development server proxies `/api` requests to `VITE_API_URL`, avoiding
the need for backend-specific development CORS configuration.
