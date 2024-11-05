from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, IntegrityError
import sqlalchemy
import os
from datetime import datetime
import time

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# Create engine with proper SSL and connection pooling settings
engine = create_engine(
    DATABASE_URL,
    connect_args={
        'sslmode': 'prefer'
    },
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

class ArticleHistory(Base):
    __tablename__ = "article_history"

    id = Column(Integer, primary_key=True, server_default=text("nextval('article_history_id_seq'::regclass)"))
    title = Column(String(500))
    content = Column(Text)
    url = Column(String(1000))
    is_fake = Column(Boolean)
    confidence_score = Column(Float)
    source_credibility_score = Column(Float)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def create_table(cls):
        """Create or verify table and sequence"""
        try:
            inspector = inspect(engine)
            
            # Create sequence first (if not exists)
            with engine.begin() as connection:
                connection.execute(text("""
                    DO $$ 
                    BEGIN
                        CREATE SEQUENCE IF NOT EXISTS article_history_id_seq
                        START WITH 1
                        INCREMENT BY 1
                        NO MINVALUE
                        NO MAXVALUE
                        CACHE 1;
                    EXCEPTION WHEN duplicate_table THEN
                        NULL;
                    END $$;
                """))
            
            # Create table if it doesn't exist
            if not inspector.has_table(cls.__tablename__):
                with engine.begin() as connection:
                    connection.execute(text("""
                        CREATE TABLE IF NOT EXISTS article_history (
                            id INTEGER PRIMARY KEY DEFAULT nextval('article_history_id_seq'),
                            title VARCHAR(500),
                            content TEXT,
                            url VARCHAR(1000),
                            is_fake BOOLEAN,
                            confidence_score FLOAT,
                            source_credibility_score FLOAT,
                            analysis_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                print("Table created successfully")
            else:
                print("Table already exists")
                
        except Exception as e:
            print(f"Error in table creation: {str(e)}")
            raise e

    @classmethod
    def add_entry(cls, session, title, content, url, is_fake, confidence_score, source_credibility_score):
        """Add a new entry with proper error handling and retry logic"""
        max_retries = 3
        retry_delay = 1
        last_error = None
        
        for attempt in range(max_retries):
            try:
                entry = cls(
                    title=(title or "")[:500],
                    content=(content or "")[:1000],
                    url=(url or "")[:1000],
                    is_fake=bool(is_fake),
                    confidence_score=float(confidence_score),
                    source_credibility_score=float(source_credibility_score) if source_credibility_score is not None else None,
                    analysis_date=datetime.utcnow()
                )
                session.add(entry)
                session.flush()  # Test the insert before committing
                session.commit()
                return entry
                
            except Exception as e:
                last_error = e
                session.rollback()
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying... Error: {str(e)}")
                    time.sleep(retry_delay)
                    continue
                break
                
        print(f"Failed to add entry after {max_retries} attempts")
        raise last_error

    @classmethod
    def get_history(cls, session, limit=50):
        """Get history with proper error handling"""
        try:
            return session.query(cls).order_by(cls.analysis_date.desc()).limit(limit).all()
        except Exception as e:
            print(f"Error retrieving history: {str(e)}")
            return []
