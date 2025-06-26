# Frontend (React + Vite)

This is the frontend application for the LangChain Assistant. It connects via WebSocket to the backend server running on `ws://localhost:8000/stream`.

## Prerequisites

- Node.js
- npm (comes with Node.js)

## Setup & Run

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

3. Open your browser and go to:

`http://localhost:5173/`

## Notes

- The frontend expects the backend server with the WebSocket `/stream` endpoint to be running on `ws://localhost:8000`.
- You can configure the WebSocket URL in `App.jsx` if your backend runs on a different address or port.
