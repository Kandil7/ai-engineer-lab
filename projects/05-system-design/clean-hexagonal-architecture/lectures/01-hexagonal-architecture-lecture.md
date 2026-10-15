# Lecture 01: Clean and Hexagonal Architecture for AI Systems

## Topic Overview

Most AI prototypes start as one script that loads a model, chunks documents,
calls an embedding endpoint, queries a vector store, and prints an answer.
That script is fast to write and painful to keep. The week the model name
changes, the vector store moves from local to hosted, or evaluation needs a
second retriever, every function has to change because domain logic, model
calls, and infrastructure clients were never separated. Clean and hexagonal
architecture fixes this with a simple rule: the domain and application layers
depend inward only, outward details live in adapters, and the two sides meet
at ports defined where they are used. This lecture teaches that shape on an
Islamic-corpus RAG system that answers questions over classical texts with
citations, chunking choices, and experiment tracking. It works one use case,
AnswerQuestion, end to end against two interchangeable retrievers, maps SOLID
to concrete code, names the patterns that recur, treats pipelines as explicit
lists of steps, isolates configuration at a single seam, and ends with the
model and store decisions you will actually face.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Python dataclasses, type hints, and Protocols; familiarity
with embeddings and vector search at a conceptual level; no GPU, network, or
hosted vector store required

Read sections one through three in order because each builds the vocabulary
the next assumes. Sections four through seven can then be read in any order
by experienced readers, though first-time readers should keep the printed
order. Section eight explains the test split that lets every claim run
offline. Section nine says when to ignore all of this and keep the script
flat. Section ten turns the worked example into thirteen named stack calls
with doors marked. Keep the glossary and the exercise open beside the text
and run the checker after section three to see the rules catch each shape.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Draw** the four layers and state the inward-only dependency rule without hedging
2. **Define** ports as Protocols in the inner layers and place seven RAG ports correctly
3. **Run** the AnswerQuestion use case against an in-memory fake and a simulated Qdrant adapter with identical results
4. **Apply** each SOLID principle to a concrete before and after in this codebase
5. **Select** the right pattern from eleven triggers without over-engineering
6. **Express** feature, training, and inference work as explicit named pipeline step lists
7. **Isolate** configuration at one typed seam and spot hardcoded model names as layering violations
8. **Test** each layer separately with domain tests that need no GPU, network, or vector store
9. **Decide** when a flat script is the right call and name the failure modes of premature layering
10. **Defend** thirteen stack decisions with a recommendation, an alternative, and a one-way versus two-way door call

---

## Key Concepts

### 1. Four Layers and the Inward-Only Dependency Rule

The system has four layers. Domain holds entities, value objects, and
policies with no framework imports. Application holds use cases and the port
Protocols they need. Infrastructure holds driven adapters that implement
those ports plus configuration builders. Interfaces holds driving adapters
such as HTTP handlers and CLIs that call inward.

The rule is one sentence: dependencies point inward only. Domain depends on
nothing. Application depends on domain. Infrastructure depends on application
and domain. Interfaces depend inward toward application. Nothing inner names
anything outer.

Consider a citation rule. It says an answer with no supporting passage must
be refused, and an answer with support must carry verse-level references. That
rule belongs in the domain because it is true whether the passages came from
memory, Qdrant, or a future store. If the rule instead lives inside the HTTP
handler, a second caller such as the evaluation script reimplements it or
skips it. If it lives inside the Qdrant adapter, switching stores deletes the
rule. Placement is the architecture.

A quick litmus test catches violations. Open any file in domain or
application and read its imports. If you see torch, qdrant_client, fastapi,
sqlalchemy, transformers, numpy, or requests, the layer is breached. Those
are outer details. The inner layers may use dataclasses, typing, abc, enum,
and the standard library. Everything else arrives through a port.

The payoff is substitution. Because the use case depends on a Retriever port
rather than a Qdrant client, tests, evaluation, and production can each bind
a different adapter without touching the use case. The diagram in the track
README shows the rings; this section is the rule that keeps them honest.

In practice the discipline is boring and total. New developers learn it in
one code review: if the import points outward, move the code outward or move
the abstraction inward. There is no third option.

