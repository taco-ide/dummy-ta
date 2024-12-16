from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import ChatService
from app.core.logger import logger

# Initialize the router
router = APIRouter(tags=["TA API Endpoints"])

# Chat request and response schemas
class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

# Initialize the chat service
chat_service = ChatService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint to interact with the model. It handles a single user prompt
    and returns the model's response.
    """
    logger.info(f"Received chat request with prompt: {request.prompt}")
    try:
        response = chat_service.generate_response(prompt=request.prompt)
        logger.info(f"Generated response: {response}")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the chat request.")
