# Glossary 01: Hexagonal Architecture Terms

This glossary supports Lecture 01. The table gives a one-line reminder for
each term; the definitions below add a fuller explanation with an example
from the Islamic-corpus RAG system used throughout the track.

| # | Term | One-line reminder |
|---|------|-------------------|
| 1 | Hexagonal architecture | Ports and adapters isolate the core from outer details |
| 2 | Clean architecture | Concentric layers with inward-only dependencies |
| 3 | Domain layer | Entities, value objects, and policies with no frameworks |
| 4 | Application layer | Use cases plus the ports they need |
| 5 | Infrastructure layer | Driven adapters, clients, and config builders |
| 6 | Interfaces layer | Driving adapters such as HTTP and CLI |
| 7 | Dependency rule | Outer layers depend inward; never the reverse |
| 8 | Port | Interface defined by the inner layer for its needs |
| 9 | Adapter | Outer implementation that satisfies a port |
| 10 | Driving adapter | Entry point that calls inward, such as a handler |
| 11 | Driven adapter | Outbound implementation such as a store client |
| 12 | Retriever | Port returning candidate passages for a query |
| 13 | Generator | Port drafting an answer from query plus passages |
| 14 | Tokenizer | Port splitting and normalizing text |
| 15 | DocumentRepository | Port loading and saving documents by id |
| 16 | Embedder | Port mapping text to vectors |
| 17 | CitationPolicy | Port deciding support and formatting references |
| 18 | ExperimentTracker | Port recording runs, params, and metrics |
| 19 | AnswerQuestion | Use case orchestrating retrieve, check, draft, cite |
| 20 | Composition root | Single place where config builds and wires adapters |
| 21 | Config seam | Typed object carrying every environment choice |
| 22 | Passage | Shared plain record of id, book, section, and text |
| 23 | InMemoryRetriever | List-scan fake used for fast tests |
| 24 | SimulatedQdrantRetriever | Paged deterministic stand-in for the real store |
| 25 | Contract test | Same cases run against every adapter of a port |
| 26 | Repository pattern | Intent-named collection interface over a store |
| 27 | Strategy pattern | Swappable algorithm behind one method |
| 28 | Factory pattern | Branched construction hidden behind one call |
| 29 | Pipeline | Named ordered list of steps with a runner |
| 30 | PipelineStep | Dataclass naming one unit of pipeline work |
| 31 | Template Method | Fixed skeleton with one varying hook |
| 32 | Observer | Emit events; subscribers attach without coupling |
| 33 | Registry | Name-to-constructor map for discoverable adapters |
| 34 | Unit of Work | Grouped writes committing once together |
| 35 | Circuit Breaker | Fail fast when downstream fails in bursts |

---

## Detailed Definitions

### 1. Hexagonal architecture

The core logic sits in the middle and talks to the outside only through
ports. Each external system gets an adapter that plugs into a port. The
shape is called hexagonal because each side is one integration, and sides
can be added or swapped without touching the middle. In this track the
middle holds AnswerQuestion and the citation policy, and the sides hold the
HTTP handler, the Qdrant client, and the embedding endpoint.

Example: swapping InMemoryRetriever for the Qdrant adapter changes wiring
only. The use case file does not move. New integrations add sides without
editing existing sides, which keeps pull requests small and reviewable.
Sides are also independently testable because each adapter has its own fake
and contract cases.

### 2. Clean architecture

Concentric rings with a dependency rule. Domain is innermost, then
application, then infrastructure, then interfaces. Source imports point
inward. The rule is enforced by review and by the HEX001 to HEX003 checks.
Clean architecture and hexagonal architecture agree on the direction; the
first names the rings and the second names the plugs.

Example: the citation refusal rule lives in the domain ring so both the API
and the evaluation script share it.

### 3. Domain layer

Pure model of the problem: passage validation, the two-text discipline for
Arabic source plus translation, citation sufficiency, and refusal wording.
It uses dataclasses, enums, and typing only. No client, model, or web import
appears here. Domain tests run in milliseconds with plain objects.

Example: a function that returns refused when the passage list is empty,
regardless of which store produced the list. The same function serves the
API, the CLI, and the evaluation script because it depends on plain inputs.
No caller reimplements the refusal wording.

### 4. Application layer

Orchestration of domain rules and ports. Use cases live here, each with a
named goal such as answer a question or ingest a book. The layer defines the
ports it needs and accepts them by constructor. It never constructs clients
or reads environment variables directly.

