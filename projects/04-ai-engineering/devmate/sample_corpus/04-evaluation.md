# Evaluation

DevMate measures retrieval and answer quality instead of trusting intuition.

## The eval harness

The harness (`devmate.eval.run_ragas`) scores a golden set of questions against the
retrieval and answer pipelines. It runs offline by default, scoring against recorded
retrieval results so it needs no network and no API key.

## Metrics

- **Hit@k**: the fraction of questions whose expected source appears in the top-k
  retrieved chunks.
- **MRR** (mean reciprocal rank): how high the first correct source ranks, averaged
  over questions. A higher MRR means the right chunk appears nearer the top.
- **Answer pass rate**: the fraction of answers that satisfy structural properties
  such as citing a source and avoiding forbidden phrases.

## The regression gate

The offline harness is wired into CI as a gate: it fails the build when Hit@5 drops
below 1.0 or MRR below 0.70 on the recorded baseline. This means a change to
chunking, embeddings, or a prompt must be justified by numbers, not opinion.

## Reports

Every run can write a report that records the commit SHA and a timestamp, so a
metric is always tied to the exact revision that produced it.
