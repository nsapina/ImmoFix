import logging
from datetime import datetime, timezone

from app.config import settings

logger = logging.getLogger(__name__)

try:
    from pymongo import ASCENDING, DESCENDING, MongoClient
    from pymongo.errors import PyMongoError
    PYMONGO_AVAILABLE = True
except ImportError:  # Allows the API to run in degraded mode if the optional Mongo service is absent.
    ASCENDING = 1
    DESCENDING = -1
    MongoClient = None
    PyMongoError = Exception
    PYMONGO_AVAILABLE = False

client = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=2500) if PYMONGO_AVAILABLE else None
database = client[settings.mongo_db] if client is not None else None
events = database["ticket_events"] if database is not None else None


def ensure_indexes() -> None:
    if events is None:
        logger.warning("PyMongo is unavailable; ticket events run in degraded mode.")
        return
    try:
        events.create_index([("ticket_id", ASCENDING), ("created_at", DESCENDING)])
    except PyMongoError as exc:
        logger.warning("MongoDB index could not be created: %s", exc)


def log_event(ticket_id: int, event_type: str, actor: str, data: dict | None = None) -> str | None:
    if events is None:
        return None
    document = {
        "ticket_id": ticket_id,
        "event_type": event_type,
        "actor": actor,
        "data": data or {},
        "created_at": datetime.now(timezone.utc),
    }
    try:
        result = events.insert_one(document)
        return str(result.inserted_id)
    except PyMongoError as exc:
        logger.warning("MongoDB event could not be written: %s", exc)
        return None


def list_events(ticket_id: int) -> list[dict]:
    if events is None:
        return []
    try:
        result = []
        for document in events.find({"ticket_id": ticket_id}).sort("created_at", ASCENDING):
            document["id"] = str(document.pop("_id"))
            result.append(document)
        return result
    except PyMongoError as exc:
        logger.warning("MongoDB events could not be read: %s", exc)
        return []


def delete_events(ticket_id: int) -> None:
    if events is None:
        return
    try:
        events.delete_many({"ticket_id": ticket_id})
    except PyMongoError as exc:
        logger.warning("MongoDB events could not be deleted: %s", exc)


def mongo_health() -> bool:
    if client is None:
        return False
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False
