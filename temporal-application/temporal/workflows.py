import asyncio
import logging
from datetime import timedelta
from typing import List

from temporalio import workflow

# Required to import activities, which contain non-deterministic code
with workflow.unsafe.imports_passed_through():
    from temporal.activities import IndexDocumentsParams, index_document

logger = logging.getLogger("temporal-worker")


@workflow.defn(name="IndexDocumentsWorkflow")
class IndexDocumentsWorkflow:
    @workflow.run
    async def run(self, urls: List[str]):
        futures = []
        for url in urls:
            future = workflow.execute_activity(
                index_document,
                IndexDocumentsParams(url),
                start_to_close_timeout=timedelta(seconds=60),
            )
            futures.append(future)
        results = await asyncio.gather(*futures)
        indexed_pages = sum(results)
        logger.info(f"Indexed {len(urls)} documents totaling {indexed_pages} pages")
        return indexed_pages
