import streamlit as st

# Add page configuration at the start
st.set_page_config(
    page_title="Fake News Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.preprocessor import TextPreprocessor
from utils.analyzer import NewsAnalyzer
from utils.source_checker import SourceChecker
from utils.database import SessionLocal, ArticleHistory
import plotly.graph_objects as go
import trafilatura
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from datetime import datetime

def get_website_text_content(url: str) -> str:
    """Extract text content from a website URL with improved error handling"""
    try:
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return "Error: Invalid URL format. Please enter a complete URL (e.g., https://example.com)"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        downloaded = response.text

        text = trafilatura.extract(downloaded, include_comments=False, no_fallback=False)
        if text and len(text.strip()) > 100:
            return text

        soup = BeautifulSoup(downloaded, 'html.parser')
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()

        for selector in ['article', 'main', '.article-body', '.story-body']:
            content = soup.select_one(selector)
            if content:
                paragraphs = content.find_all('p')
                text = '\n'.join(p.get_text().strip() for p in paragraphs)
                if len(text.strip()) > 100:
                    return text

        return "Error: Could not extract meaningful content. Please paste the article text directly."

    except Exception as e:
        return f"Error: {str(e)}"

def create_gauge_chart(confidence, is_fake):
    color = 'red' if is_fake else 'green'
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Confidence Level"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 100], 'color': "gray"}
            ]
        }
    ))
    return fig

def show_guidelines():
    """Display guidelines for improving content credibility"""
    st.markdown("""
    ### 1. Content Quality Guidelines
    
    #### Writing Style
    - ✍️ Use clear, concise language
    - 🎯 Avoid sensationalized headlines or clickbait
    - 📝 Maintain a professional, objective tone
    - ❌ Avoid excessive punctuation (!!!) or ALL CAPS
    
    #### Sources and Citations
    - 📚 Include references to credible sources
    - 🔗 Link to original research or data
    - 👥 Quote experts and provide their credentials
    - 📊 Include relevant statistics with proper attribution
    
    #### Content Structure
    - 📋 Present a balanced perspective
    - 🔍 Include context and background information
    - 📅 Provide dates and timelines
    - 🌐 Specify geographical locations when relevant
    """)

