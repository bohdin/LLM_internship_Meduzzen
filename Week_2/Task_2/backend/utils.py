from fastapi import WebSocket

from agent import StreamingAgent


async def run_and_send(agent: StreamingAgent, websocket: WebSocket, msg: str) -> None:
    """
    Handles agent streaming output and sends chunks to the client via WebSocket.

    Args:
        agent (StreamingAgent): The initialized LangChain streaming agent.
        websocket (WebSocket): WebSocket connection.
        msg (str): The user input to be passed to the agent.
    """
    async for chunk in agent.run_stream(msg):
        await websocket.send_text(chunk)
    await websocket.send_text("[DONE]")
