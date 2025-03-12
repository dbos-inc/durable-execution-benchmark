import logging
import os
from tempfile import TemporaryDirectory
from typing import List

import requests
from fastapi import FastAPI, Response, status
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.readers.file import PDFReader
from llama_index.vector_stores.postgres import PGVectorStore
from pydantic import BaseModel, HttpUrl


app = FastAPI()

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO);
logger = logging.getLogger('reference-application')

def configure_index():
    Settings.chunk_size = 512
    vector_store = PGVectorStore.from_params(
        database="reference_application",
        host="localhost",
        password=os.environ["PGPASSWORD"],
        port="5432",
        user="postgres",
    )
    vector_store._initialize()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex([], storage_context=storage_context)
    chat_engine = index.as_chat_engine()
    return index, chat_engine


index, chat_engine = configure_index()


def indexing_workflow(urls: List[HttpUrl]):
    indexed_pages = 0
    for url in urls:
        indexed_pages += index_document(url)
    indexed_pages = 0
    logger.info(f"Indexed {len(urls)} documents totaling {indexed_pages} pages")


def index_document(document_url: HttpUrl) -> int:
    with TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "file.pdf")
        with open(temp_file_path, "wb") as temp_file:
            with requests.get(document_url, stream=True) as r:
                r.raise_for_status()
                for page in r.iter_content(chunk_size=8192):
                    temp_file.write(page)
            temp_file.seek(0)
            reader = PDFReader()
            pages = reader.load_data(temp_file_path)
    for page in pages:
        index.insert(page)
    return len(pages)


class URLList(BaseModel):
    urls: List[HttpUrl]


@app.post("/index")
async def index_endpoint(urls: URLList):
    indexing_workflow(urls.urls)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



class ChatSchema(BaseModel):
    message: str


@app.post("/chat")
def chat_workflow(chat: ChatSchema):
    response = query_model(chat.message)
    return {"content": response}


def query_model(message: str) -> str:
    return str(chat_engine.chat(message))


