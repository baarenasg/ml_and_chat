from fastapi import FastAPI, Request
import time
from fastapi import Response
import os
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex
from sqlalchemy import make_url
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.prompts import RichPromptTemplate
import textwrap
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI

connection_string = os.getenv("PG_CONNECTION_STRING")


url = make_url(connection_string)
db_name = "vector_bd_movies"


vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="movies",
    embed_dim=1536,  # openai embedding dimension
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,
)

llm = OpenAI(model="gpt-4.1-nano")

template_str = """Hemos proporcionado la siguiente información de contexto.
    ---------------------
    {{ context_str }}
    ---------------------
    Dada esta información, por favor responde la siguiente pregunta: {{ query_str }}
    Responde de manera concisa y directa, utilizando la información proporcionada en el contexto.
    Si no hay información relevante en el contexto, responde con "No tengo información sobre eso".
    Si la pregunta no es clara, responde con "Pregunta no clara".
    Si la pregunta es sobre una película, responde con el título de la película y su imagen al final para que se muestre bien en la interfaz de usuario.
    Si la intención de la pregunta es un saludo di que eres un asistente virtual y sabes sobre peliculas de los 80'
    """
qa_template = RichPromptTemplate(template_str)

def get_response(query):
    """
    Function to get a response from the retriever based on the query.
    """
    nodes = retriever.retrieve(query['content'])
    context_str = "\n\n".join([node.node.get_content() for node in nodes])
    # Retrieve nodes based on the query
    
    prompt = qa_template.format(context_str=context_str, query_str=query)
    response = llm.complete(prompt)
    return response.text