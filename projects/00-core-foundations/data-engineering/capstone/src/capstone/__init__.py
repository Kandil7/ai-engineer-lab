"""Capstone: raw corpus -> clean -> profile -> dedup -> gates -> version -> export."""

from capstone.clean import clean_text, frame_from_records
from capstone.dedup import dedup_exact, minhash_dedup
from capstone.export import devmate_doc_id, export_jsonl, export_parquet
from capstone.gates import arabic_ratio, quality_gates
from capstone.profile import profile_parquet
from capstone.version import file_checksum, write_manifest

__all__ = [
    "arabic_ratio",
    "clean_text",
    "dedup_exact",
    "devmate_doc_id",
    "export_jsonl",
    "export_parquet",
    "file_checksum",
    "frame_from_records",
    "minhash_dedup",
    "profile_parquet",
    "quality_gates",
    "write_manifest",
]
