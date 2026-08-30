"""Database connection and session management."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings


class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, settings: Settings):
        """Initialize database manager.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.engine = None
        self.async_session_maker = None
    
    async def initialize(self) -> None:
        """Initialize database engine and session factory."""
        # Create async engine
        self.engine = create_async_engine(
            self.settings.database_url,
            echo=self.settings.database_echo,
            pool_size=self.settings.database_pool_size,
            max_overflow=self.settings.database_max_overflow,
            connect_args={
                "server_settings": {
                    "application_name": "incidentiq",
                    "jit": "off",
                }
            },
        )
        
        # Create async session factory
        self.async_session_maker = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
    
    async def close(self) -> None:
        """Close database engine."""
        if self.engine:
            await self.engine.dispose()
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session.
        
        Yields:
            AsyncSession: Database session
        """
        if not self.async_session_maker:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database manager instance
_db_manager: DatabaseManager | None = None


def get_db_manager() -> DatabaseManager:
    """Get global database manager instance.
    
    Returns:
        DatabaseManager: Global database manager
        
    Raises:
        RuntimeError: If database manager not initialized
    """
    if _db_manager is None:
        raise RuntimeError("Database manager not initialized")
    return _db_manager


async def init_db(settings: Settings) -> DatabaseManager:
    """Initialize global database manager.
    
    Args:
        settings: Application settings
        
    Returns:
        DatabaseManager: Initialized database manager
    """
    global _db_manager
    _db_manager = DatabaseManager(settings)
    await _db_manager.initialize()
    return _db_manager


async def close_db() -> None:
    """Close global database manager."""
    global _db_manager
    if _db_manager:
        await _db_manager.close()
        _db_manager = None
