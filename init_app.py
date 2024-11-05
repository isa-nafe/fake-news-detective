import nltk
import os
import time
from pathlib import Path
from utils.database import ArticleHistory, Base, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

def initialize_app():
    """Initialize all components needed for the application"""
    print("Starting application initialization...")
    
    # Set up NLTK data directory
    nltk_data_dir = Path.home() / 'nltk_data'
    nltk_data_dir.mkdir(parents=True, exist_ok=True)
    nltk.data.path.append(str(nltk_data_dir))
    
    # Download required NLTK resources with retry logic
    resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    for resource in resources:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Downloading {resource}...")
                nltk.download(resource, quiet=True, download_dir=str(nltk_data_dir))
                print(f"Successfully downloaded {resource}")
                break
            except Exception as e:
                print(f"Error downloading {resource} (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    print(f"Failed to download {resource} after {max_retries} attempts")
    
    # Initialize database with retry logic
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print("Initializing database...")
            # Test database connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                connection.commit()
            
            # Create table
            ArticleHistory.create_table()
            print("Database initialization successful!")
            return True
            
        except Exception as e:
            print(f"Database initialization attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("All database initialization attempts failed!")
                return False

if __name__ == "__main__":
    success = initialize_app()
    if not success:
        print("Initialization failed!")
        exit(1)
    print("Initialization completed successfully!")
