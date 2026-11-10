from contextlib import asynccontextmanager

import openai
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routes import router
from services import get_chain


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_chain()
    yield


app = FastAPI(title="OpenAI Translation API with LangChain", version="1.0.0", lifespan=lifespan)


@app.exception_handler(openai.AuthenticationError)
async def authentication_handler(request: Request, exc: openai.AuthenticationError):
    return JSONResponse(status_code=500, content={"detail": "Invalid OpenAI API key configuration"})


@app.exception_handler(openai.RateLimitError)
async def rate_limit_handler(request: Request, exc: openai.RateLimitError):
    return JSONResponse(status_code=429, content={"detail": "OpenAI rate limit exceeded, try again later"})


@app.exception_handler(openai.APITimeoutError)
async def timeout_handler(request: Request, exc: openai.APITimeoutError):
    return JSONResponse(status_code=504, content={"detail": "OpenAI request timed out"})


@app.exception_handler(openai.APIError)
async def api_error_handler(request: Request, exc: openai.APIError):
    return JSONResponse(status_code=502, content={"detail": f"OpenAI API error: {exc.message}"})


app.include_router(router)