Three review habits keep the rule alive. First, sort imports by layer in
every pull request and question any technical name in an inner file. Second,
keep a short banned list at the top of the contributing guide so torch and
store clients are rejected before discussion. Third, treat test speed as a
signal: when a domain test needs fixtures or sleeps, an outer detail has
crept inside. Fast tests are not a luxury here; they are the alarm.

The cost of violation compounds in AI work because model and store clients
are heavy. Importing torch in domain means importing a gigabyte dependency
to check a citation rule. Importing a store client in application means every
evaluation sweep starts a container. Inward-only keeps the cheap logic cheap
and pushes the heavy clients to the edge where factories can stub them.

### 2. Ports Are Protocols Defined Where They Are Used

A port is an interface the inner layer defines for its own needs. In Python
it is a typing Protocol or an abstract base class. The use case declares what
it needs; adapters conform to that shape from the outside. The port lives
with the caller, not with the implementation.

This track uses seven ports for the Islamic-corpus RAG domain. Each name
states a capability, not a product.

- Retriever returns candidate passages for a query string.
- Generator turns a query plus passages into a drafted answer.
- Tokenizer splits and normalizes text, including Arabic-aware handling.
- DocumentRepository loads and saves corpus documents by id.
- Embedder maps text to vectors.
- CitationPolicy decides whether support is sufficient and formats references.
- ExperimentTracker records runs, parameters, and metrics.

A minimal Retriever port looks like this in words: a method named retrieve
that takes a query string and a limit and returns a list of passages. An
in-memory fake implements it with a list scan. A Qdrant adapter implements it
with a client call. The use case cannot tell the difference, which is the
entire point.

Ports belong in the domain or application layer depending on who needs them.
CitationPolicy is domain because the refusal rule is domain logic. Retriever
and Generator are application because use cases orchestrate them. The file
that defines the port imports nothing technical. If a port signature mentions
torch.Tensor or a Qdrant record type, the abstraction has leaked and outer
types are now required to call inner logic.

Naming matters. Name ports after the role, not the tool. Retriever survives a
move from Qdrant to pgvector. QdrantWrapper does not. The seven names above
are stable across every decision in section ten.

Port granularity deserves care. One method per port is common for Retriever
and Generator because each has a single job. DocumentRepository is wider by
nature, with get, list, and save, but still narrower than a full database
session. When a port grows past three methods, ask whether two roles are
hiding inside. Splitting early keeps fakes small and contract tests focused.

Document the contract in words beside the signature. State the empty-input
behavior, the limit handling, the ordering guarantee, and the error shape.
The demo promises empty lists for blank queries and id-ordered ties. Those
two sentences are what let two independent adapters agree exactly. Without
them, each adapter guesses and substitution fails on edge cases first.

### 3. The AnswerQuestion Use Case End to End

AnswerQuestion is the worked example. Its inputs are a query string and a
limit. Its steps are retrieve passages, check citation policy, draft with the
generator, attach references, and record the run. It returns an answer object
with text, citations, and the passage ids used.

The use case takes its collaborators as constructor arguments typed to
ports: a Retriever, a Generator, a CitationPolicy, and an ExperimentTracker.
It never constructs them. Construction happens at the composition root where
configuration selects adapters. This separation is dependency inversion made
concrete: high-level policy depends on abstractions, and low-level details
depend on the same abstractions.

The demo runs the same use case twice. First it binds InMemoryRetriever,
which scans a small seeded list. Then it binds SimulatedQdrantRetriever,
which mimics paged dense retrieval over the same seeds with the same ranking.
Both runs receive the same query and the same limit. Both return identical
passage ids, identical text, and identical citations. The assertion is exact
equality, not similarity. Identical results prove the use case depends on the
port rather than on either adapter.

Three details make this work. First, the passage type is shared and plain: an
id, a book title, a section label, and text. Second, ranking ties are broken
deterministically by id so paging cannot reorder equals. Third, the generator
in the demo is deterministic, echoing the top passage with a fixed template,
so adapter differences cannot hide in sampling noise.

Production swaps only the binding. The HTTP handler builds the real Qdrant
adapter from typed configuration and passes it to the same class. No branch
in the use case knows which adapter is bound. That is what portable means.

