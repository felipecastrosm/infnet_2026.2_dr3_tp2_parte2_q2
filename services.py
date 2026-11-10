import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

load_dotenv()
set_llm_cache(InMemoryCache())

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional translator. Translate the text provided by the user "
            "from English to French. Keep the original meaning, tone and formatting. "
            "Return only the translated text.",
        ),
        ("human", "{text}"),
    ]
)


@lru_cache
def get_chain() -> Runnable:
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0, timeout=30, max_retries=2)
    return prompt | llm | StrOutputParser()


async def translate(text: str) -> str:
    return await get_chain().ainvoke({"text": text})
