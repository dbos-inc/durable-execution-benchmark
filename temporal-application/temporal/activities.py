import os
from dataclasses import dataclass
from tempfile import TemporaryDirectory

import requests
from llama_index.readers.file import PDFReader
from temporalio import activity

from app.index import configure_index

index, chat_engine = configure_index()


@dataclass
class IndexDocumentsParams:
    document_url: str


@activity.defn(name="index_document")
def index_document(input: IndexDocumentsParams) -> int:
    with TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "file.pdf")
        with open(temp_file_path, "wb") as temp_file:
            with requests.get(input.document_url, stream=True) as r:
                r.raise_for_status()
                for page in r.iter_content(chunk_size=8192):
                    temp_file.write(page)
            temp_file.seek(0)
            reader = PDFReader()
            pages = reader.load_data(temp_file_path)
    for page in pages:
        index.insert(page)
    return len(pages)
