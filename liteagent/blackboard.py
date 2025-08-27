"""
Blackboard-pattern shared workspace for multi-agent collaboration.

This module implements a shared knowledge workspace where multiple agents can:
- Write and read knowledge items with versioning
- Subscribe to pattern-based notifications
- Coordinate through shared state management
- Resolve conflicts through optimistic locking
"""

import asyncio
import json
import time
import re
from typing import Any, Dict, List, Optional, Callable, Union, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from threading import Lock
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeItem:
    """Represents a piece of knowledge on the blackboard."""
    key: str
    data: Any
    agent_id: str
    timestamp: float
    version: int
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeItem':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Subscription:
    """Represents a pattern subscription for notifications."""
    pattern: str
    callback: Callable[[KnowledgeItem], None]
    agent_id: str
    subscription_id: str
    categories: Optional[List[str]] = None
    
    def matches(self, item: KnowledgeItem) -> bool:
        """Check if this subscription matches a knowledge item."""
        # Check pattern match
        if not re.search(self.pattern, item.key):
            return False
            
        # Check category filter if specified
        if self.categories and item.category not in self.categories:
            return False
            
        return True


class ConflictResolutionStrategy:
    """Base class for conflict resolution strategies."""
    
    def resolve(self, current: KnowledgeItem, incoming: KnowledgeItem) -> KnowledgeItem:
        """Resolve conflict between current and incoming knowledge items."""
        raise NotImplementedError


class LastWriterWinsStrategy(ConflictResolutionStrategy):
    """Simple last-writer-wins conflict resolution."""
    
    def resolve(self, current: KnowledgeItem, incoming: KnowledgeItem) -> KnowledgeItem:
        """Always prefer the most recent write."""
        return incoming if incoming.timestamp > current.timestamp else current


class VersionedMergeStrategy(ConflictResolutionStrategy):
    """Merge strategy that increments version numbers."""
    
    def resolve(self, current: KnowledgeItem, incoming: KnowledgeItem) -> KnowledgeItem:
        """Merge by incrementing version and keeping newest data."""
        return KnowledgeItem(
            key=current.key,
            data=incoming.data,
            agent_id=incoming.agent_id,
            timestamp=incoming.timestamp,
            version=max(current.version, incoming.version) + 1,
            category=incoming.category or current.category,
            metadata={**(current.metadata or {}), **(incoming.metadata or {})}
        )


