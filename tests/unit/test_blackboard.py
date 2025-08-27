"""
Unit tests for the Blackboard shared workspace system.
"""

import pytest
import asyncio
import time
from unittest.mock import MagicMock

from liteagent.blackboard import (
    Blackboard, KnowledgeItem, Subscription,
    LastWriterWinsStrategy, VersionedMergeStrategy
)


class TestKnowledgeItem:
    """Test KnowledgeItem dataclass."""
    
    def test_knowledge_item_creation(self):
        """Test creating a KnowledgeItem."""
        item = KnowledgeItem(
            key="test_key",
            data={"value": 42},
            agent_id="agent_1",
            timestamp=time.time(),
            version=1,
            category="test_category"
        )
        
        assert item.key == "test_key"
        assert item.data == {"value": 42}
        assert item.agent_id == "agent_1"
        assert item.version == 1
        assert item.category == "test_category"
    
    def test_knowledge_item_serialization(self):
        """Test KnowledgeItem to/from dict conversion."""
        item = KnowledgeItem(
            key="test_key",
            data={"value": 42},
            agent_id="agent_1", 
            timestamp=time.time(),
            version=1
        )
        
        item_dict = item.to_dict()
        reconstructed = KnowledgeItem.from_dict(item_dict)
        
        assert reconstructed.key == item.key
        assert reconstructed.data == item.data
        assert reconstructed.agent_id == item.agent_id
        assert reconstructed.version == item.version


