from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection
SQLALCHEMY_DATABASE_URL = "postgresql://rohitbansal.eminence:5jTzG9BOduwr@ep-black-paper-64883215-pooler.us-east-2.aws.neon.tech/test?sslmode=require&channel_binding=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()