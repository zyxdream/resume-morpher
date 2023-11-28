
# this is the minimal code for RAG queries (everything by default, highly encapsulated, no customization)
# original code:
# https://gpt-index.readthedocs.io/en/v0.7.6/getting_started/starter_example.html

import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("here")

from llama_index import VectorStoreIndex, SimpleDirectoryReader

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


reader = SimpleDirectoryReader(
    input_files=["./data/paul_graham/paul_graham_essay.txt"]
)

docs = reader.load_data()
print(f"Loaded {len(docs)} docs")

print("=== indexing starts ===")
index = VectorStoreIndex.from_documents(docs)
print("=== indexing ends ===")

query_engine = index.as_query_engine()
print("=== generate query engine ===")

prompt = "What did the author do growing up?"
print("* user asked prompt: ", prompt)
response = query_engine.query(prompt)
print("* response: ", response)
