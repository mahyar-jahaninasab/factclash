from datetime import datetime, timezone
from typing import Optional
import unicodedata


def _normalize_text(s: str) -> str:
    """Unicode-normalize, case-fold and collapse whitespace."""
    return " ".join(unicodedata.normalize("NFC", s).casefold().split())


def _utc_iso(dt: Optional[datetime]) -> Optional[str]:
    return dt.astimezone(timezone.utc).isoformat() if dt else None
