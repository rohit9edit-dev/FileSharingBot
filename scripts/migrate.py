# scripts/migrate.py

import asyncio
import logging
from database.connection import get_db
from database.migrations import migrations_list  # assume a list of migration callables

logger = logging.getLogger("MigrationScript")


async def run_migrations():
    """
    Run all pending migrations in order
    """
    db = await get_db()
    for migration in migrations_list:
        try:
            logger.info(f"Running migration: {migration.__name__}")
            await migration(db)
            logger.info(f"Migration {migration.__name__} completed.")
        except Exception as e:
            logger.error(f"Error running migration {migration.__name__}: {e}")
            raise e


if __name__ == "__main__":
    asyncio.run(run_migrations())
    logger.info("All migrations finished.")