class TestBlackboard:
    """Test Blackboard functionality."""
    
    @pytest.fixture
    def blackboard(self):
        """Create a fresh blackboard for testing."""
        return Blackboard()
    
    @pytest.mark.asyncio
    async def test_write_and_read_knowledge(self, blackboard):
        """Test basic write and read operations."""
        # Write knowledge
        item = await blackboard.write_knowledge(
            key="test_key",
            data={"message": "hello world"},
            agent_id="agent_1",
            category="test"
        )
        
        assert item.key == "test_key"
        assert item.data == {"message": "hello world"}
        assert item.agent_id == "agent_1"
        assert item.version == 1
        
        # Read knowledge
        retrieved_item = await blackboard.read_knowledge("test_key")
        assert retrieved_item is not None
        assert retrieved_item.key == "test_key"
        assert retrieved_item.data == {"message": "hello world"}
    
    @pytest.mark.asyncio
    async def test_read_nonexistent_knowledge(self, blackboard):
        """Test reading knowledge that doesn't exist."""
        item = await blackboard.read_knowledge("nonexistent_key")
        assert item is None
    
    @pytest.mark.asyncio
    async def test_knowledge_categories(self, blackboard):
        """Test category-based knowledge organization."""
        # Write items to different categories
        await blackboard.write_knowledge("item1", "data1", "agent1", category="cat_a")
        await blackboard.write_knowledge("item2", "data2", "agent2", category="cat_a")
        await blackboard.write_knowledge("item3", "data3", "agent3", category="cat_b")
        
        # Get items by category
        cat_a_items = await blackboard.get_knowledge_by_category("cat_a")
        cat_b_items = await blackboard.get_knowledge_by_category("cat_b")
        
        assert len(cat_a_items) == 2
        assert len(cat_b_items) == 1
        
        # Check categories
        categories = await blackboard.get_categories()
        assert "cat_a" in categories
        assert "cat_b" in categories
    
    @pytest.mark.asyncio
    async def test_conflict_resolution_last_writer_wins(self, blackboard):
        """Test last-writer-wins conflict resolution."""
        # Write initial knowledge
        await blackboard.write_knowledge("conflict_key", "data1", "agent1")
        
        # Write conflicting knowledge
        await blackboard.write_knowledge("conflict_key", "data2", "agent2")
        
        # Should have the latest data
        item = await blackboard.read_knowledge("conflict_key")
        assert item.data == "data2"
        assert item.agent_id == "agent2"
    
    @pytest.mark.asyncio
    async def test_versioned_merge_strategy(self):
        """Test versioned merge conflict resolution."""
        blackboard = Blackboard(conflict_strategy=VersionedMergeStrategy())
        
        # Write initial knowledge
        await blackboard.write_knowledge("merge_key", "data1", "agent1")
        
        # Write conflicting knowledge
        await blackboard.write_knowledge("merge_key", "data2", "agent2")
        
        # Should have incremented version
        item = await blackboard.read_knowledge("merge_key")
        assert item.data == "data2"
        assert item.version == 2
    
    @pytest.mark.asyncio
    async def test_optimistic_locking(self, blackboard):
        """Test optimistic locking with version checking."""
        # Write initial knowledge
        item = await blackboard.write_knowledge("lock_key", "data1", "agent1")
        
        # Try to update with correct version
        updated_item = await blackboard.write_knowledge(
            "lock_key", "data2", "agent2", expected_version=item.version
        )
        assert updated_item.data == "data2"
        
        # Try to update with incorrect version (should fail)
        with pytest.raises(ValueError, match="Version conflict"):
            await blackboard.write_knowledge(
                "lock_key", "data3", "agent3", expected_version=1
            )
    
    @pytest.mark.asyncio
    async def test_subscription_notifications(self, blackboard):
        """Test pattern-based subscriptions."""
        notifications = []
        
        def callback(item: KnowledgeItem):
            notifications.append(item)
        
        # Subscribe to pattern
        subscription_id = await blackboard.subscribe_to_pattern(
            pattern="test_.*",
            callback=callback,
            agent_id="subscriber_agent"
        )
        
        # Write matching knowledge
        await blackboard.write_knowledge("test_item1", "data1", "agent1")
        await blackboard.write_knowledge("test_item2", "data2", "agent2")
        await blackboard.write_knowledge("other_item", "data3", "agent3")
        
        # Should have received 2 notifications
        await asyncio.sleep(0.1)  # Allow notifications to process
        assert len(notifications) == 2
        assert notifications[0].key == "test_item1"
        assert notifications[1].key == "test_item2"
        
        # Unsubscribe
        success = await blackboard.unsubscribe(subscription_id)
        assert success
    
    @pytest.mark.asyncio
    async def test_knowledge_deletion(self, blackboard):
        """Test knowledge deletion."""
        # Write knowledge
        await blackboard.write_knowledge("delete_key", "data", "agent1", category="test")
        
        # Verify it exists
        item = await blackboard.read_knowledge("delete_key")
        assert item is not None
        
        # Delete it
        success = await blackboard.delete_knowledge("delete_key", "agent1")
        assert success
        
        # Verify it's gone
        item = await blackboard.read_knowledge("delete_key")
        assert item is None
        
        # Category should be cleaned up
        categories = await blackboard.get_categories()
        assert "test" not in categories
    
    @pytest.mark.asyncio
    async def test_ttl_expiration(self):
        """Test TTL-based knowledge expiration."""
        # Create blackboard with short TTL
        blackboard = Blackboard(default_ttl=0.1)  # 100ms
        
        # Write knowledge
        await blackboard.write_knowledge("ttl_key", "data", "agent1")
        
        # Should exist immediately
        item = await blackboard.read_knowledge("ttl_key")
        assert item is not None
        
        # Wait for expiration
        await asyncio.sleep(0.2)
        
        # Should be expired
        item = await blackboard.read_knowledge("ttl_key")
        assert item is None
    
    @pytest.mark.asyncio
    async def test_blackboard_stats(self, blackboard):
        """Test blackboard statistics."""
        # Write some test data
        await blackboard.write_knowledge("item1", "data1", "agent1", category="cat1")
        await blackboard.write_knowledge("item2", "data2", "agent2", category="cat1")
        await blackboard.write_knowledge("item3", "data3", "agent3", category="cat2")
        
        # Subscribe to something
        await blackboard.subscribe_to_pattern(".*", lambda x: None, "agent1")
        
        # Get stats
        stats = await blackboard.get_stats()
        
        assert stats["total_items"] == 3
        assert stats["categories"] == 2
        assert stats["subscriptions"] == 1
        assert stats["category_breakdown"]["cat1"] == 2
        assert stats["category_breakdown"]["cat2"] == 1
    
    @pytest.mark.asyncio
    async def test_get_all_keys(self, blackboard):
        """Test getting all knowledge keys."""
        # Initially empty
        keys = await blackboard.get_all_keys()
        assert len(keys) == 0
        
        # Add some items
        await blackboard.write_knowledge("key1", "data1", "agent1")
        await blackboard.write_knowledge("key2", "data2", "agent2")
        
        # Should have both keys
        keys = await blackboard.get_all_keys()
        assert len(keys) == 2
        assert "key1" in keys
        assert "key2" in keys


class TestSubscription:
    """Test Subscription functionality."""
    
    def test_subscription_pattern_matching(self):
        """Test subscription pattern matching."""
        subscription = Subscription(
            pattern="test_.*",
            callback=lambda x: None,
            agent_id="agent1",
            subscription_id="sub1"
        )
        
        # Create test items
        matching_item = KnowledgeItem("test_item", "data", "agent", time.time(), 1)
        non_matching_item = KnowledgeItem("other_item", "data", "agent", time.time(), 1)
        
        assert subscription.matches(matching_item)
        assert not subscription.matches(non_matching_item)
    
    def test_subscription_category_filtering(self):
        """Test subscription with category filtering."""
        subscription = Subscription(
            pattern=".*",
            callback=lambda x: None,
            agent_id="agent1", 
            subscription_id="sub1",
            categories=["cat1", "cat2"]
        )
        
        # Create test items
        matching_item = KnowledgeItem("item", "data", "agent", time.time(), 1, "cat1")
        non_matching_item = KnowledgeItem("item", "data", "agent", time.time(), 1, "cat3")
        
        assert subscription.matches(matching_item)
        assert not subscription.matches(non_matching_item)