Failure handling stays inside the orchestration. Empty retrieval yields a
refusal with no citations. Policy rejection yields a refusal with the reason
recorded. Generator errors map to a plain failure the tracker logs with the
passage ids already chosen. Each path is covered by an application test with
fakes, so production surprises are adapter bugs rather than logic gaps.

The tracker call is not optional decoration. It records the query hash, the
limit, the model name from config, and the returned ids. Evaluation later
joins these rows across runs to compare chunking and ranking choices. A use
case that answers without recording forces evaluation to reconstruct context
from logs. Record at the moment of decision, not after.

### 4. SOLID Through This Codebase

SOLID is often taught as slogans. Here each letter is a concrete change.

Single responsibility: one module has one reason to change. Before, a step
named chunk_and_embed splits text, calls the embedding model, and writes to
the store. A tokenizer change, a model change, and a store change all edit
the same function. After, three steps named chunk_sections, embed_texts, and
upsert_passages each own one change. The checker flags names that join two
responsibilities with and.

Open closed: extend without editing. Before, adding BM25 to a dense-only
retriever edits the retrieve method with a branch. After, a HybridRetriever
composes a dense Retriever and a sparse Retriever behind the same port and
merges by score. Callers do not change. New behavior arrives as a new class.

Liskov substitution: any adapter must satisfy its port contract. Before, a
Qdrant adapter raises on empty queries while the fake returns an empty list,
so swapping adapters changes control flow. After, both return an empty list
for empty input and document the limit contract in the port. Tests run the
same cases against every adapter.

Interface segregation: small ports beat one fat port. Before, a Store port
bundles retrieve, upsert, delete, scroll, and health into one interface, so a
read-only evaluation fake must stub writes. After, Retriever and
DocumentRepository are separate, and evaluation binds only what it needs.

Dependency inversion: use cases depend on ports. Before, AnswerQuestion
imports the Qdrant adapter class and constructs a client inside the method.
After, it accepts a Retriever and the composition root wires the adapter.
The import arrow reverses, and the use case becomes testable without a
server.

Each before and after is small on purpose. SOLID is five file-level habits,
not a rewrite.

Apply them in dependency order when cleaning a tangled module. First invert
the dependency so the use case takes ports. Then split the fat interface so
fakes shrink. Then enforce substitution with shared contract cases. Then
extract strategies for the branches that remain. Teams that start with
strategy before inversion end up with swappable classes still wired by
literals. Inversion first makes every later step easier.

A worked cleanup helps. Take a 200-line ask function that imports the store,
branches on backend names, and formats HTTP responses. Step one moves parsing
to the handler and store access behind Retriever. Step two splits ranking
from fetching. Step three replaces backend branches with a factory. The file
shrinks to forty lines of orchestration plus small adapters. No step required
a framework change.

### 5. Patterns With Triggers

Eleven patterns recur. Each has a trigger sentence that tells you when to
reach for it.

Repository triggers when documents need loading by intent rather than by
SQL. Use it when callers say get_by_id or list_by_book instead of writing
queries. It hides the store behind collection-like methods.

Strategy triggers when chunking or ranking must swap without editing the
caller. Use it when section-aware splitting and fixed-512 splitting are both
plausible. Each strategy implements one chunk method; configuration picks.

Factory triggers when construction has branches. Use it when the retriever
choice depends on configuration such as backend equals memory or qdrant.
The factory reads typed config and returns the port. Callers never branch.

Adapter triggers when an outer client must meet an inner port. Use it when
the Qdrant client returns records but the use case expects passages. The
adapter translates in one place.

Pipeline triggers when work is a repeatable sequence. Use it when ingest,
training, or evaluation runs the same steps in order. Steps are named data,
and a runner executes them.

Template Method triggers when steps share a skeleton with one varying hook.
Use it when every evaluation run needs setup, timed execution, and teardown
but only the middle differs. The base defines the order; subclasses fill the
hook.

Observer triggers when runs must notify without coupling. Use it when the
experiment tracker, logging, and metrics all need completion events. The
pipeline emits; subscribers attach.

