from datetime import timedelta
from typing import List

from temporalio import workflow

# Required to import activities, which contain non-deterministic code
with workflow.unsafe.imports_passed_through():
    from temporal.activities import IndexDocumentsParams, index_document


@workflow.defn(name="IndexDocumentsWorkflow")
class IndexDocumentsWorkflow:
    @workflow.run
    async def run(self, urls: List[str]):
        for url in urls:
            await workflow.execute_activity(
                index_document,
                IndexDocumentsParams(url),
                start_to_close_timeout=timedelta(seconds=60),
            )
