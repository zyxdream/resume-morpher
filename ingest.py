import json
# Customized RAG - Break Down Steps

# -> chunking/text splitting (nodes)
# -> indexing/embedding (indices)
# -> store in vector database (e.g. Chroma)
# -> retrieval
# -> synthenizer
# ->

from pathlib import Path
import fitz  # PymuPDF

import tiktoken
from llama_index import ServiceContext, LLMPredictor, OpenAIEmbedding, PromptHelper
from llama_index.llms import OpenAI
from llama_index.extractors import (
    QuestionsAnsweredExtractor,
    TitleExtractor,
)
from llama_index.ingestion import IngestionPipeline
from llama_index.node_parser import SentenceSplitter  # =SimpleNodeParser
from llama_index import VectorStoreIndex, SimpleDirectoryReader, get_response_synthesizer
from llama_index import set_global_service_context
from llama_index.schema import TextNode

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("here")



llm = OpenAI(model='gpt-3.5-turbo', temperature=0, max_tokens=256)
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

openai_mm_llm = OpenAIMultiModal(
    model="gpt-4-vision-preview", max_new_tokens=1500
)
print("model loaded")

# Defaults to OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002 and OpenAIEmbeddingMode.TEXT_SEARCH_MOD, options are
# SIMILARITY_MODE
embed_model = OpenAIEmbedding()

prompt_helper = PromptHelper(
    context_window=4096,
    num_output=256, # avoid unexpected cost
    chunk_overlap_ratio=0.1,
    chunk_size_limit=None
)
# The service context container is a utility container for LlamaIndex index and query classes
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
    prompt_helper = prompt_helper
)

# ==================================================
# ==== Build an Ingestion Pipeline from Scratch ====
# ==================================================

# % wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf"
# --2023-11-29 10:39:40--  https://arxiv.org/pdf/2307.09288.pdf
# =====  1. Load Data =====
file_path = "./data/llama2.pdf"
documents = fitz.open(file_path)
print(len(documents), " documents loaded")

# ====== 2. Use a Text Splitter to Split Documents  ======
# SentenceSplitter: Parse text with a preference for complete sentences
# other options: TokenTextSplitter, CodeSplitter
text_parser = SentenceSplitter.from_defaults(
  separator=" ",
  chunk_size=1024,
  chunk_overlap=20,
  paragraph_separator="\n\n\n",
  secondary_chunking_regex="[^,.;。]+[,.;。]?",
  tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)

text_chunks = []
# maintain relationship with source doc index, to help inject doc metadata in (3)
doc_idxs = []
for doc_idx, page in enumerate(documents):
    print("===== doc_idx = ", doc_idx, " =====")
    page_text = page.get_text("text")
    print("length of page text: ", len(page_text))
    print(page_text[:100])
    print("........")
    print(page_text[-100:])
    cur_text_chunks = text_parser.split_text(page_text)
    text_chunks.extend(cur_text_chunks)
    print("length of text chunks so far =", len(text_chunks))
    doc_idxs.extend([doc_idx] * len(cur_text_chunks))

print()
print(doc_idxs)
print(len(text_chunks), "text chunks after sentences parser")
print("text chunks 0 :\n", text_chunks[0])
print()

# ====== 3. Manually Construct Nodes from Text Chunks =====
# We convert each chunk into a TextNode object, a low-level data abstraction in LlamaIndex that stores content but also allows defining metadata + relationships with other Nodes.
# We inject metadata from the document into each node.
# This essentially replicates logic in our SentenceSplitter
nodes = []
for idx, text_chunk in enumerate(text_chunks):
    node = TextNode(text=text_chunk)
    src_doc_idx = doc_idxs[idx]
    src_page = documents[src_doc_idx]
    nodes.append(node)

print("*** node 0 ***\n", nodes[0])
print("*** node 0 metadata ***\n", nodes[0].metadata) # for now there's no metadata
# print a sample node
print("*** node 0 get content ***\n", nodes[0].get_content(metadata_mode=all))
print(len(nodes))

# for node in nodes:
#     node_embedding = embed_model.get_text_embedding(
#         node.get_content(metadata_mode=all)
#     )
#     node.embedding = node_embedding

indexes = VectorStoreIndex(nodes=nodes, service_context=service_context)
# simple query (can also be customized later)
query_engine = indexes.as_query_engine()
# query_str = "Can you tell me about the key concepts for safety finetuning"
query_str1 = "How is Llama2 different from other popular large language models? Particularly in terms of the Performance with tool use."
# query_str = "how many samples or prompts of human labeling did llama-2 use for safety evaluation?"
query_str2 = "can you show me the content of table 15"
response = query_engine.query(query_str1)
print("response without llm-extracted metadata: \n")
print(response)
response = query_engine.query(query_str2)
print("response without llm-extracted metadata: \n")
print(response)
print("*************")


# ====== 4. Extract Metadata (here we could use llm) from each Node ========
# We extract metadata from each Node using our Metadata extractors.
# This will add more metadata to each Node.
# extractors = [
#     TitleExtractor(nodes=3, llm=llm),
#     QuestionsAnsweredExtractor(questions=2, llm=llm),
# ]
# pipeline = IngestionPipeline(
#     transformations=extractors,
# )
# nodes = pipeline.run(nodes=nodes, in_place=False)
# print("*** adding more metadata ***: \n", nodes[0].metadata)
#
#
# # === 5. Build vectors (include generating Embeddings), Save & Reload ====
#
# # Each vector store index class is a combination of a base vector store index class and a vector store
# # Here we build indexes from nodes. Optional: from_document: with parser as additional arguments
# vector_indexes = VectorStoreIndex(nodes, service_context)
# # Persist index to disk
# filepath = "output/llama2paper_index"
# indexes.storage_context.persist(filepath)


from llama_index import StorageContext, load_index_from_storage

# Rebuild storage context
filepath = "output/llama2paper_index"
storage_context = StorageContext.from_defaults(persist_dir=filepath)

# Load index from the storage context
new_index = load_index_from_storage(storage_context)

# simple query (can also be customized later)
# new_query_engine = new_index.as_query_engine()
# response = query_engine.query(query_str)
# print("response with llm-extracted metadata: \n")
# print(response)

#
# from llama_index.storage.storage_context import StorageContext
#
# StorageContext(image_store=)