"""Health check endpoints with async support."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_async_db
from backend.app.database import test_database_connection as test_sync_connection
from backend.app.database_async import test_database_connection, get_database_info, get_async_session_local
from backend.app.core.config import settings
from backend.app.core.exceptions import DatabaseConnectionError

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "The Sauce Bottle API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/health/db")
async def database_health():
    """Check database connectivity (async)."""
    try:
        is_connected = await test_database_connection()
        
        if is_connected:
            db_info = await get_database_info()
            return {
                "status": "healthy",
                "database": "connected",
                **db_info
            }
        else:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "error": "Failed to connect to database"
            }
    except Exception as e:
        # Return error details for debugging, but still return 200 OK
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "note": "Database is currently unavailable",
        }


@router.get("/health/db/detailed")
async def detailed_database_health():
    """Detailed database health check with table information."""
    try:
        # Create session directly without dependency for health check
        session_factory = get_async_session_local()
        async with session_factory() as db:
            # Get database info
            db_info = await get_database_info()
            
            # Get table counts
            if settings.is_sqlite:
                # SQLite query for table info
                tables_query = text("""
                    SELECT name, sql 
                    FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    ORDER BY name
                """)
            else:
                # PostgreSQL query for table info
                tables_query = text("""
                    SELECT table_name as name, 
                           pg_size_pretty(pg_total_relation_size(table_name::regclass)) as size
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
            
            tables_result = await db.execute(tables_query)
            tables = [{"name": row[0], "sql": row[1] if len(row) > 1 else None} for row in tables_result]
            
            # Get row counts for main tables
            table_stats = {}
            for table_name in ["politicians", "statements"]:
                try:
                    count_result = await db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    table_stats[table_name] = count_result.scalar()
                except Exception:
                    table_stats[table_name] = "N/A"
            
            return {
                "status": "healthy",
                "database": {
                    **db_info,
                    "tables": tables,
                    "row_counts": table_stats
                },
                "connection_pool": {
                    "pool_size": settings.DATABASE_POOL_SIZE,
                    "max_overflow": settings.DATABASE_MAX_OVERFLOW
                },
                "configuration": {
                    "echo_sql": settings.DATABASE_ECHO,
                    "url_type": "sqlite" if settings.is_sqlite else "postgresql"
                }
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Failed to retrieve detailed database information"
        }


@router.get("/health/db/migrations")
async def migration_health():
    """Check migration status."""
    try:
        # Create session directly without dependency for health check
        session_factory = get_async_session_local()
        async with session_factory() as db:
            # Check if yoyo migrations table exists
            if settings.is_sqlite:
                check_query = text("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='_yoyo_migration'
                """)
            else:
                check_query = text("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = '_yoyo_migration'
                """)
            
            result = await db.execute(check_query)
            has_migrations_table = result.scalar() is not None
            
            if has_migrations_table:
                # Get migration info
                migrations_query = text("""
                    SELECT migration_id, applied_at_utc 
                    FROM _yoyo_migration 
                    ORDER BY applied_at_utc DESC
                    LIMIT 10
                """)
                migrations_result = await db.execute(migrations_query)
                migrations = [
                    {"id": row.migration_id, "applied_at": str(row.applied_at_utc)}
                    for row in migrations_result
                ]
                
                return {
                    "status": "healthy",
                    "migrations_table": "exists",
                    "recent_migrations": migrations,
                    "total_migrations": len(migrations)
                }
            else:
                return {
                    "status": "warning",
                    "migrations_table": "not found",
                    "message": "Migrations may not have been applied"
                }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to check migration status"
        }