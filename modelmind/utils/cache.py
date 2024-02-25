from typing import Any, Dict, Optional


class SimpleCache:
    def __init__(self):
        self._cache: Dict[str, Any] = dict()

    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)

    def set(self, key: str, value: Any):
        self._cache[key] = value
