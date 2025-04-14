from typing import AsyncIterable, Annotated

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from loguru import logger

from presentation.dependencies import OrchestratorServiceDependency

router = APIRouter(prefix="/medical-qa-assistant")


class ConnectionManager:
    @staticmethod
    async def connect(websocket: WebSocket):
        await websocket.accept()

    @staticmethod
    async def send_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    @staticmethod
    async def send_stream(message_stream: AsyncIterable[str], websocket: WebSocket):
        async for chunk in message_stream:
            await websocket.send_text(chunk)


manager = ConnectionManager()


@router.websocket("/ws")
async def medical_qa_websocket(websocket: WebSocket, orchestrator: OrchestratorServiceDependency,
                               response_mode: Annotated[str, Query()]):
    """
    WebSocket endpoint for the medical qa assistant.
    """
    await manager.connect(websocket)
    try:
        if response_mode == "STREAM":
            while True:
                doctor_query = await websocket.receive_text()
                async for chunk in orchestrator.chat_stream(doctor_query):
                    await manager.send_message(chunk, websocket)
        elif response_mode == "NORMAL":
            while True:
                doctor_query = await websocket.receive_text()
                response = await orchestrator.chat(doctor_query)
                await manager.send_message(response.model_dump_json(), websocket)

    except WebSocketDisconnect:
        logger.info("Client disconnected.")
