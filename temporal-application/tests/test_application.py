import concurrent.futures
import uuid

import pytest
from temporalio.client import Client
from temporalio.worker import Worker

from app.main import query_model
from temporal.activities import index_document
from temporal.workflows import IndexDocumentsWorkflow


@pytest.mark.asyncio
async def test_end_to_end(test_document_url, reset_vector_store):
    client = await Client.connect("localhost:7233")
    task_queue = str(uuid.uuid4())
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        async with Worker(
            client,
            task_queue=task_queue,
            workflows=[IndexDocumentsWorkflow],
            activities=[index_document],
            activity_executor=activity_executor,
        ):
            indexed_pages = await client.execute_workflow(
                IndexDocumentsWorkflow.run,
                [test_document_url],
                id=str(uuid.uuid4()),
                task_queue=task_queue,
            )
    assert indexed_pages == 1
    response = query_model("What was Apple's earnings per share in 2021?")
    assert "5.67" in response
