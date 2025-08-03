#!/usr/bin/env python3
import psycopg2
from sqlalchemy import make_url
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import Document
import pandas as pd
from llama_index.core import VectorStoreIndex
from llama_index.core import  StorageContext
import os


db_name = "vector_bd_movies"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")

url = make_url(connection_string)
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

csv_path = "input/movies-dataset.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at path: {csv_path}")
df = pd.read_csv(csv_path)
df = df.head()
documents = [
    Document(text=row.to_json(), metadata={"index": idx,"title": row['title'], "image": row['image']})
    for idx, row in df.iterrows()
]

print("Number of documents:", len(documents))
print("First document text:", documents[0].text)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True,
    num_workers=4
)


