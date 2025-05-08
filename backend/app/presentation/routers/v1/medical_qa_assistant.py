from typing import AsyncIterable

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

from presentation.dependencies import OrchestratorServiceDependency
from presentation.schemas.medical_qa_assistant import DoctorQuery, AssistantResponse

router = APIRouter(prefix="/medical-qa-assistant")


class ConnectionManager:
    @staticmethod
    async def connect(websocket: WebSocket):
        await websocket.accept()

    @staticmethod
    async def send_message(assistant_response: AssistantResponse, websocket: WebSocket):
        await websocket.send_text(assistant_response.model_dump_json())

    @staticmethod
    async def send_stream(message_stream: AsyncIterable[str], websocket: WebSocket):
        async for chunk in message_stream:
            await websocket.send_text(chunk)


manager = ConnectionManager()


@router.websocket("/general/ws")
async def general_medical_qa_websocket(websocket: WebSocket, orchestrator: OrchestratorServiceDependency):
    """
    WebSocket endpoint for the general medical qa assistant.
    """
    # Parse query parameters manually from websocket
    query_params = websocket.query_params
    response_mode = query_params.get("response_mode", "NORMAL")  # Default to "NORMAL" if not provided
    logger.info(f"Query params: {query_params}")

    await manager.connect(websocket)
    try:
        if response_mode == "STREAM":
            while True:
                json_doctor_query = await websocket.receive_json()
                doctor_query: DoctorQuery = DoctorQuery.model_validate(json_doctor_query)
                logger.info(f"doctor_query: {doctor_query}")
                await manager.send_stream(orchestrator.general_medical_qa_chat_stream(doctor_query), websocket)
        elif response_mode == "NORMAL":
            while True:
                json_doctor_query = await websocket.receive_json()
                doctor_query: DoctorQuery = DoctorQuery.model_validate(json_doctor_query)
                logger.info(f"doctor_query: {doctor_query}")
                assistant_response: AssistantResponse = await orchestrator.general_medical_qa_chat(doctor_query)
                await manager.send_message(assistant_response, websocket)

    except WebSocketDisconnect:
        logger.info("Client disconnected.")


@router.websocket("/patient/{patient_id}/ws")
async def patient_medical_qa_websocket(patient_id: str, websocket: WebSocket,
                                       orchestrator: OrchestratorServiceDependency):
    """
    WebSocket endpoint for the patient medical qa assistant.
    """

    logger.info(f"Patient ID: {patient_id}")

    await manager.connect(websocket)
    try:
        while True:
            json_doctor_query = await websocket.receive_json()
            doctor_query: DoctorQuery = DoctorQuery.model_validate(json_doctor_query)
            logger.info(f"doctor_query: {doctor_query}")
            assistant_response: AssistantResponse = await orchestrator.patient_medical_qa_chat(patient_id, doctor_query)
            await manager.send_message(assistant_response, websocket)
    except WebSocketDisconnect:
        logger.info("Client disconnected.")
