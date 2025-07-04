"""
Create statements table
"""
from yoyo import step

steps = [
    step(
        # Forward migration
        """
        CREATE TABLE statements (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            date_made DATE,
            politician_id INTEGER NOT NULL,
            ai_summary TEXT,
            ai_contradiction_analysis TEXT,
            source_url VARCHAR(1024),
            source_type VARCHAR(50),
            source_name VARCHAR(255),
            review_status VARCHAR(50) DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (politician_id) REFERENCES politicians (id)
        )
        """,
        # Rollback migration
        "DROP TABLE IF EXISTS statements"
    ),
    step(
        "CREATE INDEX ix_statements_id ON statements (id)",
        "DROP INDEX IF EXISTS ix_statements_id"
    ),
    step(
        "CREATE INDEX ix_statements_politician_id ON statements (politician_id)",
        "DROP INDEX IF EXISTS ix_statements_politician_id"
    )
]