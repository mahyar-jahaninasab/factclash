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

