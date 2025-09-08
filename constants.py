from dotenv import load_dotenv
import os

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_ENDPOINT_KEY = "https://chat-ai.academiccloud.de/v1/"
LLM_MODEL_NAME = 'meta-llama-3.1-8b-instruct'
EMBEDDING_MODEL_NAME = "e5-mistral-7b-instruct"