# FactClash: What It Does and What Comes Next

| Field | Value |
| --- | --- |
| Date | 2026-11-21, updated 2026-11-25 and 2026-11-28 |
| Author(s) | mahyar |
| Status | Draft |

## 1. Where the code is today

- **API:** a FastAPI app with one endpoint, `POST /api/v1/contradictions/nlp`. It validates the request (context blocks with their sources) and returns an analysis per block.
- **Analyzer:** `NLPAnalyzer` sits behind the abstract `ContradictionAnalyzer` and an analyzer registry. It returns a fixed answer (`CONTRARY`, confidence 0.999). No detection runs yet.
- **Domain model in code:** `Source` (with a reliability score), `Fact` (subject, statement, scope, validity window, evidence, fingerprint), `Evidence`, `Hypothesis`, `Premise` and a fact status history, following [reasoning.md](../domain-model/entities/reasoning.md).
- **spaCy:** added, on `en_core_web_md` (switched from `en_core_web_sm` on 2026-11-28 for its word vectors). `adapters/claim_extraction/spacy_extractor.py` explores noun phrases, numbers and subjects but is not wired into the API yet. `api/nlp_model.py` loads the model once per process with `functools.lru_cache`.
- **Tooling:** uv, ruff and ty in pre-commit, pytest unit and integration tests.
- **Code layout:** since 2026-11-24 (CD-37) the code sits in the layer layout of [overview.md](../solution-architecture-documents/overview.md): `core/`, `services/`, `adapters/`, `api/`.

## 2. What FactClash is

FactClash is a context guard that learns. It watches what goes into an LLM, catches sources that contradict each other, decides which one to trust, keeps the verified facts as a graph that RAG can retrieve from, and gets cheaper over time as a small model learns from its LLM judge's decisions.

It works in four stages. Each stage ships as its own release, with its own numbers.

### 2.1 Watch: detect clashes

- **In:** the context about to be sent to an LLM, as passages plus their source details.
- **Steps:** check each sentence of each passage and skip the ones the rules can't read reliably (fragments, no subject, a pronoun with nothing earlier in the passage to point to, text cut mid-sentence, noisy text), recording why → turn the rest into claims (what it is about, what it says, any value, whether it is negated, and the condition of "if X then Y" claims) with spaCy rules → pair only the claims that talk about the same thing → screen each pair with rules (quantities, simple strict contradictions) → flag the pairs that clash.
- **What a claim is:** the smallest piece of text that can be true or false on its own and that another text could contradict. It can be plain ("The cluster runs 3 replicas.") or conditional ("If traffic spikes, the cluster scales to 10."). Sentences that are not claims (greetings, questions, commands, hedges such as "might be running") stay with a claim as supporting text. A claim is not yet a Hypothesis: a Hypothesis is made from a claim when a clash is flagged.
- **Same thing, by meaning:** pairing decides whether two claims are about the same thing by meaning, not by exact wording. It must still keep apart words that look alike but mean different things in a domain ("shall" / "should", "flammable" / "combustible").
- **Why check sentences first:** FactClash gets passages, not whole documents, cut by someone else's retriever, parser or scraper. A wrong claim creates false clashes, so a sentence the rules can't read gives no claim, and the skip counts show when a costlier fallback is worth it.
- **Why pair first:** checking every passage against every other grows quadratically. 20 passages already make 190 pairs [2].
- **Out:** the API answers without the clash. Each flagged clash sets the flag on its Hypothesis and leaves one monitor record: the two claims, their sources, the clash type, the score and how long each stage took.

### 2.2 Resolve: decide which side to trust

- Pairs the screener is unsure about go to an LLM judge that can look things up (the source passage, facts already stored) before it makes the final call.
- The judge separates three cases: a real contradiction; an update, where the value changed over time (`Fact.valid_from`, `Fact.valid_until`); and a conditional statement, where both are true in different scopes (`Fact.scope`).
- For a real contradiction it picks the side to trust from provenance and records why, as a Hypothesis with its Premises and Evidence. Provenance means source reliability, recency and supporting evidence. Source reliability is set by the caller, for example the score their own retrieval system gives a source.
- Nothing is deleted silently. The losing side is marked with the reason and stays reviewable. Silent deletion is a reported failure of LLM-driven memory updates [4].
- Every judge decision is stored. These decisions are the training data for stage 4.
- The strict screener gains an NLI model in this release, measured against the rules version.

### 2.3 Remember: a graph of verified facts

- Context, facts, premises, hypotheses and judge decisions are stored in PostgreSQL. pgvector finds entries that mean the same thing, which drives de-duplication, recurring-clash detection, the candidate pairs in 2.1, and similarity retrieval.
- In parallel, verified facts are written to a graph in Neo4j: entity, attribute, value, source, valid from and until. This is the GraphRAG a customer's RAG retrieves from, through an HTTP endpoint and an MCP tool.
- A small GraphRAG demo client answers the same questions with and without the verified graph, so the difference can be measured.

