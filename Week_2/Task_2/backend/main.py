import asyncio
import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect

from agent import StreamingAgent
from vector_store import VectorStore

load_dotenv()
app = FastAPI()

agent = StreamingAgent(
    model_name=os.getenv("MODEL"), api_key=os.getenv("OPENAI_API_KEY")
)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    """
    Endpoint to upload a file, save it locally, and index its content into the vector store.

    Args:
        file (UploadFile): Uploaded file.

    Returns:
        dict: JSON with status and filename.
    """
    save_dir = "data/files"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    vector_store = VectorStore()
    vector_store.index_file(file_path)

    return {"status": "ok", "filename": file.filename}


@app.get("/health")
async def health() -> dict[str, str]:
    """
    Health check endpoint.

    Returns
        dict[str, str]: status OK.
    """
    return {"status": "ok"}


@app.websocket("/stream")
async def stream_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint to handle streaming chat with the agent.

    Args:
        websocket (WebSocket): WebSocket connection.
    """
    await websocket.accept()
    current_task = None

    try:
        while True:
            msg = await websocket.receive_text()

            if msg == "__STOP__":
                if current_task and not current_task.done():
                    current_task.cancel()
                continue

            async def run_and_send():
                async for chunk in agent.run_stream(msg):
                    await websocket.send_text(chunk)

            current_task = asyncio.create_task(run_and_send())

    except WebSocketDisconnect:
        if current_task and not current_task.done():
            current_task.cancel()
        print("Client disconnected")
