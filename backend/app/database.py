"""
Database Connection Module
Implements connection pooling and database utilities for PostgreSQL
"""
import logging
from contextlib import contextmanager
from typing import Generator, Optional
import psycopg2
from psycopg2 import pool, extras, Error as Psycopg2Error
from psycopg2.extensions import connection as Connection

from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseConnectionPool:
    """
    Manages PostgreSQL connection pool for the application.
    Implements singleton pattern to ensure single pool instance.
    """
    
    _instance: Optional['DatabaseConnectionPool'] = None
    _pool: Optional[pool.ThreadedConnectionPool] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnectionPool, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize connection pool if not already initialized"""
        if self._pool is None:
            self._initialize_pool()
    
    def _initialize_pool(self):
        """Create the connection pool with configured settings"""
        try:
            self._pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                # Connection options
                connect_timeout=settings.DB_POOL_TIMEOUT,
                options=f'-c statement_timeout={settings.DB_POOL_TIMEOUT * 1000}'  # milliseconds
            )
            logger.info(
                f"Database connection pool initialized: "
                f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
            )
        except Psycopg2Error as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise
    
    def get_connection(self) -> Connection:
        """
        Get a connection from the pool
        
        Returns:
            Connection: PostgreSQL connection object
            
        Raises:
            Psycopg2Error: If unable to get connection from pool
        """
        if self._pool is None:
            raise RuntimeError("Connection pool not initialized")
        
        try:
            conn = self._pool.getconn()
            logger.debug("Connection acquired from pool")
            return conn
        except Psycopg2Error as e:
            logger.error(f"Failed to get connection from pool: {e}")
            raise
    
    def return_connection(self, conn: Connection):
        """
        Return a connection to the pool
        
        Args:
            conn: Connection to return to pool
        """
        if self._pool is None:
            raise RuntimeError("Connection pool not initialized")
        
        try:
            self._pool.putconn(conn)
            logger.debug("Connection returned to pool")
        except Psycopg2Error as e:
            logger.error(f"Failed to return connection to pool: {e}")
            raise
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self._pool is not None:
            self._pool.closeall()
            logger.info("All database connections closed")
    
    def health_check(self) -> bool:
        """
        Check if database connection is healthy
        
        Returns:
            bool: True if connection is healthy, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            self.return_connection(conn)
            return result[0] == 1
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global connection pool instance
db_pool = DatabaseConnectionPool()


@contextmanager
def get_db_connection() -> Generator[Connection, None, None]:
    """
    Context manager for database connections.
    Automatically handles connection acquisition and release.
    
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table")
            results = cursor.fetchall()
    
    Yields:
        Connection: PostgreSQL connection object
    """
    conn = None
    try:
        conn = db_pool.get_connection()
        yield conn
    except Psycopg2Error as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            db_pool.return_connection(conn)


@contextmanager
def get_db_cursor(commit: bool = False) -> Generator[extras.RealDictCursor, None, None]:
    """
    Context manager for database cursor with automatic connection management.
    Returns results as dictionaries for easier access.
    
    Args:
        commit: If True, commits transaction on success
    
    Usage:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO table VALUES (%s)", (value,))
    
    Yields:
        RealDictCursor: Cursor that returns results as dictionaries
    """
    conn = None
    cursor = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        yield cursor
        if commit:
            conn.commit()
            logger.debug("Transaction committed")
    except Psycopg2Error as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
            logger.debug("Transaction rolled back")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.return_connection(conn)


def execute_query(query: str, params: tuple = None, fetch: bool = True) -> Optional[list]:
    """
    Execute a SQL query with automatic connection management
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: If True, fetches and returns results
    
    Returns:
        List of results if fetch=True, None otherwise
    
    Raises:
        Psycopg2Error: If query execution fails
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        return None


def execute_transaction(queries: list[tuple[str, tuple]]) -> bool:
    """
    Execute multiple queries in a single transaction
    
    Args:
        queries: List of (query, params) tuples
    
    Returns:
        bool: True if transaction succeeded
    
    Raises:
        Psycopg2Error: If any query fails
    """
    with get_db_cursor(commit=True) as cursor:
        for query, params in queries:
            cursor.execute(query, params)
    return True


def init_database():
    """
    Initialize database connection pool.
    Called during application startup.
    """
    global db_pool
    db_pool = DatabaseConnectionPool()
    logger.info("Database initialized")


def close_database():
    """
    Close all database connections.
    Called during application shutdown.
    """
    db_pool.close_all_connections()
    logger.info("Database connections closed")
