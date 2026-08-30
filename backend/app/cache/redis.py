"""Redis cache and session management."""

import json
import logging
from typing import Any, Generic, TypeVar

import redis.asyncio as redis
from redis.asyncio import Redis

from app.config.settings import Settings


logger = logging.getLogger(__name__)

T = TypeVar("T")


class RedisCache(Generic[T]):
    """Redis cache wrapper for key-value operations."""
    
    def __init__(self, redis_client: Redis):
        """Initialize Redis cache.
        
        Args:
            redis_client: Redis async client
        """
        self.redis = redis_client
    
    async def get(self, key: str, default: T | None = None) -> T | None:
        """Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if key not found
            
        Returns:
            Cached value or default
        """
        try:
            value = await self.redis.get(key)
            if value is None:
                return default
            return json.loads(value)
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return default
    
    async def set(
        self,
        key: str,
        value: T,
        ttl: int | None = None,
    ) -> bool:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful
        """
        try:
            serialized = json.dumps(value, default=str)
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)
            return True
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists
        """
        try:
            return bool(await self.redis.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False
    
    async def clear(self, pattern: str = "*") -> int:
        """Clear cache keys matching pattern.
        
        Args:
            pattern: Key pattern (supports wildcards)
            
        Returns:
            Number of keys deleted
        """
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Error clearing cache with pattern {pattern}: {e}")
            return 0


class CacheManager:
    """Manages Redis cache connections."""
    
    def __init__(self, settings: Settings):
        """Initialize cache manager.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.redis: Redis | None = None
        self.cache: RedisCache | None = None
    
    async def initialize(self) -> None:
        """Initialize Redis connection."""
        try:
            self.redis = await redis.from_url(
                self.settings.redis_url,
                decode_responses=False,
                encoding="utf-8",
            )
            # Test connection
            await self.redis.ping()
            self.cache = RedisCache(self.redis)
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise
    
    async def close(self) -> None:
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
            logger.info("Redis cache closed")
    
    def get_cache(self) -> RedisCache:
        """Get cache instance.
        
        Returns:
            RedisCache instance
            
        Raises:
            RuntimeError: If cache not initialized
        """
        if not self.cache:
            raise RuntimeError("Cache not initialized. Call initialize() first.")
        return self.cache


# Global cache manager instance
_cache_manager: CacheManager | None = None


def get_cache_manager() -> CacheManager:
    """Get global cache manager instance.
    
    Returns:
        CacheManager: Global cache manager
        
    Raises:
        RuntimeError: If cache manager not initialized
    """
    if _cache_manager is None:
        raise RuntimeError("Cache manager not initialized")
    return _cache_manager


async def init_cache(settings: Settings) -> CacheManager:
    """Initialize global cache manager.
    
    Args:
        settings: Application settings
        
    Returns:
        CacheManager: Initialized cache manager
    """
    global _cache_manager
    _cache_manager = CacheManager(settings)
    await _cache_manager.initialize()
    return _cache_manager


async def close_cache() -> None:
    """Close global cache manager."""
    global _cache_manager
    if _cache_manager:
        await _cache_manager.close()
        _cache_manager = None
