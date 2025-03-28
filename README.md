# Durable Execution Benchmark

This repository compares what is required to add durable execution to a reference application using both [DBOS](https://dbos.dev) and [Temporal](https://temporal.io).

The reference application is a document indexing pipeline based loosely on LlamaIndex's [SEC Insights](https://github.com/run-llama/sec-insights) application.
It ingests and indexes documents, then provides Retrieval Augmented Generation (RAG)-based querying of those documents.
For example, it can ingest a company's SEC filings for some years then accurately answer detailed questions about the company's financial performance during that time.
Because the application can ingest many documents concurrently and because each document takes a long time to ingest, it greatly benefits from durable execution to ensure that it correctly ingests all requested documents.

This repository contains three implementations of the application.

- A [reference implementation](./reference-application) without any durable execution.
- An [implementation using DBOS](./dbos-application) for durable execution.
- An [implementation using Temporal](./temporal-application) for durable execution.

Each implementation's README contains notes on how to run and test it.

Comparing the implementations, we find adding durable execution with DBOS requires ~10x less code than adding durable execution with Temporal.
- The reference implementation is 110 lines of code.
- Adding durable execution with DBOS requires adding or changing 7 lines of code.
It does not change how the application is operated.
The total size of the DBOS implementation is 113 lines of code.
- Adding durable execution with Temporal requires adding or changing >100 lines of code.
It also requires rearchitecting the application into two separate services (a Temporal worker and an API server) and adding a runtime dependency on a third service, the Temporal Server.
The total size of the Temporal implementation is 187 lines of code.

All three implementations use Postgres with pgvector as a vector store.
If you have Docker, you can start Postgres with:

```shell
python3 start_postgres_docker.py
```