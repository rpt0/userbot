"""State Manager for handling temporary data storage across multiple clients.

This module provides a simple key-value store with client isolation.
Each client has its own namespace to avoid data conflicts.
"""

from threading import Lock
from typing import Any, Dict


class State:
    """State manager for temporary data storage with client isolation."""

    def __init__(self):
        """Initialize empty state storage and lock mechanism."""
        self._state: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def set(self, client_id: str, key: str, value: Any) -> None:
        """Set a value for a specific client.

        Args:
            client_id: Unique identifier for the client
            key: Key to store the value under
            value: Value to store
        """
        with self._lock:
            if client_id not in self._state:
                self._state[client_id] = {}
            self._state[client_id][key] = value

    def get(self, client_id: str, key: str, default: Any = None) -> Any:
        """Get a value for a specific client.

        Args:
            client_id: Unique identifier for the client
            key: Key to retrieve
            default: Value to return if key doesn't exist

        Returns:
            Stored value or default if not found
        """
        with self._lock:
            return self._state.get(client_id, {}).get(key, default)

    def delete(self, client_id: str, key: str) -> bool:
        """Delete a value for a specific client.

        Args:
            client_id: Unique identifier for the client
            key: Key to delete

        Returns:
            True if value was deleted, False if it didn't exist
        """
        with self._lock:
            if client_id in self._state and key in self._state[client_id]:
                del self._state[client_id][key]
                return True
            return False

    def clear_client(self, client_id: str) -> None:
        """Clear all data for a specific client.

        Args:
            client_id: Unique identifier for the client
        """
        with self._lock:
            self._state.pop(client_id, None)

    def clear_all(self) -> None:
        """Clear all data for all clients."""
        with self._lock:
            self._state.clear()

    def get_keys(self, client_id: str) -> list:
        """Get all keys stored for a specific client.

        Args:
            client_id: Unique identifier for the client

        Returns:
            List of keys stored for the client
        """
        with self._lock:
            return list(self._state.get(client_id, {}).keys())

    def has_key(self, client_id: str, key: str) -> bool:
        """Check if a key exists for a specific client.

        Args:
            client_id: Unique identifier for the client
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        with self._lock:
            return client_id in self._state and key in self._state[client_id]


# Create global state instance
state = State()