Registry triggers when adapters must be discoverable by name. Use it when
tokenizers or retrievers grow beyond two and if-chains spread. A dictionary
maps names to constructors.

Unit of Work triggers when several writes must succeed or roll back
together. Use it when ingest writes passages and updates an alias table.
The unit commits once at the end.

Circuit Breaker triggers when a downstream call fails in bursts. Use it when
the embedding endpoint stalls and retries would amplify the outage. The
breaker opens after a threshold and fails fast until recovery.

Retry triggers when failures are transient and idempotent. Use it when a
single embedding call times out but repeating the same request is safe. Bound
attempts, back off, and add jitter; never retry a non-idempotent write.

If none of these trigger sentences is true, write the plain version. Patterns
earn their place per use.

Two cautions prevent pattern sprawl. First, do not stack patterns on one
class: a Registry-built Factory returning an Observer-decorated Strategy is
a design looking for a problem. One pattern per seam is enough until the
second trigger arrives. Second, keep pattern code near the seam it serves.
A retry helper used once belongs beside the embedding adapter, not in a
shared library with five unused options.

The exercise checks the most abused pair. Repository keeps query intent
inside the adapter; callers that pass filter dicts bypass it and should be
flagged in review. Observer keeps fan-out declarative; pipelines that import
concrete subscribers directly defeat it. Triggers plus placement decide.

### 6. Pipelines as Explicit DAGs

A pipeline is a named list of steps executed in order. Each step is a small
dataclass with a name and a function. The runner calls each function with a
shared context dictionary and records timing. There is no hidden ordering in
imports or callbacks.

Feature work uses a pipeline named build_features with steps such as
load_documents, normalize_arabic, chunk_sections, embed_texts, and
write_parquet. Training uses train_qlora with steps such as load_features,
split_train_eval, configure_lora, train, and save_adapter. Inference uses
serve_answer with steps such as parse_request, retrieve_passages,
rerank_candidates, generate_draft, and attach_citations.

Explicit lists beat implicit graphs for teams of this size. A newcomer reads
the list and knows the order. Evaluation diffs two lists. A failed run names
the step. When branching is genuinely needed, the step function returns the
next step name, which keeps the DAG visible in data rather than buried in
nested calls.

The checker enforces single responsibility at this level too. A step named
chunk_and_embed_and_rerank is three steps wearing one name. Split it. Future
changes will thank you when only one of the three needs editing.

Keep step functions pure where possible. They take the context, return an
update, and avoid global state. Impure edges such as vector-store writes sit
in exactly one step so retries and dry runs stay simple.

Name the context keys once and reuse them. Keys such as documents, chunks,
vectors, and metrics appear in every pipeline here. A short schema comment
at the top of the pipeline file lists each key and its type. New steps read
that comment before adding keys. Undocumented keys multiply until no runner
can be reasoned about.

Dry runs fall out naturally. A flag that skips steps marked as writes lets
evaluation verify ordering without side effects. Because steps are data, the
runner can list what would run, in order, with timing from the last run.
That listing is the cheapest architecture diagram the team owns.

### 7. The Config Seam

All environment-dependent choices meet in one place: a typed configuration
object built at startup from YAML plus environment overrides and validated
with Pydantic Settings style checks. The config names the model, the store
URL, chunk sizes, retrieval limits, and file paths. Adapter factories take
this object and return ports. Nothing else reads environment variables.

A hardcoded model name outside this seam is a layering violation. When
generate calls the model gpt-4o-mini by literal or when retrieval opens
http localhost port 6333 inline, three things break: tests cannot substitute
without editing, evaluation cannot sweep without branching, and review cannot
find the knobs. The checker flags literals such as model ids, http URLs, and
port numbers outside the config module.

The seam also simplifies decisions. Switching the embedding model from one
release to another edits one field and reruns evaluation. Switching the store
from Qdrant to pgvector replaces one factory branch. The use cases, ports,
and domain rules do not move.

Keep secrets out. Configuration holds names and URLs for non-sensitive
settings; credentials arrive from the environment and never appear in code or
in committed files. The absence of env files in this track is deliberate.

Validation belongs at startup, not at first use. The settings object checks
ranges for chunk sizes and limits, reachability for URLs in live mode, and
vocabulary presence for model names against an allow list. A bad value fails
fast with the field name and the valid range. Late validation turns a typo
into a midnight retrieval outage.

