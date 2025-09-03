"""
Tests for the LLM and Embedding APIs of ChatAI

:author: Jonathan Decker
"""

from llama_index.core.llms import ChatMessage
from llama_index.core import Settings
import pytest
import llama_index_init


@pytest.fixture
def init():
    llama_index_init.init()


def test_llm_works(init):
    # Validate that LLM works
    message = [ChatMessage(content="hello", role="user")]
    llm = Settings.llm
    assert llm.chat(message).message.content == "Hello! How can I assist you today?",\
        f"Assert failed, LLM message is {llm.chat(message).message.content}"


def test_embedding_works(init):
    # Validate that embedding works
    embed_model = Settings.embed_model
    embeddings = embed_model.get_text_embedding("hello")
    assert len(embeddings) == 8192, f"Assert failed, embedding length is {len(embeddings)}"
