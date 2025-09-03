"""
Minimal example for a RAG pipeline.

:author: Jonathan Decker
"""

import llama_index_init
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings

if __name__ == "__main__":
    models = llama_index_init.init()

    # Assign custom models to global Settings
    Settings.llm = models["llm"]
    Settings.embed_model = models["embed_model"]

    documents = SimpleDirectoryReader("./data").load_data()
    vector_index = VectorStoreIndex.from_documents(documents)
    query_engine = vector_index.as_query_engine()

    response = query_engine.query("Summarize the given document.")
    print(response)
