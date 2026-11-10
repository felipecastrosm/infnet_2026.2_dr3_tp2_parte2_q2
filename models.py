from pydantic import BaseModel, ConfigDict, Field


class MessageResponse(BaseModel):
    message: str


class TranslationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(min_length=1, max_length=10000, examples=["Hello, how are you today?"])


class TranslationResponse(BaseModel):
    model: str
    source_language: str
    target_language: str
    original_text: str
    translated_text: str