Example: AnswerQuestion takes a Retriever and a CitationPolicy rather than
importing either implementation. Tests bind fakes with fixed seeds while
production binds the store adapter from config. The orchestration file never
branches on backend names.

### 5. Infrastructure layer

Everything environment-specific: vector-store clients, embedding calls,
database sessions, file writers, and the factories that build them from
config. Each class implements a port defined inside. Failures from clients
are translated here into plain errors the application already handles.

Example: the Qdrant adapter maps record payloads into Passage objects at the
edge so callers never import the client types. Batching, paging, timeouts,
and error translation also live here. Swapping the store replaces this one
directory while ports and use cases stay put.

### 6. Interfaces layer

Driving side entries: HTTP routes, CLI commands, and scheduled jobs. They
parse input, build config, wire adapters at the composition root, call one
use case, and format output. They hold no domain rules and no ranking logic.

Example: the ask route validates the request shape, calls AnswerQuestion,
and returns text plus citations.

### 7. Dependency rule

Dependencies point inward only. Domain knows nothing outer. Application knows
domain. Infrastructure knows application and domain. Interfaces know
application. A single outward import is a violation, not a shortcut. The
HEX001 and HEX003 rules exist to catch exactly this arrow.

Example: an application file importing the Qdrant adapter breaks the rule;
accepting a Retriever follows it. Reviewers check import direction before
logic because a wrong arrow corrupts every later decision. The HEX001 to
HEX003 checks automate that first pass.

### 8. Port

An interface declared where it is used. In Python it is a Protocol with one
or two methods and plain-type signatures. The port documents the contract,
including empty-input behavior and limit handling, so every adapter agrees.
Ports are versioned with the use case, not with the product.

Example: Retriever with retrieve taking a query and a limit and returning a
list of passages. The docstring states empty-input behavior and tie order so
fakes and store adapters agree. Version the port with the use case whenever
the contract changes.

### 9. Adapter

A class outside that satisfies a port. It wraps a client, translates shapes,
maps errors, and owns batching and paging. One port usually has at least two
adapters: a fake for tests and a real one for production. Contract tests run
identical cases against both.

Example: SimulatedQdrantRetriever pages the same seeds deterministically so
results match the in-memory fake exactly. Both share the ranking helper with
id tie-breaking. The demo asserts equality to prove the port boundary holds.

### 10. Driving adapter

An entry that starts work by calling inward. HTTP handlers, CLI commands,
and queue consumers are driving adapters. They own parsing, validation, and
response formatting. They delegate every decision to the use case.

Example: the CLI reads argv, builds config, wires memory or Qdrant, and
prints the answer object.

### 11. Driven adapter

An outbound integration called by the core through a port. Stores, model
endpoints, trackers, and caches are driven adapters. They own retries,
timeouts, and client quirks behind the port boundary.

Example: the embedding adapter retries transient timeouts with backoff and
maps the rest to a plain EmbeddingError.

### 12. Retriever

The port for candidate search. It takes a query string and a limit and
returns passages in rank order with deterministic tie-breaking by id. It
promises an empty list for empty support rather than raising. Both sparse,
dense, and hybrid strategies sit behind this one shape.

Example: retrieve of a verse phrase returns the two seeded passages in id
order for both demo adapters. Over-limit requests clamp to the corpus size.
Blank queries return empty lists rather than raising, per the contract.

### 13. Generator

The port for drafting. It takes a query plus passages and returns text. The
demo generator is deterministic and cites the top passage; production binds a
model-backed adapter with the same signature. Temperature and sampling live
in config, not in the use case.

Example: the stub returns a fixed template so adapter swaps cannot hide in
sampling noise.

### 14. Tokenizer

The port for splitting and normalization. Arabic handling includes
normalization of letter forms, removal of tatweel, and careful treatment of
diacritics per the configured strategy. The port returns token lists or
chunk lists in plain types.

Example: section-aware chunking keeps a verse and its heading together while
fixed-512 splitting is a swappable Strategy alternative. Evaluation compares
both behind the same port without editing callers. Metadata carries book and
section for citation formatting.

### 15. DocumentRepository

The port for document persistence by intent. Methods read get by id and list
by book rather than exposing query strings. Implementations include memory,
file, and database adapters. Evaluation fixtures load through this port so
dataset handling never leaks into use cases.

Example: get_by_id returns the seeded book record for both memory and file
adapters.

