# Data Engineering 18: DVC and Dataset Versioning — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| DVC | Dataset versioning with pipelines | dvc repro |
| dvc.yaml | Pipeline stage declarations | stages: clean/dedup/export |
| Stage | One named pipeline step | dedup |
| Cmd | The command a stage runs | python scripts/dedup.py |
| Deps | Files a stage reads | data/clean.csv |
| Outs | Files a stage writes | data/dedup.csv |
| Params | Named values affecting output | threshold: 0.9 |
| params.yaml | Parameter file stages read | dedup.threshold |
| dvc.lock | Pinned checksums of deps/outs | md5 per path |
| dvc repro | Re-run stale stages only | dvc repro |
| Remote | Where data bytes live | local path first |
| dvc push | Upload data to the remote | dvc push |
| dvc pull | Download data from remote | dvc pull |
| dvc add | Start tracking a dataset | dvc add raw/a.csv |
| dvc init | Initialize DVC in a repo | dvc init |
| .dvcignore | Paths DVC must skip | *.tmp |
| manifest.json | Pipeline-written record | row counts + hashes |
| Params hash | Hash of active parameters | sha256 of params |
| Git SHA | Commit that produced data | 40-char hex |
| Stage DAG | Stages linked via files | clean -> dedup -> export |
| Blob bloat | Git history growth from data | 2 GB committed twice |
| Content-addressable | Storage keyed by checksum | .dvc/cache |
| MD5 checksum | Per-file content fingerprint | 32-char hex |
| Reproducibility | Same commit, same bytes | lock diff proves change |

---

## Alphabetical Glossary

### Blob bloat
Git history grows permanently with each committed dataset version. **See also:** Content-addressable.

### Cmd
The exact command a stage runs to rebuild its outputs. **See also:** Stage.

### Content-addressable
Storage keyed by checksum, so identical bytes are stored once. **See also:** MD5 checksum.

### DAG (stage)
Stages linked through files: one stage's outs are the next stage's deps. **See also:** dvc.yaml.

### Deps
Files a stage reads, including its own scripts. **See also:** Outs.

### dvc add
Command that starts tracking a dataset; git stores a small pointer file. **See also:** dvc init.

### dvc init
Command that initializes DVC inside a git repository. **See also:** Remote.

### dvc.lock
File pinning every dep and out checksum after a run; committed to git. **See also:** dvc repro.

### dvc pull
Command downloading data files from the remote. **See also:** dvc push.

### dvc push
Command uploading data files to the configured remote. **See also:** Remote.

### dvc repro
Command re-running only stages whose inputs differ from the lock. **See also:** dvc.lock.

### dvc.yaml
Pipeline file declaring stages with cmd, deps, outs, and params. **See also:** Stage.

### DVC
Data version control: pointers in git, bytes in cache plus remote. **See also:** Reproducibility.

### .dvcignore
Pattern file listing paths DVC must never track. **See also:** Outs.

### Git SHA
The commit hash recorded in the manifest, tying data to code. **See also:** manifest.json.

### manifest.json
Pipeline-written record: checksums, params hash, git sha, row counts, bytes. **See also:** Params hash.

### MD5 checksum
Per-file content fingerprint pinning exact bytes in the lock. **See also:** Content-addressable.

### Outs
Files a stage writes and DVC tracks by checksum. **See also:** Deps.

### Params
Named values from params.yaml that affect a stage's output. **See also:** params.yaml.

### params.yaml
Parameter file whose values stages declare and the manifest hashes. **See also:** Params hash.

### Params hash
Hash of the active parameters, proving which settings produced the data. **See also:** manifest.json.

### Remote
Configured storage for data bytes; local path first, cloud later. **See also:** dvc push.

### Reproducibility
Same commit yields same bytes; any byte change shows as a lock diff. **See also:** dvc.lock.

### Stage
One named pipeline step with cmd, deps, outs, and optional params. **See also:** dvc.yaml.

---

## Related Concepts

- **Provenance**: checksums tie data to its source (topic 06)
- **Versioning**: the vocabulary this tooling implements (topic 14)
- **Dedup counts**: the row accounting the manifest records (topic 05)

## Key Takeaways

1. Pointers in git, bytes in cache plus remote.
2. Lock pins bytes; manifest records meaning.
3. Local remote first, cloud later.
4. Unpinned output is untracked data.
