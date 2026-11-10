from fastapi import APIRouter

from models import MessageResponse, TranslationRequest, TranslationResponse
from services import MODEL_NAME, translate

router = APIRouter()


@router.get("/", response_model=MessageResponse)
def home():
    return MessageResponse(message="OpenAI Translation API is running")


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(data: TranslationRequest):
    return TranslationResponse(
        model=MODEL_NAME,
        source_language="en",
        target_language="fr",
        original_text=data.text,
        translated_text=await translate(data.text),
    )
