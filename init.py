import nltk
import os
from pathlib import Path
from utils.database import ArticleHistory

def initialize():
    # Set up NLTK data directory
    nltk_data_dir = Path.home() / 'nltk_data'
    nltk_data_dir.mkdir(parents=True, exist_ok=True)
    nltk.data.path.append(str(nltk_data_dir))
    
    # Download required NLTK resources
    resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True, download_dir=str(nltk_data_dir))
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Error downloading {resource}: {str(e)}")
    
    # Initialize database
    try:
        ArticleHistory.create_table()
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        raise e

if __name__ == "__main__":
    initialize()