Defaults are documented choices, not accidents. Each field carries a comment
with the reason and the evaluation that set it. The chunk size default cites
the section-aware experiment. The limit default cites the reranker tradeoff.
Future changes update the comment with the new evidence.

### 8. Testing Layers Separately

Each layer has its own tests with its own fixtures. Domain tests cover the
citation policy, passage validation, and refusal behavior with plain objects.
They import no model, store, or web framework and run in milliseconds.

Application tests bind fakes. AnswerQuestion runs against InMemoryRetriever
and a stub generator with fixed outputs. Assertions cover passage selection,
citation attachment, refusal on empty support, and tracker calls. No GPU, no
network, no Qdrant container.

Adapter tests use recorded fixtures. The Qdrant adapter test replays a saved
response file rather than starting a server. The embedding adapter test
asserts batching and error mapping against a scripted stub. Contract tests
run the same port cases against every adapter so substitution stays honest.

Interface tests assert mapping only. The HTTP test posts a fixed payload to
the handler with a fake use case bound and checks status codes and response
shape. It never loads a model.

This separation is why the demo runs anywhere. If a domain test needs a GPU,
the layering has already failed before the test runs.

Count the layers in continuous integration to keep the split honest. Domain
and application suites run on every commit with no services. Adapter suites
run with recorded fixtures on every commit and with live services nightly.
Interface suites run with fakes on every commit. A test that needs a service
in the fast suite is moved the same day it is found.

Write contract cases once and reuse them. The retriever contract file holds
empty input, over-limit, tie order, unicode, and Arabic normalization cases.
Each adapter test imports that file and runs it. Adding a case fixes every
adapter at once, which is how substitution stays honest as the corpus grows.

### 9. Failure Modes and When a Flat Script Is Right

Layering fails in predictable ways. Over-porting creates a Protocol for every
function, including one-off helpers used once. The fix is to inline what has
one caller and promote only what has two adapters or two callers needing a
seam.

Leaky ports are the second failure. A Retriever that returns Qdrant records
forces every caller to import the client library. The fix is to translate at
the adapter edge and keep the passage type plain.

Premature adapters are the third. Wrapping a model that changes weekly behind
three indirections slows every experiment. The fix is a thin function and a
note to promote it when the second caller arrives.

Anemic use cases are the fourth. If AnswerQuestion only forwards to the
adapter without policy or orchestration, the port adds nothing. The fix is to
move the orchestration into the use case or admit the call does not need one.

A flat script is the right call when the task is a one-off exploration, a
single-file evaluation sweep with no second caller, or a spike to learn a
model API. The rule of two governs: one caller and one adapter means a
script; two callers or two adapters means a port. Start flat, extract when
the second use arrives, and keep the extraction small.

Migration has a fixed order. First add the port beside the use case without
changing behavior. Then add the fake and switch tests to it. Then move the
old code into the adapter behind the port. Then delete the direct import.
Each step is a small commit that passes the suite. Big-bang layering that
touches every file at once is how teams stall for a week.

Watch for the halfway state where the port exists but callers still import
the adapter for one method. That state is worse than no port because it pays
the abstraction cost without the substitution benefit. The checker catches
the import; review should catch the excuse. Finish the migration or revert
it the same day.

### 10. Architecture Decisions for This Stack

The table below records thirteen decisions with a recommendation, the main
alternative, the reason, and whether the door is one-way or two-way. One-way
means reversal is expensive and deserves an ADR and evaluation before
committing. Two-way means reversal is a configuration or adapter swap.

