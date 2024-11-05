import nltk
import os
from pathlib import Path

def download_nltk_data():
    # Set up NLTK data directory in the project folder
    nltk_data_dir = Path.home() / 'nltk_data'
    nltk_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Add the directory to NLTK's data path
    nltk.data.path.append(str(nltk_data_dir))
    
    # Required NLTK resources
    resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    
    # Download all required resources
    for resource in resources:
        try:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True, download_dir=str(nltk_data_dir))
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Error downloading {resource}: {str(e)}")

if __name__ == "__main__":
    download_nltk_data()
