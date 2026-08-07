from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.mongo import mongo_health

router = APIRouter(tags=["System"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    postgres = "error"
    try:
        db.execute(text("SELECT 1"))
        postgres = "connected"
    except Exception as exc:  # Health endpoint must report the error instead of crashing.
        postgres = f"error: {type(exc).__name__}"

    return {
        "status": "ok" if postgres == "connected" else "degraded",
        "postgres": postgres,
        "mongo": "connected" if mongo_health() else "unavailable",
    }
