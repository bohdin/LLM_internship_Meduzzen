import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from agent import StreamingAgent

load_dotenv()
app = FastAPI()

agent = StreamingAgent(
    model_name=os.getenv("MODEL"), api_key=os.getenv("OPENAI_API_KEY")
)


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
    WebSocket endpoint for streaming agent responses.
    
    Receives user input text and streams back chunks of the agent's response.
    
    Args:
        websocket (WebSocket): WebSocket connection.
    """
    await websocket.accept()
    try:
        while True:
            user_input = await websocket.receive_text()
            async for chunk in agent.run_stream(user_input):
                try:
                    await websocket.send_text(chunk)
                except RuntimeError:
                    print("Attempted to send on closed WebSocket")
                    break
    except WebSocketDisconnect:
        print("Client disconnected WebSocket")