### 2.4 Learn: get cheaper over time

- FactClash runs a cascade. Each case goes to the cheapest model that can handle it, and only what that model is unsure about moves up a tier: rules → small task models (a spaCy NER model for domain entities, a classifier for the clash type) → a small LLM for cases that need reasoning → the large LLM judge.
- The large LLM's decisions are the labels. Each smaller model is fine-tuned on them and re-checked after every update on a fixed, human-labelled held-out set.
- A tier is added only when the numbers show the tier below fails on a slice large enough to matter. The first one built is the clash-type classifier, because the judge's decisions give it clean labels.
- Success means the same accuracy with lower cost per 1,000 requests and lower latency. The share of cases each tier handles is reported over time. Small fine-tuned models already do hallucination detection at a fraction of an LLM judge's cost [6][7][9].

### 2.5 Measure

Every release reports its numbers in the README: detection precision, recall and F1 on public benchmarks; agreement with human labels for resolution; p50 and p95 latency; cost per 1,000 requests; and, from stage 4 on, the small model's learning curve against the judge.

## 3. Prior art and what is different

| Project | What it does | How FactClash differs |
| --- | --- | --- |
| Graphiti (Zep) [1] | Temporal knowledge graph for agent memory. When a new fact conflicts with an old one, an LLM call per new edge invalidates the older edge and keeps its history. | Does not assume the newer fact wins: weighs reliability, recency and evidence, and records why. Runs cheap rules first and calls the LLM only for unsure pairs. Monitor-first, with measured detection numbers. |
| Mem0 [3][4] | Memory layer for agents. Has used an LLM ADD / UPDATE / DELETE step to reconcile new facts with stored ones. | Never deletes. Every decision keeps its evidence and reason. |
| Research: ConflictRAG [5], LLMs as context validators [2], MAGIC [8] | Methods and benchmarks for conflicts between retrieved documents. Current models are still weak at this, especially across multiple hops. | An open-source service with a monitor, a store and published numbers. |
| HHEM [9], Luna [6] | Small models that check an LLM's answer against its sources. | FactClash checks sources against each other before the LLM sees them, and its small model keeps learning from its own judge. |

A first search (2026-11-21) found no packaged open-source tool that does all three: detect conflicts between sources before generation, resolve them with a recorded reason, and get cheaper over time.

## 4. Releases and next steps

### v0.1.0 Watch

| # | When this is done, the code… | Size | Ticket |
| --- | --- | --- | --- |
| 0 | sits in the layer layout from [overview.md](../solution-architecture-documents/overview.md), with no change in behaviour and all tests green | S | CD-37 |
| 1 | turns each passage of a request into claims (what it is about, what it says, any value, negation, the condition of if-then claims, the supporting sentences around them, its source) with spaCy rules, tested on the spec examples | M | CD-30 |
| 1b | skips the sentences the rules can't read reliably and says why, so the skip rate per reason can be counted | S | CD-38 |
| 2 | pairs only the claims about the same thing, judged by meaning rather than exact wording, instead of every claim with every other | M | CD-31 |
| 3 | flags quantity clashes ("3 replicas" vs "5 replicas") with a score | M | CD-9 |
| 4 | flags strict contradictions ("running" vs "not running") with rules and a score | M | CD-4 |
| 5 | runs the screener behind the endpoint, sets the flag on the Hypothesis and writes one monitor record per clash, with per-stage latency | M | CD-21, CD-22 |
| 6 | prints precision, recall and F1 on a public benchmark with one command | M | CD-10, CD-11 |
| 7 | runs lint and tests on every push, builds a Docker image, serves the API from a cloud URL, and is tagged v0.1.0 | L | CD-13, CD-16, CD-29, CD-14 |

### v0.2.0 Resolve and store

LLM judge with tools (CD-23) that survives LLM failures (CD-25); contradiction vs update vs conditional; the side to trust, with a recorded reason; routing threshold between the screener and the judge; cost per request (CD-26); PostgreSQL store with pgvector (CD-27, CD-28); NLI model in the strict screener (CD-35).

### v0.3.0 Remember

Model and domain on each request (CD-18), domain entities that the stock spaCy model misses (CD-36), verified-fact graph in Neo4j (CD-32), retrieval over HTTP and MCP (CD-24), GraphRAG demo client with before-and-after numbers (CD-33).

### v0.4.0 Learn

The small spaCy model learns online from stored judge decisions and takes the pairs it is confident about; learning curve, cost and latency before and after (CD-34).

## 5. Not before v0.1.0

