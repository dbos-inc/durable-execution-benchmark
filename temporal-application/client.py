import asyncio

from temporalio.client import Client

from temporal.temporal import IndexDocumentsWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        IndexDocumentsWorkflow.run,
        "your name",
        id="your-workflow-id",
        task_queue="your-task-queue",
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
