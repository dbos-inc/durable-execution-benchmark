import os

import pytest
from sqlalchemy import create_engine, text


@pytest.fixture()
def test_document_url():
    return "https://dbos-blog-posts.s3.us-west-1.amazonaws.com/durable-execution-benchmark/apple-2021.pdf"


@pytest.fixture
def reset_vector_store():
    engine = create_engine(os.environ.get("TEMPORAL_DATABASE_URL"))
    with engine.connect() as connection:
        connection.execute(text("TRUNCATE TABLE data_llamaindex"))
        connection.commit()
