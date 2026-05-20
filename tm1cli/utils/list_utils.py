"""Shared utilities for list commands: filtering, paging, and output rendering."""
from __future__ import annotations

import json
import re
from enum import Enum
from typing import Optional

import yaml


class OutputFormat(str, Enum):
    yaml = "yaml"
    json = "json"


class VisibilityType(str, Enum):
    public = "public"
    private = "private"
    both = "both"


def apply_filter(names: list[str], pattern: Optional[str]) -> list[str]:
    """Return names matching *pattern* (case-insensitive regex or substring)."""
    if not pattern:
        return names
    try:
        rx = re.compile(pattern, re.IGNORECASE)
        return [n for n in names if rx.search(n)]
    except re.error:
        needle = pattern.lower()
        return [n for n in names if needle in n.lower()]


def apply_paging(items: list, limit: Optional[int], offset: int) -> list:
    """Slice *items* by *offset* and *limit*."""
    if offset:
        items = items[offset:]
    if limit is not None:
        items = items[:limit]
    return items


def render_output(data: list, fmt: OutputFormat) -> str:
    """Serialise *data* to a YAML or JSON string."""
    if fmt == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    return yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False).rstrip()