LLM judge, NLI model, PostgreSQL store, Neo4j graph, MCP, online learning, authentication, a UI or dashboard, languages other than English.

## 6. Decisions and open questions

### Decisions (2026-11-21, 3 updated and 9–11 added 2026-11-25, 12 added 2026-11-28)

1. **Release order:** Watch ships first. The judge and the store come in the next release.
2. **Models:** a cascade from cheap to expensive: rules, small task models (spaCy NER, a clash-type classifier), a small LLM for reasoning cases, and the large LLM judge. The smaller models learn from the judge's decisions. A tier is added only when measurements show the one below falls short.
3. **Claim extraction:** spaCy rules first, then the small model. Each sentence is checked before extraction; sentences the rules can't read reliably are skipped with a reason and counted. An LLM fallback for skipped sentences (restore punctuation and grammar, then parse again; or ask one multiple-choice question about the ambiguous part) comes with the judge in v0.2.0, if the skip counts show it is needed. The LLM monitors and makes the final call, and its decisions train the small model.
4. **Strict screener:** rules for simple cases first, an NLI model next.
5. **Evaluation:** well-known public benchmarks, chosen after research, plus the small model's learning curve over time.
6. **Storage:** PostgreSQL with pgvector for context, facts, premises, hypotheses and similarity retrieval. In parallel, a GraphRAG over verified facts in Neo4j.
7. **Source reliability:** set by the caller from data they already have, such as their retrieval system's score. FactClash uses it to weight its decisions.
8. **GraphRAG demo client:** in scope.
9. **Claims:** plain and conditional claims both in v0.1.0. A claim records negation. Claim is its own type; a Hypothesis is made from a claim when a clash is flagged.
10. **Same subject:** decided by meaning in v0.1.0 (CD-31), not by text rules, because text rules have too many edge cases.
11. **Sentence checks:** the checks that need no number (root is not a verb, no subject, pronoun subject with nothing before it, cut mid-sentence, words the parser couldn't classify) and the ones with a threshold (sentence length, share of lowercase letters, out-of-vocabulary rate). Thresholds come from measurement, never from a guess.
12. **spaCy model:** `en_core_web_md` from CD-30 on, replacing `en_core_web_sm`, because `sm` ships no word vectors and the claim tests use a similarity check. Whether `md`'s vectors are good enough for matching claims by meaning is still measured in CD-31.

### Still open

- Which benchmarks (CD-10)?
- Online learning: how does the small model avoid losing what it learned earlier as it updates (known as catastrophic forgetting), and how often is it re-checked on the held-out set?
- PostgreSQL and Neo4j: which one is the source of truth for a fact, and how do they stay in sync?
- Callers report reliability on different scales. How are their scores made comparable?
- When is the small model confident enough to take a pair without the LLM?
- Which tiers earn their place: does the classifier leave enough hard cases to justify a small LLM?
- Gate thresholds (sentence length, share of lowercase letters, unclassified words): CD-38's starting values come from a handful of passages. What are they on real data (CD-10's dataset)?
- The out-of-vocabulary check needs word vectors, which `en_core_web_md` has (decision 12). Which out-of-vocabulary rate counts as too high? (CD-38's measurement.)
- Is `en_core_web_md` good enough for matching claims by meaning (CD-31), or does it need the large model or a sentence-embedding model? To be measured on pairs that look alike but must stay apart ("shall" / "should", "flammable" / "combustible", "is running" / "is not running").
- Beam-search NER: worth configuring when we train our own NER (CD-36, v0.3.0), so the gate can use entity confidence?
- Pronoun subjects ("It must be renewed every 90 days."): a single passage can't say what "it" is, so v0.1.0 skips them. Could a request carry the passage before it?

## 7. References

1. Graphiti: https://github.com/getzep/graphiti · temporal model: https://mintlify.com/getzep/graphiti/concepts/temporal-model
2. Contradiction Detection in RAG Systems: Evaluating LLMs as Context Validators for Improved Information Consistency: https://arxiv.org/abs/2504.00180
3. Mem0, custom update memory prompt: https://docs.mem0.ai/open-source/features/custom-update-memory-prompt
4. "Mem0 auto-resolves memory conflicts for you until it silently deletes one you still need" (one author's report): https://dev.to/mukesh_13/mem0-auto-resolves-memory-conflicts-for-you-until-it-silently-deletes-one-you-still-need-4f4m
5. ConflictRAG: https://arxiv.org/abs/2605.17301
6. Luna: https://arxiv.org/abs/2406.00975
7. HalluGuard: https://arxiv.org/html/2510.00880
8. MAGIC: A Multi-Hop and Graph-Based Benchmark for Inter-Context Conflicts in RAG: https://arxiv.org/abs/2507.21544
9. Vectara HHEM: https://huggingface.co/vectara/hallucination_evaluation_model
