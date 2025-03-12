from app.main import index_documents, query_model


def test_end_to_end(test_document_url, reset_vector_store):
    indexed_pages = index_documents([test_document_url])
    assert indexed_pages == 1
    response = query_model("What was Apple's earnings per share in 2021?")
    assert "5.67" in response