| # | Decision | Recommendation | Alternative | Reason | Door |
|---|----------|----------------|-------------|--------|------|
| 1 | Training approach | QLoRA-first on a pretrained base | From-scratch pretraining | Pretraining needs far more data and compute; adapters test the idea cheaply | One-way |
| 2 | Model scale | 50M-150M prototype, then 1B+ only if eval demands | Start at 1B+ | Small models iterate fast on 16 GB VRAM; scale on evidence | Two-way |
| 3 | Tokenizer | Bilingual 32-49K BPE trained on the corpus mix | English-only tokenizer | English vocab fragments Arabic and inflates lengths; parity needs coverage | One-way |
| 4 | Chunking | Section-aware with heading metadata | Fixed 512 tokens | Sections preserve citation units; fixed windows split verses and rulings | Two-way |
| 5 | Retrieval | Hybrid BM25 plus dense | Dense-only | Exact terms matter for names and phrases; fusion raises recall | Two-way |
| 6 | Reranking | Cross-encoder reranker on top candidates | No reranker | Cheap first stage plus precise second stage beats either alone | Two-way |
| 7 | Vector store | Qdrant or pgvector | Chroma | Qdrant and pgvector carry production operations; Chroma suits prototypes | Two-way |
| 8 | API layer | FastAPI plus Pydantic | Flask | Typed schemas and validation catch boundary errors early | Two-way |
| 9 | Serving | vLLM for throughput | llama.cpp for local | vLLM batches server GPU work; llama.cpp wins on CPU and edge | Two-way |
| 10 | Tracking | MLflow or W and B | JSON logs | Run comparison needs queries, not grep; JSON suffices only at tiny scale | Two-way |
| 11 | Config | YAML plus Pydantic Settings | Hardcoded constants | Typed validated config centralizes knobs; literals scatter them | Two-way |
| 12 | Storage format | Parquet and JSONL | Text plus database | Columnar plus line-delimited keeps features and audit simple | Two-way |
| 13 | Cache | Redis for frequent reads | No cache | Repeated queries and embeddings benefit; add when hits justify | Two-way |

Read the door column as planning advice. One-way doors get a short ADR and
an evaluation run before committing. Two-way doors get an adapter and a flag
so reversal is a pull request, not a project.

Revisit the table quarterly with fresh evaluation numbers. Tokenizer and
chunking choices age as the corpus mix shifts. Store and serving choices age
as load changes. What was a two-way door at prototype scale can become
one-way once data and clients depend on its quirks. The table is a living
record, not a one-time vote.

Use the worked ports to de-risk the two-way calls. Because Retriever,
Embedder, and DocumentRepository already have fakes and contract tests,
swapping chunking, stores, or rerankers is an adapter change with a
rerun, not a redesign. That reversibility is the return on the layering
investment made in sections one through eight.

---

## Common Mistakes to Avoid

1. ❌ **Letting domain import torch or clients:** application logic quietly requires a GPU to import.
   ✅ Keep domain to stdlib types and move clients to adapters. Review imports first in every pull request.
2. ❌ **Constructing adapters inside use cases:** the use case picks Qdrant by literal import.
   ✅ Inject ports and construct at the composition root. The use case should never name a backend.
3. ❌ **Naming ports after products:** QdrantRetriever as a port freezes the stack.
   ✅ Name the role Retriever and let adapters carry product names. Product names belong outside only.
4. ❌ **Leaking record types through ports:** callers import client types to read results.
   ✅ Translate to plain passages at the adapter edge. Callers should never import a client library.
5. ❌ **Joining responsibilities in one step name:** chunk_and_embed hides two change reasons.
   ✅ Split into chunk_sections and embed_texts. Each step then owns exactly one reason to change.
6. ❌ **Hardcoding model names and URLs:** evaluation cannot sweep without edits.
   ✅ Put every knob in typed config and pass it to factories. Review flags literals outside config.
7. ❌ **Testing through the real store:** unit runs need containers and networks.
   ✅ Test domain and application with fakes; replay fixtures for adapters. Fast suites stay offline.
8. ❌ **Layering a one-off script:** three Protocols for a single spike slow the experiment.
   ✅ Start flat and extract when the second caller arrives. The rule of two decides.

---

## Best Practices

1. Draw the four rings on every design review and label each new file with its ring.
   Newcomers learn placement in one review when every file states its layer.
2. Define each port beside the use case that needs it, not beside the adapter.
   Proximity reminds readers who owns the contract and who merely satisfies it.
3. Keep port signatures to plain types: strings, ints, lists, and small dataclasses.
   Plain types keep callers free of client imports and make fakes trivial.
4. Inject all collaborators through constructors typed to ports.
   Constructor injection makes substitution visible at the call site every time.
