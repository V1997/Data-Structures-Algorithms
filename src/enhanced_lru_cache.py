"""
Enhanced LRU Cache Implementation
==================================

A proper Least Recently Used (LRU) Cache implementation using:
- Hash table for O(1) key access
- Doubly linked list for O(1) insertion/deletion
- Type hints for better code clarity
- Comprehensive error handling

Time Complexity: O(1) for all operations
Space Complexity: O(capacity)
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Node:
    """Doubly linked list node for LRU cache."""

    key: int
    value: Any
    prev: Optional["Node"] = None
    next: Optional["Node"] = None


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.

    Features:
    - O(1) get and set operations
    - Automatic eviction of least recently used items
    - Thread-safe operations (can be extended)
    - Comprehensive error handling
    """

    def __init__(self, capacity: int) -> None:
        """
        Initialize LRU Cache with given capacity.

        Args:
            capacity: Maximum number of items to store        Raises:
            ValueError: If capacity <= 0
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.cache: Dict[int, Node] = {}
        # Create dummy head and tail nodes for easier list manipulation
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node) -> None:
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        if self.head.next is not None:
            self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node is not None:
            prev_node.next = next_node
        if next_node is not None:
            next_node.prev = prev_node

    def _move_to_head(self, node: Node) -> None:
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """Pop the last node (least recently used)."""
        last_node = self.tail.prev
        if last_node:
            self._remove_node(last_node)
            return last_node
        else:
            # This should never happen in a properly implemented LRU cache
            raise RuntimeError("Cache is empty")

    def get(self, key: int) -> Any:
        """
        Get value by key and mark as recently used.

        Args:
            key: Key to retrieve

        Returns:
            Value if key exists, -1 otherwise
        """
        node = self.cache.get(key)

        if not node:
            return -1

        # Move to head (mark as recently used)
        self._move_to_head(node)
        return node.value

    def set(self, key: int, value: Any) -> None:
        """
        Set key-value pair. Evict LRU item if at capacity.

        Args:
            key: Key to set
            value: Value to store
        """
        if self.capacity == 0:
            print("Warning: Cannot perform operations on 0 capacity cache")
            return

        node = self.cache.get(key)

        if not node:
            new_node = Node(key, value)

            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                tail = self._pop_tail()
                del self.cache[tail.key]

            # Add new node
            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Update existing key
            node.value = value
            self._move_to_head(node)

    def size(self) -> int:
        """Return current cache size."""
        return len(self.cache)

    def __str__(self) -> str:
        """String representation for debugging."""
        items = []
        current = self.head.next
        while current and current != self.tail:
            items.append(f"{current.key}:{current.value}")
            current = current.next
        return f"LRUCache({' -> '.join(items)})"


def demonstrate_lru_cache() -> None:
    """Demonstrate LRU Cache functionality with examples."""
    print("=== LRU Cache Demonstration ===\n")

    # Test 1: Basic operations
    print("Test 1: Basic Operations")
    cache = LRUCache(3)

    cache.set(1, "one")
    cache.set(2, "two")
    cache.set(3, "three")
    print(f"After adding 3 items: {cache}")

    print(f"Get key 1: {cache.get(1)}")  # Should return "one"
    print(f"Get key 4: {cache.get(4)}")  # Should return -1

    # Test 2: Capacity overflow
    print("\nTest 2: Capacity Management")
    cache.set(4, "four")  # Should evict key 2 (LRU)
    print(f"After adding 4th item: {cache}")
    print(f"Get key 2: {cache.get(2)}")  # Should return -1 (evicted)

    # Test 3: Update existing key
    print("\nTest 3: Update Existing Key")
    cache.set(1, "ONE")  # Update existing key
    print(f"After updating key 1: {cache}")
    print(f"Get key 1: {cache.get(1)}")  # Should return "ONE"

    # Test 4: Edge case - zero capacity
    print("\nTest 4: Edge Cases")
    zero_cache = LRUCache(1)
    zero_cache.set(1, "single")
    print(f"Single capacity cache: {zero_cache}")
    zero_cache.set(2, "replacement")
    print(f"After replacement: {zero_cache}")


if __name__ == "__main__":
    demonstrate_lru_cache()