class Blackboard:
    """
    Shared workspace for multi-agent collaboration using the Blackboard pattern.
    
    Features:
    - Thread-safe knowledge storage with versioning
    - Pattern-based subscriptions for real-time notifications
    - Conflict resolution with pluggable strategies
    - Category-based knowledge organization
    - TTL-based cleanup for memory management
    """
    
    def __init__(self, 
                 conflict_strategy: Optional[ConflictResolutionStrategy] = None,
                 default_ttl: Optional[float] = None):
        """
        Initialize the blackboard.
        
        Args:
            conflict_strategy: Strategy for resolving write conflicts
            default_ttl: Default time-to-live for knowledge items (seconds)
        """
        self._knowledge: Dict[str, KnowledgeItem] = {}
        self._subscriptions: Dict[str, Subscription] = {}
        self._lock = Lock()
        self._conflict_strategy = conflict_strategy or LastWriterWinsStrategy()
        self._default_ttl = default_ttl
        self._categories: Dict[str, Set[str]] = {}  # category -> set of keys
        
        logger.info("Blackboard initialized")
    
    async def write_knowledge(self, 
                            key: str, 
                            data: Any, 
                            agent_id: str,
                            category: Optional[str] = None,
                            metadata: Optional[Dict[str, Any]] = None,
                            expected_version: Optional[int] = None) -> KnowledgeItem:
        """
        Write knowledge to the blackboard with optimistic locking.
        
        Args:
            key: Unique identifier for the knowledge
            data: The knowledge data (any JSON-serializable type)
            agent_id: ID of the agent writing the knowledge
            category: Optional category for organization
            metadata: Optional metadata for the knowledge item
            expected_version: Expected current version for optimistic locking
            
        Returns:
            The created/updated KnowledgeItem
            
        Raises:
            ValueError: If optimistic locking fails (version mismatch)
        """
        timestamp = time.time()
        
        with self._lock:
            # Check for optimistic locking
            if key in self._knowledge and expected_version is not None:
                current_version = self._knowledge[key].version
                if current_version != expected_version:
                    raise ValueError(
                        f"Version conflict for key '{key}': "
                        f"expected {expected_version}, current {current_version}"
                    )
            
            # Determine version for new item
            if key in self._knowledge:
                current_version = self._knowledge[key].version
                new_version = current_version + 1
            else:
                new_version = 1
            
            # Create new knowledge item
            new_item = KnowledgeItem(
                key=key,
                data=data,
                agent_id=agent_id,
                timestamp=timestamp,
                version=new_version,
                category=category,
                metadata=metadata
            )
            
            # Handle conflicts if key already exists
            if key in self._knowledge:
                current_item = self._knowledge[key]
                resolved_item = self._conflict_strategy.resolve(current_item, new_item)
                self._knowledge[key] = resolved_item
                result_item = resolved_item
            else:
                self._knowledge[key] = new_item
                result_item = new_item
            
            # Update category index
            if category:
                if category not in self._categories:
                    self._categories[category] = set()
                self._categories[category].add(key)
            
            logger.debug(f"Knowledge written: {key} by {agent_id}")
        
        # Notify subscribers (outside the lock to avoid deadlocks)
        await self._notify_subscribers(result_item)
        
        return result_item
    
    async def read_knowledge(self, key: str) -> Optional[KnowledgeItem]:
        """
        Read knowledge from the blackboard.
        
        Args:
            key: The knowledge key to read
            
        Returns:
            The KnowledgeItem if found, None otherwise
        """
        with self._lock:
            item = self._knowledge.get(key)
            if item:
                # Check TTL if configured
                if (self._default_ttl and 
                    time.time() - item.timestamp > self._default_ttl):
                    # Item expired, remove it
                    del self._knowledge[key]
                    if item.category and item.category in self._categories:
                        self._categories[item.category].discard(key)
                    logger.debug(f"Knowledge expired and removed: {key}")
                    return None
                    
            logger.debug(f"Knowledge read: {key} -> {'found' if item else 'not found'}")
            return item
    
    async def get_knowledge_by_category(self, category: str) -> List[KnowledgeItem]:
        """
        Get all knowledge items in a specific category.
        
        Args:
            category: The category to filter by
            
        Returns:
            List of KnowledgeItems in the category
        """
        with self._lock:
            if category not in self._categories:
                return []
            
            items = []
            expired_keys = []
            
            for key in self._categories[category]:
                if key in self._knowledge:
                    item = self._knowledge[key]
                    
                    # Check TTL
                    if (self._default_ttl and 
                        time.time() - item.timestamp > self._default_ttl):
                        expired_keys.append(key)
                    else:
                        items.append(item)
            
            # Clean up expired items
            for key in expired_keys:
                del self._knowledge[key]
                self._categories[category].discard(key)
            
            logger.debug(f"Category query: {category} -> {len(items)} items")
            return items
    
    async def subscribe_to_pattern(self, 
                                 pattern: str, 
                                 callback: Callable[[KnowledgeItem], None],
                                 agent_id: str,
                                 categories: Optional[List[str]] = None) -> str:
        """
        Subscribe to knowledge updates matching a pattern.
        
        Args:
            pattern: Regex pattern to match knowledge keys
            callback: Function to call when matching knowledge is written
            agent_id: ID of the subscribing agent
            categories: Optional list of categories to filter by
            
        Returns:
            Subscription ID for later unsubscription
        """
        subscription_id = str(uuid.uuid4())
        
        subscription = Subscription(
            pattern=pattern,
            callback=callback,
            agent_id=agent_id,
            subscription_id=subscription_id,
            categories=categories
        )
        
        with self._lock:
            self._subscriptions[subscription_id] = subscription
        
        logger.debug(f"Subscription created: {pattern} by {agent_id}")
        return subscription_id
    
    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Remove a subscription.
        
        Args:
            subscription_id: ID of the subscription to remove
            
        Returns:
            True if subscription was found and removed, False otherwise
        """
        with self._lock:
            removed = self._subscriptions.pop(subscription_id, None)
        
        logger.debug(f"Subscription removed: {subscription_id} -> {'success' if removed else 'not found'}")
        return removed is not None
    
    async def get_all_keys(self) -> List[str]:
        """Get all knowledge keys currently on the blackboard."""
        with self._lock:
            return list(self._knowledge.keys())
    
    async def get_categories(self) -> List[str]:
        """Get all categories currently on the blackboard."""
        with self._lock:
            return list(self._categories.keys())
    
    async def delete_knowledge(self, key: str, agent_id: str) -> bool:
        """
        Delete knowledge from the blackboard.
        
        Args:
            key: The knowledge key to delete
            agent_id: ID of the agent requesting deletion
            
        Returns:
            True if knowledge was deleted, False if not found
        """
        with self._lock:
            item = self._knowledge.pop(key, None)
            if item:
                # Remove from category index
                if item.category and item.category in self._categories:
                    self._categories[item.category].discard(key)
                    # Remove empty categories
                    if not self._categories[item.category]:
                        del self._categories[item.category]
                
                logger.debug(f"Knowledge deleted: {key} by {agent_id}")
                return True
            
            return False
    
    async def cleanup_expired(self) -> int:
        """
        Clean up expired knowledge items based on TTL.
        
        Returns:
            Number of items cleaned up
        """
        if not self._default_ttl:
            return 0
        
        current_time = time.time()
        expired_keys = []
        
        with self._lock:
            for key, item in self._knowledge.items():
                if current_time - item.timestamp > self._default_ttl:
                    expired_keys.append(key)
            
            # Remove expired items
            for key in expired_keys:
                item = self._knowledge.pop(key)
                if item.category and item.category in self._categories:
                    self._categories[item.category].discard(key)
                    if not self._categories[item.category]:
                        del self._categories[item.category]
        
        logger.info(f"Cleaned up {len(expired_keys)} expired knowledge items")
        return len(expired_keys)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get blackboard statistics."""
        with self._lock:
            return {
                "total_items": len(self._knowledge),
                "categories": len(self._categories),
                "subscriptions": len(self._subscriptions),
                "category_breakdown": {
                    cat: len(keys) for cat, keys in self._categories.items()
                }
            }
    
    async def _notify_subscribers(self, item: KnowledgeItem) -> None:
        """Notify all matching subscribers about a knowledge update."""
        matching_subscriptions = []
        
        with self._lock:
            for subscription in self._subscriptions.values():
                if subscription.matches(item):
                    matching_subscriptions.append(subscription)
        
        # Call callbacks outside the lock
        for subscription in matching_subscriptions:
            try:
                if asyncio.iscoroutinefunction(subscription.callback):
                    await subscription.callback(item)
                else:
                    subscription.callback(item)
            except Exception as e:
                logger.error(f"Error in subscription callback: {e}")