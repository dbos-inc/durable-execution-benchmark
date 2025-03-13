# Durable Execution Benchmark

This repository compares what is required to add durable execution to an existing application using both [DBOS](https://dbos.dev) and [Temporal](https://temporal.io).

The reference application is a document indexing pipeline based loosely on LlamaIndex's [SEC Insights](https://github.com/run-llama/sec-insights) application.
It ingests and indexes documents, then provides Retrieval Augmented Generation (RAG)-based querying of those documents.
For example, it can ingest Apple's SEC 10-K filings from 2021-2023 then accurately answer detailed questions about Apple's financial performance during that time.
Because the application can ingest many document concurrently and because each document takes a long time to ingest, it greatly benefits from durable execution to ensure that it correctly ingests all requested documents.

This repository contains three implementations of the application.

- A [reference implementation](./reference-application/README.md) without any durable execution.
- An [implementation using DBOS](./dbos-application/README.md) for durable execution.
- An [implementation using Temporal](./dbos-application/README.md) for durable execution.

Each implementation's README contains detailed notes on how to run and test it.

Upon comparing the implementations, we found adding durable execution with DBOS requires ~10x less code than adding durable execution with Temporal.
- The reference implementation is 111 lines of code.
- Adding durable execution with DBOS required adding or changing 7 lines of code.
It required no change in how the application is operated.
The total size of the DBOS implementation is 114 lines of code.
- Adding durable execution with Temporal required adding or changing >100 lines of code.
It also required rearchitecting the application into two separate services (a Temporal worker and an API server) and adding a runtime dependency on a third service, the Temporal Service.
The total size of the Temporal implementation is 192 lines of code.

All three implementations require Postgres with pgvector (as LlamaIndex's vector store).
If you have Docker, you can start Postgres with:


```shell
python3 start_postgres_docker.py
```