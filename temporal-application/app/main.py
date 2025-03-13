import logging
import uuid
from typing import List

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from temporalio.client import Client

from temporal.temporal import IndexDocumentsWorkflow

from .index import configure_index

app = FastAPI()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("temporal-application")


###########################
# Configure Vector Index
###########################

index, chat_engine = configure_index()

###########################
# Index Documents
###########################


class URLList(BaseModel):
    urls: List[str]


@app.post("/index")
async def index_endpoint(urls: URLList):
    client = await Client.connect("localhost:7233")
    await client.start_workflow(
        IndexDocumentsWorkflow.run,
        urls.urls,
        id=str(uuid.uuid4()),
        task_queue="index-task-queue",
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


###########################
# Query Index
###########################


class ChatSchema(BaseModel):
    message: str


@app.post("/chat")
def chat_workflow(chat: ChatSchema):
    response = query_model(chat.message)
    return {"content": response}


def query_model(message: str) -> str:
    return str(chat_engine.chat(message))
