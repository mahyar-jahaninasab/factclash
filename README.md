# FactClash

## Overview
`factclash` is python library that functions just before feeding the retrieval information to the LLM for the final call. It recognizes which facts are contradictory to each other and can cause LLM to hallucinate. FactClash comes in the middle it first detects if contradictory facts exist inside the context. 

## How it helps 
The main three source of contradictions are: 
- Fault recording and human error while documenting a specific task. 
- Change of policy within a company. For instance in a certain timestamp the policy of the company was X but now it turned into Y for some certain conditions 
- Retrieval Error: The retrieval mechanism actually retrieved False information that can potentially cause contradiction with True information that is retrieved. 

## Quick start

```shell
#Clone
git clone https://github.com/mahyar-jahaninasab/factclash.git

# Install dependencies
uv sync --dev

# Run tests
uv run pytest tests/

```

## Development 

```shell
uvx pre-commit install
uvx pre-commit run

```


## Status

The project is in the initial phase. 


## Types of contradiciton

For more information about the type of contradictions, read [docs/contradictions.md](docs/contradictions.md).

## Usage 
```bash
uv run factclash
```
### Example 

#### Request 
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/contradictions/nlp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
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
  ```

#### Response 

```bash
{
  "blocks": [
    {
      "contradiction_type": "CONTRARY",
      "analyzer": "NLP",
      "confidence": 0.999,
      "metadata": null,
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
```

## v0 scope 

In scope: ``Strict Contraction`` and ``Quantification Contradiction`` as they can be fully automated using standard NLP

Out Scope: 
- ``hybrid pipeline`` : Temporal Contradiction and Contrary Contradiction
- ``Need LLM``: Lexical Contradiction and Pragmatic Contradiction

For the input and output of the system check [spec](docs/spec.md)

### Later

- partitioning
- input format: json, md, 
- output format: JSON

