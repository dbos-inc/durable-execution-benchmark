import os

from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url


def configure_index():
    Settings.chunk_size = 512
    db_url = os.environ.get("TEMPORAL_DATABASE_URL", None)
    if db_url is None:
        raise Exception("TEMPORAL_DATABASE_URL not provided")
    url = make_url(db_url)
    vector_store = PGVectorStore.from_params(
        database=url.database,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
    )
    vector_store._initialize()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex([], storage_context=storage_context)
    chat_engine = index.as_chat_engine()
    return index, chat_engine
