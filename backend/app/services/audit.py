from __future__ import annotations
import json
from typing import Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditEvent


def record_audit_event(
    db: Session,
    event_type: str,
    *,
    user_id: Optional[int] = None,
    outcome: str = 'success',
    request_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> None:
    event = AuditEvent(
        user_id=user_id,
        event_type=event_type,
        outcome=outcome,
        request_id=request_id,
        ip_address=ip_address,
        metadata_json=json.dumps(metadata or {}, separators=(',', ':'), default=str),
    )
    db.add(event)
