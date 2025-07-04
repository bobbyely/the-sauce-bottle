"""
Create politicians table
"""
from yoyo import step

steps = [
    step(
        # Forward migration
        """
        CREATE TABLE politicians (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            party VARCHAR,
            chamber VARCHAR,
            position_title VARCHAR,
            electorate VARCHAR,
            state VARCHAR,
            date_elected DATE,
            sitting_status VARCHAR,
            is_cabinet_minister INTEGER,
            is_shadow_minister INTEGER,
            previous_positions VARCHAR,
            website_url VARCHAR,
            social_media_links VARCHAR,
            statement_count INTEGER DEFAULT 0,
            tags VARCHAR,
            profile_picture_url VARCHAR,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Rollback migration
        "DROP TABLE IF EXISTS politicians"
    ),
    step(
        "CREATE INDEX ix_politicians_id ON politicians (id)",
        "DROP INDEX IF EXISTS ix_politicians_id"
    )
]