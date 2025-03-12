# Reference Application

This is a reference implementation of the document indexing application with no durable execution.

Required environment variables:

- `OPENAI_API_KEY`: An OpenAI API key
- `TEMPORAL_DATABASE_URL`: Connection string for a Postgres database

To run:

```shell
uv sync
uv run fastapi run app/main.py
```

To test:

```shell
uv run pytest
```

To ingest some data (Apple 10-K filings for 2021-2023):

```
curl -X POST "http://localhost:8000/index" \
     -H "Content-Type: application/json" \
     -d '{"urls": ["https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/faab4555-c69b-438a-aaf7-e09305f87ca3.pdf", "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/b4266e40-1de6-4a34-9dfb-8632b8bd57e0.pdf", "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/42ede86f-6518-450f-bc88-60211bf39c6d.pdf"]}'
```

To query ingested data:

```
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What were Apple earnings per share in 2021?"}'
```