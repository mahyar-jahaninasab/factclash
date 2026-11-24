# FactClash: Solution Architecture Overview

| Field | Value |
| --- | --- |
| Date | 2026-11-21 |
| Author(s) | mahyar |
| Status | Draft |

## 1. Context

FactClash sits between an application that builds context for an LLM and the LLM itself.

- **Caller:** an application that retrieves passages (a RAG pipeline or an agent). It sends them to FactClash before its LLM call, with each source's details and reliability score.
- **The caller's LLM:** receives the context. FactClash never calls it. (FactClash's own LLM judge, from v0.2.0, is a separate model.)
- **Monitor output:** one JSON log line per flagged clash in v0.1.0. The store is added in v0.2.0.
- **Later:** an LLM provider for the judge (v0.2.0), PostgreSQL with pgvector (v0.2.0), Neo4j (v0.3.0).

## 2. Package layout

Code is grouped by layer, following Architecture Patterns with Python (where `core/` is called the domain and `api/` an entrypoint). Dependencies point inward: `api/` → `services/` → `core/` ← `adapters/`. Inside a layer, each feature gets its own subfolder once it has code there (for example `adapters/claim_extraction/`).

```
src/factclash/
├── core/        entities, business rules, interfaces
├── services/    use cases
├── adapters/    implementations that talk to the outside world
└── api/         the FastAPI app (later cli/ and mcp/ beside it)
```

| Package | Holds | First used |
| --- | --- | --- |
| `core/` | Entities and value types (Source, Fact, Evidence, Hypothesis, Premise, status records, Claim, Clash); business rules that need no outside library (the rule-based screeners; pairing, apart from its meaning check, see §3); and the interfaces the outer layers implement: claim extractor, screener, monitor, store, judge | v0.1.0 |
| `services/` | Use cases, one per thing FactClash does: check a context (v0.1.0), resolve unsure pairs (v0.2.0), store and retrieve facts (v0.2.0, v0.3.0), train a cheaper tier (v0.4.0). Each receives its adapters through the interfaces in `core/`. | v0.1.0 |
| `adapters/` | Implementations that talk to the outside world: spaCy claim extractor, JSON log monitor, NLI screener (v0.2.0), LLM judge client (v0.2.0), PostgreSQL store with pgvector (v0.2.0), Neo4j fact graph (v0.3.0), model training (v0.4.0) | v0.1.0 |
| `api/` | The FastAPI app, routes, the dependencies that choose which adapters to plug in, and the API's request and response schemas | v0.1.0 |
| `cli/`, `mcp/` | Other ways in, with the same job as `api/`: the evaluation command (CD-11) and the MCP server (CD-24) | later |

### Rules

- `core/` imports nothing else from FactClash, and nothing from FastAPI, spaCy or database libraries.
- `services/` imports only `core/`. It never names a concrete adapter.
- `adapters/` import `core/` to implement its interfaces, plus their own external library.
- `api/` (and later `cli/`, `mcp/`) wires everything together: it builds the adapters, passes them to the services, and converts between API schemas and `core/` objects. API schemas never reach `core/`.
- Every interface in `core/` has a fake for tests (Architecture Patterns, ch. 2).

## 3. Components

