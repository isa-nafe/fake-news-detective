import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os
from pathlib import Path

class TextPreprocessor:
    def __init__(self):
        # Set up NLTK data directory in the project folder
        self.nltk_data_dir = Path.home() / 'nltk_data'
        self.nltk_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Add the directory to NLTK's data path
        nltk.data.path.append(str(self.nltk_data_dir))
        
        # Required NLTK resources
        self.required_resources = {
            'tokenizers/punkt': 'punkt',
            'corpora/stopwords': 'stopwords',
            'corpora/wordnet': 'wordnet',
            'taggers/averaged_perceptron_tagger': 'averaged_perceptron_tagger'
        }
        
        # Download and verify all required resources
        self._ensure_nltk_resources()
        
        # Initialize components
        try:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            print("NLTK components initialized successfully")
        except Exception as e:
            print(f"Warning: Failed to initialize NLTK components: {str(e)}")
            self.lemmatizer = None
            self.stop_words = set()

    def _ensure_nltk_resources(self):
        """Ensure all required NLTK resources are available"""
        for resource_path, resource_name in self.required_resources.items():
            try:
                # Check if resource exists
                nltk.data.find(resource_path)
            except LookupError:
                try:
                    # Download missing resource
                    print(f"Downloading NLTK resource: {resource_name}")
                    nltk.download(resource_name, download_dir=str(self.nltk_data_dir), quiet=True)
                except Exception as e:
                    print(f"Error downloading {resource_name}: {str(e)}")

    def clean_text(self, text):
        """Clean and preprocess the input text with fallback options"""
        if not text:
            return ""
            
        try:
            # Convert to lowercase and clean text
            text = text.lower()
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Tokenization with fallback
            try:
                tokens = word_tokenize(text)
            except LookupError:
                print("Falling back to basic tokenization")
                tokens = text.split()
            
            # Lemmatization and stopword removal if available
            if self.lemmatizer and self.stop_words:
                tokens = [
                    self.lemmatizer.lemmatize(token)
                    for token in tokens
                    if token not in self.stop_words
                ]
            else:
                # Basic cleaning if NLTK components are not available
                tokens = [token for token in tokens if len(token) > 2]
            
            return ' '.join(tokens)
        except Exception as e:
            print(f"Warning: Text preprocessing error: {str(e)}")
            # Ultimate fallback: basic cleaning
            return ' '.join(text.split())