### 16. Embedder

The port mapping texts to vectors. It batches inputs, honors a configured
model name, and raises a plain error on failure. Tests bind a hashing fake
with fixed dimensionality. Production binds the model endpoint adapter.

Example: embed of the same passage twice returns the same vector from both
fake and real adapters.

### 17. CitationPolicy

The domain-side rule deciding whether support suffices and how references
read. The default requires at least one passage and formats book, section,
and passage id. A stricter variant requires two. The use case calls it before
drafting and refuses cleanly when support is thin.

Example: empty retrieval yields a refusal with no citations rather than a
guess. The stricter two-passage variant binds without editing the use case.
Wording stays in the domain so API and evaluation refuse identically.

### 18. ExperimentTracker

The port recording runs. It logs parameters, dataset hashes, retrieval
metrics, and generation scores. Memory and MLflow adapters share the shape.
Every pipeline step calls it through the port so runs compare without grep.

Example: AnswerQuestion logs the query hash, the limit, and the passage ids
used. The memory adapter keeps rows in a list for tests while the MLflow
adapter persists them for comparison. Joins across runs power the decision
table in Lecture 01 section ten.

### 19. AnswerQuestion

The central use case. Steps are retrieve, check policy, draft, attach
citations, and track. Collaborators arrive by constructor typed to ports.
The same class runs in tests, evaluation, and production with different
bindings and identical orchestration.

Example: the demo runs it twice with different retrievers and asserts exact
equality of results. Production binds the real store with no orchestration
change. Refusal, drafting, citation, and tracking paths each have a fake
bound test.

### 20. Composition root

The one place that reads config, calls factories, and wires objects. It
lives at the application edge near main or the route setup. Use cases never
locate their own dependencies. Tests use a separate tiny root that wires
fakes.

Example: main builds typed config, asks the factory for a Retriever, and
passes it to AnswerQuestion. Tests use a separate tiny root wiring fakes.
No use case ever locates its own dependencies or reads the environment.

### 21. Config seam

The typed boundary between choices and logic. A settings object validates
model names, URLs, chunk sizes, and limits at startup. Factories take it as
input. Literals for these values anywhere else are flagged as violations.

Example: changing the embedding model edits one config field and reruns
evaluation with no code change. Validation fails fast at startup with field
names and ranges. Secrets stay in the environment and never enter committed
files.

### 22. Passage

The shared plain record flowing across the port. Fields are id, book title,
section label, and text. It carries no client metadata. Both adapters build
it, both callers read it, and equality is by value for test assertions.

Example: two adapters returning the same seeds produce equal passage lists.
Value equality makes the ports-demo assertion meaningful. Client metadata
never enters this shape; translation happens at the adapter edge.

### 23. InMemoryRetriever

The list-scan fake. It holds seeded passages, scores by simple overlap,
breaks ties by id, and slices to the limit. It starts instantly and needs no
server. Application tests and the demo bind it as the baseline.

Example: the demo baseline run against three seeded passages with limit two.
Scoring is plain token overlap with id tie-breaking so the paged stand-in can
match it exactly. No server, no container, no network is needed for the run.

### 24. SimulatedQdrantRetriever

A deterministic stand-in that mimics paged dense retrieval over the same
seeds. It pages internally, merges in rank order, and returns the same slice
as the fake. It exists so the substitution proof runs offline while reading
like the real adapter.

Example: the demo second run asserting exact equality with the fake run.
Paging is internal: the stand-in walks pages of size one, merges by score,
then slices to the limit. Readers see the paging shape of the real adapter
without needing the service.

### 25. Contract test

A shared case list executed against every adapter of a port. Cases cover the
empty query, the limit larger than the corpus, tie order, and unicode input.
A new adapter passes the same file before it ships. Liskov holds by test.

Example: both retrievers returning empty lists for blank input. The shared
case file also covers over-limit, tie order, and unicode. New adapters run
the same file before shipping so Liskov holds by test rather than by hope.

### 26. Repository pattern

A collection-like interface with intent-named methods. Callers say what they
want, not how the store fetches it. The store-specific query lives inside
the adapter. Use it when document access repeats across callers.

Example: list_by_book replacing scattered filter dictionaries. Callers state
intent while the adapter owns the query dialect. Evaluation fixtures load
through the same port so dataset handling never leaks into use cases.

### 27. Strategy pattern

