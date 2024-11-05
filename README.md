# 🔍 Fake News Detective

## Overview
A sophisticated fake news detection website built using Streamlit and Natural Language Processing (NLP) techniques. The application helps users analyze news articles and determine their credibility through multiple analysis methods.

## Features
1. **Content Analysis**
   - Text preprocessing and cleaning using NLTK
   - Statistical pattern recognition for fake news indicators
   - Sentiment and tone analysis
   - Machine learning-based classification
   - Confidence scoring with visual representation

2. **Source Credibility**
   - Domain verification against known credible/fake news sources
   - SSL certificate validation
   - Website age checking using WHOIS
   - Suspicious pattern detection in URLs
   - Comprehensive credibility scoring system

3. **History Tracking**
   - Automatic saving of analyzed articles
   - Chronological view of analysis history
   - Track credibility patterns over time
   - Detailed result storage in PostgreSQL

4. **User Interface**
   - Clean, intuitive Streamlit-based design
   - Dual input methods (URL/text)
   - Interactive visualization of results
   - Detailed analysis breakdowns
   - Real-time processing feedback

## Installation & Setup
1. Prerequisites
   - Python 3.8+
   - PostgreSQL database
   - Required Python packages:
     - streamlit
     - nltk
     - sqlalchemy
     - psycopg2-binary
     - beautifulsoup4
     - requests
     - python-whois
     - trafilatura
     - plotly

2. Environment Setup
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/fake-news-detective.git
   cd fake-news-detective
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Initialize NLTK resources
   python download_nltk_data.py
   ```

3. Configuration
   Required environment variables:
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   PGDATABASE=your_database_name
   PGUSER=your_database_user
   PGPASSWORD=your_database_password
   PGHOST=your_database_host
   PGPORT=your_database_port
   ```

## Usage Guide
1. **Starting the Application**
   ```bash
   python start_app.py
   ```
   The application will be available at `http://localhost:5000`

2. **Analyzing Articles**
   - **URL Analysis**: 
     1. Enter the article URL
     2. Click "Analyze"
     3. Review source credibility and content analysis
   
   - **Text Analysis**:
     1. Paste article text
     2. Click "Analyze"
     3. Review content analysis results

   - **Understanding Results**:
     - Credibility Score: 0-100 scale
     - Confidence Level: Gauge visualization
     - Source Analysis: Detailed breakdown
     - Content Indicators: Specific red flags

3. **Using Features**
   - **Content Analysis**: Automated analysis of writing style, patterns, and indicators
   - **Source Checking**: Domain age, SSL, reputation verification
   - **History Tracking**: Access past analyses in the History tab
   - **Guidelines**: Best practices for content credibility

## Technical Details
1. **Architecture**
   - **Frontend**: Streamlit web interface
   - **Backend**: Python-based processing pipeline
   - **Database**: PostgreSQL for persistent storage
   - **Components**:
     - TextPreprocessor: NLTK-based text cleaning
     - NewsAnalyzer: Content analysis
     - SourceChecker: URL and domain verification
     - ArticleHistory: Database operations

2. **Technologies Used**
   - **Streamlit**: Web interface and data visualization
   - **NLTK**: Natural language processing
   - **SQLAlchemy**: Database ORM
   - **Trafilatura**: Web content extraction
   - **Plotly**: Interactive visualizations
   - **BeautifulSoup4**: HTML parsing
   - **Whois**: Domain information retrieval

3. **Security Features**
   - SSL certificate verification for sources
   - Database connection encryption
   - Input sanitization
   - Error handling and validation
   - Secure environment variable management

## Troubleshooting
Common issues and solutions:

1. **Database Connection**
   - Verify PostgreSQL is running
   - Check environment variables
   - Ensure network connectivity

2. **NLTK Resources**
   - Run `python download_nltk_data.py`
   - Check NLTK data directory permissions
   - Verify internet connection

3. **URL Analysis**
   - Ensure valid URL format
   - Check website accessibility
   - Verify content extraction

## Development
Guidelines for contributors:

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Add docstrings for functions
   - Maintain modular architecture

2. **Testing**
   - Write unit tests
   - Test edge cases
   - Verify database operations
   - Check error handling

3. **Contributing**
   - Fork the repository
   - Create feature branch
   - Submit pull request
   - Add tests for new features

## License
MIT License

Copyright (c) 2024 Fake News Detective

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
