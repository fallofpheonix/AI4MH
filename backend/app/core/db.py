from __future__ import annotations

from app.core.config import Settings, settings
from app.crud.base import Store
from app.crud.sqlite import SQLiteStore


def create_store(config: Settings = settings) -> Store:
    return SQLiteStore(db_path=config.sqlite_path, max_posts=config.max_posts)