One method with swappable implementations chosen at runtime. Chunking,
ranking, and tokenization each fit. Configuration names the strategy and the
factory returns it. Callers keep one call shape.

Example: section-aware versus fixed-512 chunking behind one chunk method.
Ranking strategies swap the same way behind Retriever. Config names the
choice and the factory returns it without caller edits.

### 28. Factory pattern

Construction with branches hidden behind one function. It reads typed config
and returns a port. Callers never switch on backend names. Registries extend
factories when the option list grows.

Example: make_retriever returning memory or Qdrant from one config field.
Registries extend the factory when options multiply. Unknown names fail fast
with the valid list so typos surface at startup.

### 29. Pipeline

An explicit ordered list of named steps plus a runner. Ingest, training, and
serving each have one list. The list is data, so diffs and logs name steps.
Branching returns the next step name rather than nesting calls.

Example: build_features listing load, normalize, chunk, embed, and write in
order. Training and serving lists reuse the same runner with timing. Diffs
between runs name steps, which makes evaluation comparisons concrete.

### 30. PipelineStep

The dataclass for one unit of pipeline work. It carries a name and a
function taking the shared context. Names use single verbs. Multi-verb names
signal a split. The runner times each step for the tracker.

Example: chunk_sections as one step owning only splitting. The runner records
its timing for the tracker and passes its output key to embed_texts. A name
with two verbs would split here before the second responsibility accretes.

### 31. Template Method

A base class fixing the skeleton with one hook for variation. Evaluation
runs share setup, timed execution, and teardown; only scoring differs. The
base owns the order and the subclass fills the hook.

Example: one base running setup, run, and report while rerank and dense runs
override only the middle. The base owns timing and tracker calls so every
variant reports identically. Subclasses implement exactly one hook method.

### 32. Observer

Decoupled notification. The pipeline emits completion events; the tracker,
logger, and metrics each subscribe. The pipeline never names subscribers.
Adding a subscriber edits registration, not the emitter.

Example: attaching a metrics subscriber without touching pipeline code.
Registration lists the tracker, logger, and metrics handlers in one place.
Removal is equally small: delete the registration line and nothing else moves.

### 33. Registry

A dictionary from names to constructors. It replaces if-chains when adapters
multiply. Tokenizers and retrievers register under short names that config
references. Unknown names fail fast with the valid list.

Example: registering bm25, dense, and hybrid under one retriever map.
Config references the short name while the factory returns the constructor.
Adding a reranked variant registers one entry instead of editing callers.

### 34. Unit of Work

Grouped writes with one commit. Ingest stages passage writes plus alias
updates, then commits once. Failure rolls back the group. Callers see either
all effects or none.

Example: book ingest committing passages and the alias row together.
Staging holds both writes until the final commit call. A mid-batch failure
rolls back the group so callers never see half-ingested books.

### 35. Circuit Breaker

A guard that opens after repeated downstream failures and fails fast until
recovery. It sits in the driven adapter around the client call. It prevents
retry storms when the embedding endpoint stalls. Half-open probes close it
after success.

Example: the embed adapter opening after three timeouts and refusing calls
for the cooldown window. Half-open probes send one trial after the wait and
close on success. Callers see a plain fast failure instead of a hung batch.

---

## How to Use This Glossary

Keep this file open beside the lecture and the checker. When a HEX finding
names a term, read the table row first for the reminder, then the definition
for the example. When review debates a seam, cite the term number so the
discussion stays on placement rather than preference. The thirty-five terms
above are the shared vocabulary for every later track in this lane.

Pair each term with its checker rule while reading. HEX001 guards the
domain and dependency terms. HEX002 and HEX003 guard ports, adapters, and
the composition root. HEX004 and HEX005 guard port contracts. HEX006 guards
pipeline steps. HEX007 guards the config seam. HEX008 guards the missing
seam. The glossary explains the words and the exercise enforces them.

Revisit the quick table weekly until the one-line reminders read as obvious.
Fluency with these names shortens design reviews because placement questions
get answered with a term and a number instead of a paragraph. That shared
shorthand is the practical return on keeping the glossary beside the code.

Use the track checker as the companion drill. Each HEX code maps to the
terms above, and the BAD pack shows one violation per rule with a line
number. Read the finding, open the matching definition, fix the module in
words, then rerun. That loop turns vocabulary into placement habit.
No new terms are introduced here; the loop rehearses the thirty-five above.
Keep scores from the quiz with this file to track which terms need review.
