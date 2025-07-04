"""Database utilities for testing and switching between databases."""
import asyncio
import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_database_async():
    """Test async database connection and display information."""
    # Import here to ensure we get fresh settings
    from backend.app.core.config import settings
    from backend.app.database_async import test_database_connection, get_database_info
    
    print("Testing database connection...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Database Type: {'SQLite' if settings.is_sqlite else 'PostgreSQL'}")
    print()
    
    try:
        # Test connection
        is_connected = await test_database_connection()
        
        if is_connected:
            print("✅ Database connection successful!")
            
            # Get detailed info
            db_info = await get_database_info()
            print(f"Database: {db_info['type']} {db_info['version']}")
            print(f"Async Driver: {db_info['async_driver']}")
            print()
        else:
            print("❌ Database connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Main CLI for database utilities."""
    # Process command line args before importing settings
    if len(sys.argv) < 2:
        print("Usage: python -m backend.app.db_utils <command>")
        print("Commands:")
        print("  test        - Test current database connection")
        print("  postgres    - Switch to PostgreSQL and test")
        print("  sqlite      - Switch to SQLite and test")
        print("  info        - Show current database configuration")
        return
    
    command = sys.argv[1].lower()
    
    # Set environment variable BEFORE importing anything that uses settings
    if command == "postgres":
        postgres_url = os.getenv("POSTGRES_DATABASE_URL")
        if not postgres_url:
            print("❌ POSTGRES_DATABASE_URL not set in .env file")
            print("Add your Neon connection string to .env:")
            print('POSTGRES_DATABASE_URL=postgresql+asyncpg://user:password@host/database')
            return
        os.environ["DATABASE_URL"] = postgres_url
        print(f"✅ Switched to PostgreSQL: {postgres_url.split('@')[-1]}")
    
    elif command == "sqlite":
        sqlite_url = "sqlite+aiosqlite:///./saucebottle.db"
        os.environ["DATABASE_URL"] = sqlite_url
        print(f"✅ Switched to SQLite: {sqlite_url}")
    
    # Now handle commands
    if command in ["test", "postgres", "sqlite"]:
        await test_database_async()
    
    elif command == "info":
        # Import settings after env is set
        from backend.app.core.config import settings
        
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Current DATABASE_URL: {settings.DATABASE_URL}")
        print(f"Database Type: {'SQLite' if settings.is_sqlite else 'PostgreSQL'}")
        print(f"Echo SQL: {settings.DATABASE_ECHO}")
        print(f"Pool Size: {settings.DATABASE_POOL_SIZE}")
        print(f"Max Overflow: {settings.DATABASE_MAX_OVERFLOW}")
        
        postgres_url = os.getenv("POSTGRES_DATABASE_URL")
        if postgres_url:
            print(f"\nPostgreSQL URL available: {postgres_url.split('@')[-1]}")
        else:
            print("\nNo POSTGRES_DATABASE_URL set in .env")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    asyncio.run(main())