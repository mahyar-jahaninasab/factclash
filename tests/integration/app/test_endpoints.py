import pytest
from fastapi.testclient import TestClient
from fastapi import status
from factclash import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello I am confused, these facts don't make sense"}

def test_nlp_endpoint_happy_path():
    response = client.post(
        "/api/v1/contradictions/nlp",
        json={
            "blocks": [
                {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "metadata": {
                    "description": "The retrived doc discusses operational timing of the facility",
                    "id": "operational",
                    "prompt": "find me facility operations I was told it is three days a week",
                    "provider": "rag",
                    "score": 0.25
                },
                "passages": [
                    "The facility operates 24 hours a day, 7 days a week.",
                    "The facility closes at 6:00 PM every evening."
                ],
                "source_type": "retrieval"
                }
            ]
            }
                           )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
                                "blocks": [
                                    {
                                    "contradiction_type": "CONTRARY",
                                    "analyzer": "NLP",
                                    "confidence": 0.999,
                                    "metadata": None,
                                    "context_block": {
                                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                        "source_type": "retrieval",
                                        "passages": [
                                        "The facility operates 24 hours a day, 7 days a week.",
                                        "The facility closes at 6:00 PM every evening."
                                        ],
                                        "metadata": {
                                        "id": "operational",
                                        "description": "The retrived doc discusses operational timing of the facility",
                                        "score": 0.25,
                                        "prompt": "find me facility operations I was told it is three days a week",
                                        "provider": "rag"
                                        }
                                    }
                                    }
                                ]
                                }


def test_nlp_endpoint_wrong_context_type():
    response = client.post(
        "/api/v1/contradictions/nlp",
        json={
            "blocks": [
                {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "metadata": {
                    "description": "The retrived doc discusses operational timing of the facility",
                    "id": "operational",
                    "prompt": "find me facility operations I was told it is three days a week",
                    "provider": "rag",
                    "score": 0.25
                },
                "passages": 
                    "The facility operates 24 hours a day, 7 days a week. The facility closes at 6:00 PM every evening."
                ,
                "source_type": "retrieval"
                }
            ]
            }
                           )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_nlp_endpoint_wrong_field_name():
    response = client.post(
        "/api/v1/contradictions/nlp",
        json={
            "blocks": [
                {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "metadata": {
                    "description": "The retrived doc discusses operational timing of the facility",
                    "id": "operational",
                    "prompt": "find me facility operations I was told it is three days a week",
                    "provider": "rag",
                    "score": 0.25
                },
                "passages": 
                    ["The facility operates 24 hours a day, 7 days a week. The facility closes at 6:00 PM every evening."]
                ,
                "source_types": "retrieval"
                }
            ]
            }
                           )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT



def test_nlp_endpoint_wrong_enum_value():
    response = client.post(
        "/api/v1/contradictions/nlp",
        json={
            "blocks": [
                {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "metadata": {
                    "description": "The retrived doc discusses operational timing of the facility",
                    "id": "operational",
                    "prompt": "find me facility operations I was told it is three days a week",
                    "provider": "rag",
                    "score": 0.25
                },
                "passages": 
                    ["The facility operates 24 hours a day, 7 days a week. The facility closes at 6:00 PM every evening."]
                ,
                "source_type": "known"
                }
            ]
            }
                           )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_nlp_endpoint_wrong_input():
    response = client.post(
        "/api/v1/contradictions/nlp",
        json= "The facility operates 24 hours a day, 7 days a week. The facility closes at 6:00 PM every evening.")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT