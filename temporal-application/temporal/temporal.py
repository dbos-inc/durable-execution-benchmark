import asyncio
import concurrent.futures
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from app.index import configure_index
from temporal.activities import index_document
from temporal.workflows import IndexDocumentsWorkflow

index, chat_engine = configure_index()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("temporal-worker")


async def main():
    client = await Client.connect("localhost:7233")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue="index-task-queue",
            workflows=[IndexDocumentsWorkflow],
            activities=[index_document],
            activity_executor=activity_executor,
        )
        logger.info("Worker ready")
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
