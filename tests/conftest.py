import pytest 


@pytest.fixture
def sample_input():
    "Provide a sample for the endpoint test"
    return {
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
               