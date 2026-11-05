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

For more information about the type of contradictions, read  [contradictions.md](docs/factclash/domain-model/cross-cutting/contradictions.md).

## Failure Modes

- `Confirmation Bias`: Models demonstrate a systematic preference for external evidence that corroborates their internal parametric priors.
- `Sycophancy and False Premise Acceptance`: Instruction tuning aligns models to follow user intent, making them highly vulnerable to user-induced prompt contradictions. When a user prompt introduces a false premise or a biased hint, models frequently abandon parametric truth to agree with the user.
- `Blindness to Generated Context`: In multi-step generation or agentic workflows, LLMs treat their own previously generated hallucinatory outputs as valid contextual truth. When retrieved factual contexts conflict with model-generated contexts, LLMs struggle to disentangle the two, frequently prioritizing their own synthetic output over reliable external data.

## Usage
```bash
uv run factclash
```
