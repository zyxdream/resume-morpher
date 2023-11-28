
# customzied RAG queries (break down steps)
# chunking -> indexing -> composed-indexing (if needed) -> embedding -> retrival -> augmented

from llama_index import ServiceContext, LLMPredictor, OpenAIEmbedding, PromptHelper
from llama_index.embeddings import openai
from llama_index.llms import OpenAI
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import set_global_service_context
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("here")
# llm = OpenAI(model='gpt-3.5-turbo', temperature=0, max_tokens=256)
# embed_model = OpenAIEmbedding()
# text_splitter = TokenTextSplitter(
#   separator=" ",
#   chunk_size=1024,
#   chunk_overlap=20,
#   backup_separators=["\n"],
#   tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
# )
# node_parser = SimpleNodeParser.from_defaults(
#   text_splitter=text_splitter
# )
# prompt_helper = PromptHelper(
#   context_window=4096,
#   num_output=256,
#   chunk_overlap_ratio=0.1,
#   chunk_size_limit=None
# )
#
# # The service context container is a utility container for LlamaIndex index and query classes
# service_context = ServiceContext.from_defaults(
#   llm=llm,
#   embed_model=embed_model,
#   node_parser=node_parser,
#   prompt_helper=prompt_helper
# )
#
# documents = SimpleDirectoryReader(input_dir='data').load_data()
#
# # Each vector store index class is a combination of a base vector store index class and a vector store
# # from_document: Create index from documents.
# index = VectorStoreIndex.from_documents(
#     documents,
#     service_context = service_context
#     )
# # By default, LlamaIndex stores data in-memory, and this data can be explicitly persisted if desired:
# # storage_context.persist(persist_dir="<persist_dir>")
# # This will persist data to disk, under the specified persist_dir (or ./storage by default).
# index.storage_context.persist()
#
# # reconnect to vector store
# # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# # storage_context = StorageContext.from_defaults(vector_store=vector_store)
# # index = GPTVectorStoreIndex([], storage_context=storage_context)
#
# query_engine = index.as_query_engine(service_context=service_context)
# response = query_engine.query("What is HNSW?")
# print(response)
