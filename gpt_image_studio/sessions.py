import json
import uuid
from datetime import datetime

from .paths import SESSIONS_DIR, ensure_app_dirs


def list_sessions():
    items = []
    ensure_app_dirs()
    for p in sorted(SESSIONS_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(p.read_text("utf-8"))
            items.append(data)
        except Exception:
            pass
    return items


def load_session(sid: str) -> dict:
    ensure_app_dirs()
    p = SESSIONS_DIR / f"{sid}.json"
    if p.exists():
        return json.loads(p.read_text("utf-8"))
    return {}


def save_session(session: dict):
    ensure_app_dirs()
    p = SESSIONS_DIR / f"{session['id']}.json"
    p.write_text(json.dumps(session, ensure_ascii=False, indent=2), "utf-8")


def new_session() -> dict:
    return {
        "id": str(uuid.uuid4()),
        "title": "新对话",
        "created": datetime.now().isoformat(timespec="seconds"),
        "updated": datetime.now().isoformat(timespec="seconds"),
        "model": "gpt-image-2",
        "turns": [],
    }
