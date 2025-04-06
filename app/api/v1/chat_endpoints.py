from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.chat_service import ChatService
from app.core.logger import logger
from app.core.settings import get_model_settings, Config
from typing import Optional

router = APIRouter(tags=["Chat API Endpoints"])

class ChatRequest(BaseModel):
    model: str = Field(..., description="The model id to use for generating the response")
    prompt: str = Field(..., description="The student's question from the chat interface")
    problem: str = Field(..., description="The problem statement shown to the student")
    code: str = Field(..., description="The student's current code")
    output: str = Field(..., description="The current output of the student's code")
    system_message: Optional[str] = Field(
        default=None,
        description="Optional custom system message for this interaction"
    )

class ChatResponse(BaseModel):
    response: str = Field(..., description="The model's response")

model_settings = get_model_settings()
chat_services = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received chat request with prompt: {request.prompt}")

    try:
        config = model_settings[request.model]

        if request.model not in chat_services:
            logger.info(f"Loading model: {request.model}")
            chat_services[request.model] = ChatService(config)

        chat_service = chat_services[request.model]

        student_prompt = (
            "You are interacting with an undergraduate student learning Python programming. "
            "Your role is to help them reason through the problem and understand their mistakes without giving direct solutions.\n\n"
            "# Problem Description:\nThis is the programming task assigned to the student.\n"
            f"{request.problem}\n\n"
            "# Student's Code:\nThis is what the student has written so far.\n"
            f"{request.code}\n\n"
            "# Code Output:\nThis is the result or error produced when the student's code was run.\n"
            f"{request.output}\n\n"
            "# Student's Question:\nThis is the student's doubt or concern, as entered in the chat.\n"
            f"{request.prompt}\n\n"
        )

        system_message = request.system_message or config.SYSTEM_MESSAGE
        logger.debug(f"Using system message: {system_message}")

        response = chat_service.generate_response(
            prompt=student_prompt,
            system_message=system_message
        )

        logger.info(f"Generated response: {response}")
        return ChatResponse(response=response)

    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the chat request."
        )



