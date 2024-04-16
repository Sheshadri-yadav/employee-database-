from fastapi import Request
from datetime import datetime
from models.model import AuditLog
from database.db import SessionLocal

def create_audit_log(user_position: str, action: str, timestamp: datetime):
    """Create an audit log entry in the database."""
    db = SessionLocal()
    try:
        audit_log = AuditLog(
            user_position=user_position,
            action=action,
            timestamp=timestamp,
        )
        db.add(audit_log)
        db.commit()
    finally:
        db.close()

async def audit_logger(request: Request, call_next):
    """Middleware function to log audit entries."""
    response = await call_next(request)
    if request.url.path == "/login_page" and request.method == "POST":
        user_position = request.session.get("user_position")
        action = "Login"
        timestamp = datetime.now()
        create_audit_log(user_position, action, timestamp)
    return response
