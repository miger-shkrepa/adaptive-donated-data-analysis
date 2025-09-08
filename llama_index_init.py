"""
Helper file to initialize the LLM and embedding model settings for LlamaIndex

:author: Jonathan Decker
"""

from llama_index.llms.openai_like import OpenAILike

from constants import (
    LLM_MODEL_NAME,
    LLM_API_ENDPOINT_KEY,
    EMBEDDING_MODEL_NAME,
    LLM_API_KEY
)

from llama_index.core import Settings

from vllm_embeddings import VLLMEmbedding


def init(api_key: str = LLM_API_KEY, end_point: str = LLM_API_ENDPOINT_KEY, llm_model_name: str = LLM_MODEL_NAME,
         embedding_model_name: str = EMBEDDING_MODEL_NAME, temperature: int = 0, max_tokens: int = 200) -> Settings:
    llm = OpenAILike(
        model=llm_model_name,
        is_chat_model=True,
        temperature=temperature,
        max_new_tokens=max_tokens,
        api_key=api_key,
        context_window=50000,
        api_base=end_point,
        default_headers={"inference-service": llm_model_name},
    )

    embed_model = VLLMEmbedding(
        model=embedding_model_name,
        api_key=api_key,
        api_base=end_point,
    )

    return {"llm": llm, "embed_model": embed_model}