5. Build every adapter in a factory that takes typed config and returns the port.
   Factories centralize branching so use cases never switch on backend names.
6. Translate outer record shapes to inner passage shapes at the adapter boundary.
   One translation point keeps client upgrades from rippling into orchestration.
7. Name pipeline steps with single verbs and keep each step list readable top to bottom.
   A readable list is the cheapest diagram and the fastest onboarding document.
8. Break ranking ties by id so paging and fakes agree exactly.
   Deterministic order turns substitution proofs from similarity into equality.
9. Make generators deterministic in tests with fixed templates and seeded sampling.
   Fixed outputs isolate adapter differences from sampling noise during review.
10. Record every run with parameters, dataset hash, and metrics in the tracker.
    Complete rows let evaluation join across runs instead of reconstructing from logs.
11. Prefer composition of small ports over one fat interface.
    Small ports keep fakes small and let evaluation bind only what it needs.
12. Run the same contract cases against every adapter before accepting a swap.
    Shared cases turn Liskov from a slogan into a suite that blocks regressions.
13. Treat one-way doors with an ADR and evaluation; treat two-way doors with a flag.
    Matching ceremony to reversibility keeps planning proportional to risk.
14. Keep secrets in the environment and names in config; commit neither credentials nor env files.
    The seam holds non-sensitive knobs while credentials never enter the repo.

---

## Practice Exercises

Each exercise maps to one lecture section and runs offline with the track checker.

1. Draw the dependency arrows for AnswerQuestion, Retriever, InMemoryRetriever, and the HTTP handler, then mark which arrows would reverse if the use case constructed the adapter directly.
   Label each arrow with the imported name to make the violation explicit.
2. Write a HybridRetriever that composes a dense and a sparse Retriever behind the same port, merges by normalized score, and passes the shared contract cases without editing callers.
   Prove substitution by running the contract file unchanged against the new class.
3. Promote a hardcoded model literal to the config seam: move the string to typed config, thread it through the factory, and show evaluation sweeping two values with no code edits.
   Show the diff touching only config and factory files.
4. Split a three-responsibility step named ingest_and_chunk_and_upsert into three named steps, then run the pipeline runner before and after to show identical outputs.
   Record timing per step to confirm the split did not change behavior.
5. Add a second CitationPolicy that requires two supporting passages, bind it without touching AnswerQuestion, and run the application tests to confirm the use case is unchanged.
   Demonstrate the swap in the composition root only.

---

## Summary

Nine statements carry the lecture. Each maps to one section above.

1. Dependencies point inward; domain depends on nothing and outer details live outside.
   The import arrow is the architecture; review it before logic.
2. Ports are Protocols defined by inner needs; adapters implement them from outside.
   Small plain-typed contracts keep substitution honest.
3. Seven RAG ports cover retrieval, generation, tokenization, documents, embeddings, citations, and tracking.
   Role names survive every store and model swap in section ten.
4. AnswerQuestion proves substitution by returning identical results on two adapters.
   Exact equality, not similarity, is the bar for portable orchestration.
5. SOLID maps to five small file-level changes, not slogans.
   Inversion first makes the other four steps fall into place.
6. Eleven patterns each have a trigger; without the trigger, write the plain version.
   One pattern per seam beats stacked abstractions.
7. Pipelines are named step lists with a runner; single-responsibility names keep them editable.
   Explicit lists make order, timing, and dry runs visible.
8. Typed config is the only seam; hardcoded models and URLs are layering violations.
   Centralized knobs let evaluation sweep without code edits.
9. Layered tests run domain and application cases with no GPU, network, or store.
   Contract cases run unchanged against every adapter.

**Next lecture:** adapters in depth, with the Qdrant mapping, batching, error translation, and recorded-fixture contract tests.

Work the five practice exercises before moving on. Each takes under thirty
minutes with the checker and together they rehearse every layer decision the
next lecture assumes. Bring your dependency sketch from exercise one to the
adapters lecture because its first section builds directly on that drawing.
Keep the checker output from section three as well; the adapter examples
reference each HEX code by number and expect that context.
Start the next lecture with the decision table nearby; its tradeoffs return.
