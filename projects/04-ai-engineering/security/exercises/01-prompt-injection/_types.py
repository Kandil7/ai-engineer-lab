"""
=============================================================================
AI Security Exercise 01: Prompt Injection Attacks & Defenses
=============================================================================

Topic: Prompt Injection
-----------------------
Prompt injection is a vulnerability where an attacker manipulates an LLM's
behavior by crafting inputs that override or bypass the system prompt. This
exercise covers attack vectors and multi-layer defense strategies.

Learning Objectives:
  1. Understand direct and indirect prompt injection techniques
  2. Recognize common jailbreak patterns
  3. Implement robust defense mechanisms
  4. Build detection and monitoring systems

Prerequisites:
  - Python 3.9+
  - openai (pip install openai)
  - re, hashlib, json, logging, dataclasses, enum, typing

WARNING: This code is for EDUCATIONAL purposes. Do not use attack patterns
against systems you do not own or have permission to test.
=============================================================================
"""

import re
import json
import hashlib
import logging
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Callable
from collections import defaultdict

logger = logging.getLogger("prompt_injection")


class AttackType(Enum):
    """Classification of prompt injection attack types."""

    DIRECT_INJECTION = auto()  # User directly overrides system prompt
    INDIRECT_INJECTION = auto()  # Injection via external data/content
    JAILBREAK = auto()  # Bypass safety constraints
    ROLE_HYPING = auto()  # Fake system/admin messages
    ENCODING_EVASION = auto()  # Obfuscate malicious intent
    CONTEXT_MANIPULATION = auto()  # Poison context/history
    MULTILINGUAL = auto()  # Use other languages to bypass filters
    PAYLOAD_SPLITTING = auto()  # Split malicious input across turns


@dataclass
class AttackSignature:
    """Represents a known attack pattern for detection."""

    name: str
    attack_type: AttackType
    patterns: list[str]
    severity: str  # low, medium, high, critical
    description: str


# Known attack signatures database
ATTACK_SIGNATURES: list[AttackSignature] = [
    AttackSignature(
        name="system_override",
        attack_type=AttackType.DIRECT_INJECTION,
        patterns=[
            r"(?i)ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?)",
            r"(?i)disregard\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?)",
            r"(?i)forget\s+(everything|all|your)\s+(you)?(were|have been)\s+told",
            r"(?i)new\s+instructions?:",
            r"(?i)override\s+(system|your|the)\s+(prompt|instructions?)",
            r"(?i)you\s+are\s+now\s+(in|on)\s+(debug|developer|admin)\s+mode",
        ],
        severity="critical",
        description="Attempts to override the system prompt directly",
    ),
    AttackSignature(
        name="role_manipulation",
        attack_type=AttackType.ROLE_HYPING,
        patterns=[
            r"(?i)(system|admin|developer)\s*(message|prompt|override)\s*:",
            r"(?i)\[system\]|\[admin\]|\[override\]",
            r"(?i)<<SYS>>|<</SYS>>",
            r"(?i)###\s*(system|instruction|prompt)\s*###",
            r"(?i)---\s*(system|admin)\s*(start|prompt)---",
        ],
        severity="critical",
        description="Fake system messages injected into user input",
    ),
    AttackSignature(
        name="jailbreak_dan",
        attack_type=AttackType.JAILBREAK,
        patterns=[
            r"(?i)do\s+anything\s+now|DAN\s+mode",
            r"(?i)developer\s+mode\s+(enabled|activated|on)",
            r"(?i)jailbreak|jailbreak(?:ed|ing)",
            r"(?i)unrestricted\s+(mode|ai|assistant)",
            r"(?i)no\s+(restrictions|rules|guidelines|limitations)",
            r"(?i)act\s+as\s+if\s+you\s+(have|had)\s+no\s+(rules|restrictions)",
        ],
        severity="high",
        description="Jailbreak attempts to remove safety constraints",
    ),
    AttackSignature(
        name="encoding_evasion",
        attack_type=AttackType.ENCODING_EVASION,
        patterns=[
            r"(?i)(base64|hex|rot13|binary|unicode)\s*(encode|decode|convert)",
            r"(?i)speak\s+in\s+(code|cipher|pseudocode)",
            r"(?i)use\s+(only\s+)?(first|last)\s+(letters?|characters?|words?)",
            r"(?i)replace\s+(each|every)\s+(letter|word)\s+with",
            r"(?i)caesar\s+cipher|atbash|reverse",
        ],
        severity="medium",
        description="Encoding tricks to obfuscate malicious content",
    ),
    AttackSignature(
        name="payload_splitting",
        attack_type=AttackType.PAYLOAD_SPLITTING,
        patterns=[
            r"(?i)(in\s+your\s+next|for\s+the\s+next|continue\s+with)\s+(response|reply|answer|message)",
            r"(?i)(part|step)\s*[2-9]\s*[:\-]",
            r"(?i)now\s+(say|repeat|output|write)\s+(that|this|the)\s+(without|with|using)",
            r"(?i)concatenate\s+(the|all|these)\s+(above|previous)",
        ],
        severity="medium",
        description="Splitting malicious payloads across multiple turns",
    ),
]


# =============================================================================
# Section 2: Input Sanitizer
# =============================================================================