def main():
    st.title("🔍 Fake News Detective")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Analysis Tool", "History", "Guidelines", "How It Works", "Access Guide"])
    
    with tab1:
        st.markdown("""
        ### How it works
        1. Enter an article URL or paste the text directly
        2. Our AI will analyze the content
        3. Get detailed insights about credibility
        """)
        
        input_method = st.radio("Choose input method:", ["Enter URL", "Paste Text"])
        article_text = ""
        source_credibility = None
        url = ""
        
        if input_method == "Enter URL":
            url = st.text_input("Enter article URL:")
            if url:
                with st.spinner("Fetching article..."):
                    article_text = get_website_text_content(url)
                    if article_text.startswith("Error"):
                        st.error(article_text)
                        article_text = ""
                    else:
                        st.success("Article fetched successfully!")
                        with st.expander("View extracted text"):
                            st.text(article_text)
                            
                        source_credibility = source_checker.check_source_credibility(url)
        else:
            article_text = st.text_area("Paste your article text here:", height=200)
        
        if st.button("Analyze"):
            if article_text:
                try:
                    with st.spinner("Analyzing..."):
                        # Process and analyze text
                        cleaned_text = preprocessor.clean_text(article_text)
                        results = analyzer.analyze_text(cleaned_text)
                        
                        # Save to history
                        db = SessionLocal()
                        try:
                            title = article_text.split('\n')[0][:100]
                            ArticleHistory.add_entry(
                                session=db,
                                title=title,
                                content=article_text[:1000],
                                url=url,
                                is_fake=results['is_fake'],
                                confidence_score=results['confidence'],
                                source_credibility_score=source_credibility['credibility_score'] if source_credibility else None
                            )
                        finally:
                            db.close()
                        
                        # Display results
                        st.header("Analysis Results")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            verdict = "🚫 Likely Fake News" if results['is_fake'] else "✅ Likely Genuine News"
                            st.write(f"**Verdict:** {verdict}")
                            st.plotly_chart(create_gauge_chart(results['confidence'], results['is_fake']))
                        
                        if source_credibility:
                            with col2:
                                st.write("**Source Credibility:**")
                                st.write(f"Score: {source_credibility['credibility_score']:.1f}%")
                                st.write(source_credibility['details'])
                        
                        st.subheader("Content Indicators")
                        for indicator, present in results['indicators'].items():
                            st.write(f"{'🚨' if present else '✅'} {indicator}")
                            
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
            else:
                st.warning("Please enter a URL or paste text to analyze.")
    
    with tab2:
        st.header("📋 Analysis History")
        db = SessionLocal()
        try:
            history = ArticleHistory.get_history(db)
            if not history:
                st.info("No analysis history yet. Start analyzing articles to see them here!")
            else:
                for idx, entry in enumerate(history):
                    with st.expander(f"{entry.title} - {entry.analysis_date.strftime('%Y-%m-%d %H:%M')}"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(f"**Verdict:** {'🚫 Fake News' if entry.is_fake else '✅ Genuine News'}")
                            st.write(f"**Confidence:** {entry.confidence_score:.1f}%")
                            if entry.source_credibility_score:
                                st.write(f"**Source Credibility:** {entry.source_credibility_score:.1f}%")
                            if entry.url:
                                st.write(f"**Source:** {entry.url}")
                        with col2:
                            st.write("**Content:**")
                            st.text_area("", 
                                value=entry.content,
                                height=200,
                                disabled=True,
                                key=f"history_content_{idx}"
                            )
        finally:
            db.close()
    
    with tab3:
        st.header("📚 Guidelines")
        show_guidelines()
        
    with tab4:
        st.header("ℹ️ How It Works")
        st.markdown("""
        Our Fake News Detection system uses a combination of advanced techniques to analyze content and determine its credibility:
        
        ### 1. Content Analysis
        - 🔍 Text preprocessing and cleaning
        - 📊 Statistical pattern recognition
        - 🎯 Sentiment and tone analysis
        - 🚩 Red flag detection
        
        ### 2. Source Evaluation
        - 🔒 SSL certificate verification
        - ⏰ Domain age checking
        - 🏢 Publisher credibility assessment
        - 🔗 URL pattern analysis
        
        ### 3. Statistical Indicators
        - 📈 Confidence scoring
        - 🎯 Accuracy metrics
        - 📊 Credibility factors
        - 🔄 Pattern matching
        """)
        
    with tab5:
        st.header("🌐 Access Guide")
        st.markdown("""
        ### Accessing the Application

        The Fake News Detective is hosted on Replit and can be accessed through your web browser.

        #### Access Details:
        - **URL**: The application is available at your Replit URL
        - **Port**: 8080 (configured automatically)
        - **Browser Support**: Compatible with all modern web browsers

        #### Usage Tips:
        1. **First Access**:
           - Click the provided Replit URL
           - The application will load in your browser
           - No additional configuration needed

        2. **Sharing Access**:
           - Share the Replit URL with others
           - They can access all features directly
           - No login required

        3. **Best Practices**:
           - Use a modern web browser
           - Enable JavaScript
           - Allow cookies for best experience

        4. **Troubleshooting**:
           - If the page doesn't load, try refreshing
           - Check your internet connection
           - Clear browser cache if needed

        ### Security Note:
        - This is a public web application
        - Do not share sensitive information
        - Use for educational and verification purposes only
        """)

if __name__ == "__main__":
    # Initialize components
    try:
        preprocessor = TextPreprocessor()
        analyzer = NewsAnalyzer()
        source_checker = SourceChecker()
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        st.stop()
    
    main()