| Component | Where | Job | In | Out |
| --- | --- | --- | --- | --- |
| API | `api/` | Validates the request, converts it to domain objects, calls the use case, answers the caller | HTTP request | HTTP response without the clash |
| Check-a-context use case | `services/` | Runs extraction, pairing, screening and monitoring for one request; from v0.2.0 also sends unsure pairs to the judge | Domain context | Hypotheses with flags |
| Claim extractor | interface in `core/`, spaCy version in `adapters/` | Checks each sentence, skips the ones its rules can't read reliably with a reason, and turns the rest into claims (plain and conditional); from v0.2.0, skipped sentences can go to an LLM fallback | Passages with sources | Claims, skipped sentences with reasons |
| Pairing | `core/`; the meaning check needs a model, and where that model sits is decided in CD-31 | Pairs only the claims about the same thing, judged by meaning rather than exact wording | Claims | Candidate pairs |
| Screeners | interface and rule-based screeners in `core/`; NLI screener in `adapters/` (v0.2.0) | One strategy per kind of clash, all behind one interface. Each pair goes through each screener. | Candidate pairs | Clash type and score per pair |
| Monitor | interface in `core/`, JSON log version in `adapters/` | Records each flagged clash | Flagged clash | One JSON log line |
| Judge | interface in `core/`, LLM client in `adapters/` (v0.2.0) | Makes the final call on pairs the screeners are unsure about | Unsure pairs | Decision with a reason |
| Store | interface in `core/`, PostgreSQL with pgvector in `adapters/` (v0.2.0) | Keeps context, facts, premises, hypotheses and judge decisions; finds entries that mean the same thing | Domain objects | Stored records, similar entries |
| Fact graph | `adapters/` (v0.3.0) | Holds verified facts as a graph for GraphRAG | Verified facts | Graph queries |
| Learner | use case in `services/`, trainer in `adapters/` (v0.4.0) | Trains the cheaper tiers on judge decisions | Judge decisions | Models that take over confident cases |

## 4. One request, end to end (v0.1.0)

Two retrieved passages: source A says "The cluster runs 3 replicas." and source B says "The cluster runs 5 replicas."

1. The caller sends both passages with their sources to the API (today `POST /api/v1/contradictions/nlp`).
2. `api/` validates the request against the API schemas, converts it into domain objects, builds the adapters (spaCy claim extractor, JSON log monitor) and calls the check-a-context use case in `services/`.
3. The use case asks the claim extractor for claims. Both sentences pass the sentence check, so nothing is skipped, and it returns two claims: cluster, replicas, 3, from A; and cluster, replicas, 5, from B.
4. Pairing in `core/` sees the same subject and makes one candidate pair.
5. The quantity screener sees the same subject and attribute with different numbers and flags a clash with a score. The strict screener has nothing to say.
6. The clash's Hypothesis gets its flag. The use case hands the clash to the monitor, which writes one JSON log line with both claims, their sources, the clash type, the score and the time each step took.
7. The API answers without the clash.

From v0.2.0, the use case sends pairs the screeners are unsure about to the judge, and stores the judge's decision, both through their interfaces in `core/`.

## 5. From the old code to this layout

Done in CD-37 (2026-11-24), files moved with no behaviour change:

| Before | Now |
| --- | --- |
| `app/main.py` | `api/main.py` |
| `contradictions/router.py`, `dependencies.py`, `schemas.py` | `api/router.py`, `api/dependencies.py`, `api/schemas.py` |
| `domain/schemas.py`, `domain/helpers.py` | `core/models.py`, `core/helpers.py` |
| `domain/dependencies.py` (loads the spaCy model) | `api/nlp_model.py` |
| `services/analyzer/preprocessor.py` | `adapters/claim_extraction/spacy_extractor.py` |

Still to move:

| Today | Moves to |
| --- | --- |
| `services/analyzer/base.py` (analyzer interface, registry) | `core/` as the screener interface, once it no longer imports the API schemas |
| `services/analyzer/nlp_based.py` (`NLPAnalyzer`, fixed answer) | replaced by the screeners (CD-9, CD-4) |

## 6. Related documents

- [next-steps.md](../functional-requirements/next-steps.md): what FactClash does and the release plan
- [ADR-0001](../decision-records/ADR-0001.md): hybrid NLP and LLM architecture
- [ADR-0002](../decision-records/ADR-0002.md): hybrid NLI pipeline
- [reasoning.md](../domain-model/entities/reasoning.md): the reasoning entities
- [contradictions.md](../domain-model/cross-cutting/contradictions.md): contradiction types
- [spec.md](../functional-requirements/spec.md): input, detection and output
