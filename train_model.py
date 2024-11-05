import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

# Sample dataset for demonstration
# In real application, this would be loaded from a proper dataset file
fake_news = [
    "SHOCKING: Scientists discover miracle cure that big pharma doesn't want you to know!!!",
    "You won't BELIEVE what this celebrity did next! Click to find out!",
    "BREAKING: Government hiding aliens in secret underground facility!!!",
    "Secret society controls world economy - EXPOSED!!!",
    "Doctors HATE this one weird trick to lose weight instantly!"
]

real_news = [
    "New study shows benefits of regular exercise on mental health",
    "Local community center opens after renovation",
    "Scientists publish findings on climate change impact",
    "Tech company announces new smartphone model for next year",
    "Recent economic report shows steady job growth"
]

# Create labels (1 for fake, 0 for real)
X = fake_news + real_news
y = np.array([1] * len(fake_news) + [0] * len(real_news))

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Initialize TfidfVectorizer and transform the text data
vectorizer = TfidfVectorizer(max_features=5000)
X_vectorized = vectorizer.fit_transform(X)

# Train the model
model = LogisticRegression(random_state=42)
model.fit(X_vectorized, y)

# Create a dictionary containing both the model and vectorizer
model_components = {
    'model': model,
    'vectorizer': vectorizer
}

# Save the model and vectorizer
with open('models/fake_news_model.pkl', 'wb') as f:
    pickle.dump(model_components, f)

print("Model trained and saved successfully!")
