from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.chat_service import ChatService
from app.core.logger import logger
from app.core.settings import get_settings
from typing import Optional, List

# Initialize the router and settings
router = APIRouter(tags=["Chat API Endpoints"])
config = get_settings()

# Enhanced request and response schemas
class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender (system/user/assistant)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="The user's input message")
    system_message: Optional[str] = Field(
        default=None,
        description="Optional custom system message for this interaction"
    )

class ChatResponse(BaseModel):
    response: str = Field(..., description="The model's response")
    
# Initialize the chat service
chat_service = ChatService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint to interact with the model in a chat format.
    
    Args:
        request: ChatRequest containing the user's prompt and optional system message
    
    Returns:
        ChatResponse containing the model's response
    
    Raises:
        HTTPException: If there's an error processing the request
    """
    logger.info(f"Received chat request with prompt: {request.prompt}")
    
    try:
        # Use custom system message if provided, otherwise use default from config
        system_message = request.system_message or config.SYSTEM_MESSAGE
        logger.debug(f"Using system message: {system_message}")
        
        response = chat_service.generate_response(
            prompt=request.prompt,
            system_message=system_message
        )
        
        logger.info(f"Generated response: {response}")
        return ChatResponse(response=response)
        
    except Exception as e:
        error_msg = f"Error during chat processing: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the chat request."
        )
