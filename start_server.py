import os
import sys
from pathlib import Path
import streamlit.web.bootstrap as bootstrap
from init_app import initialize_app

def main():
    """
    Main entry point for the Fake News Detective application.
    Handles initialization and server startup with proper configuration.
    """
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    # Configure Streamlit environment
    os.environ.update({
        'STREAMLIT_SERVER_PORT': '8080',
        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
        'STREAMLIT_SERVER_HEADLESS': 'true',
        'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
        'STREAMLIT_SERVER_ENABLE_CORS': 'true',
        'STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION': 'false',
        'STREAMLIT_GLOBAL_DEVELOPMENT_MODE': 'false',
        'STREAMLIT_GLOBAL_SHOW_WARNING_ON_DIRECT_EXECUTION': 'false',
        'STREAMLIT_THEME_BASE': 'light',
        'STREAMLIT_THEME_PRIMARY_COLOR': '#FF4B4B'
    })
    
    # Initialize application
    print("Initializing application...")
    if not initialize_app():
        print("Failed to initialize application")
        sys.exit(1)
    
    print("Starting Streamlit server...")
    try:
        flag_options = {
            'server.port': 8080,
            'server.address': '0.0.0.0',
            'server.headless': True,
            'server.enableCORS': True,
            'server.enableXsrfProtection': False,
            'browser.serverAddress': '0.0.0.0',
            'browser.serverPort': 8080,
            'global.developmentMode': False,
            'global.showWarningOnDirectExecution': False,
            'theme.base': 'light',
            'theme.primaryColor': '#FF4B4B'
        }
        
        # Run the Streamlit application with corrected arguments
        bootstrap.run(
            file=__file__,
            command_line="streamlit run main.py",
            args=[],
            flag_options=flag_options
        )
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
