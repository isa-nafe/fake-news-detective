from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
import os

class NewsAnalyzer:
    def __init__(self):
        # Load pre-trained model and vectorizer
        model_path = os.path.join('models', 'fake_news_model.pkl')
        with open(model_path, 'rb') as f:
            model_components = pickle.load(f)
            self.model = model_components['model']
            self.vectorizer = model_components['vectorizer']
    
    def get_credibility_indicators(self, text):
        # Extract features that might indicate fake news
        indicators = {
            'Emotional Language': self._check_emotional_language(text),
            'Clickbait Style': self._check_clickbait(text),
            'Excessive Punctuation': self._check_punctuation(text)
        }
        return indicators
    
    def _check_emotional_language(self, text):
        emotional_words = ['shocking', 'incredible', 'amazing', 'unbelievable']
        count = sum(1 for word in text.lower().split() if word in emotional_words)
        return count > 0
    
    def _check_clickbait(self, text):
        clickbait_patterns = ['you won\'t believe', 'shocking truth', 'what happens next']
        return any(pattern in text.lower() for pattern in clickbait_patterns)
    
    def _check_punctuation(self, text):
        return text.count('!') > 2 or text.count('?') > 2

    def analyze_text(self, text):
        # Transform text using TF-IDF
        text_vectorized = self.vectorizer.transform([text])
        
        # Get prediction probability
        probability = self.model.predict_proba(text_vectorized)[0]
        
        # Get credibility indicators
        indicators = self.get_credibility_indicators(text)
        
        # Calculate confidence level
        confidence = max(probability) * 100
        
        # Determine if the text is likely fake news
        is_fake = probability[1] > 0.5
        
        return {
            'is_fake': is_fake,
            'confidence': confidence,
            'indicators': indicators
        }
