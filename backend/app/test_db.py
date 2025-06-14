from backend.app.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

# Drop all tables
Base.metadata.drop_all(bind=engine)
