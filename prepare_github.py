import os
from pathlib import Path

def verify_repository():
    """Verify all required files are present"""
    required_files = [
        'README.md',
        'requirements.txt',
        '.gitignore',
        'main.py',
        'start_server.py',
        'init_app.py',
        'download_nltk_data.py',
        'utils/analyzer.py',
        'utils/database.py',
        'utils/preprocessor.py',
        'utils/source_checker.py',
        '.streamlit/config.toml'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"- {file}")
        return False
        
    print("✅ All required files present")
    return True

def verify_ignore_patterns():
    """Verify .gitignore contains all necessary patterns"""
    required_patterns = [
        '__pycache__',
        '*.pyc',
        'venv',
        '.env',
        '.streamlit/secrets.toml',
        'nltk_data',
        '*.sqlite',
        '*.db',
        '.replit',
        'replit.nix'
    ]
    
    with open('.gitignore', 'r') as f:
        content = f.read()
        
    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in content:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print("Missing .gitignore patterns:")
        for pattern in missing_patterns:
            print(f"- {pattern}")
        return False
        
    print("✅ .gitignore patterns verified")
    return True

def main():
    """Main verification process"""
    print("Verifying repository for GitHub upload...")
    
    checks = [
        verify_repository(),
        verify_ignore_patterns()
    ]
    
    if all(checks):
        print("\n✅ Repository is ready for GitHub!")
        print("\nNext steps:")
        print("1. Create a new GitHub repository")
        print("2. Initialize git repository:")
        print("   git init")
        print("3. Add files:")
        print("   git add .")
        print("4. Create initial commit:")
        print("   git commit -m 'Initial commit'")
        print("5. Add remote repository:")
        print("   git remote add origin <repository-url>")
        print("6. Push to GitHub:")
        print("   git push -u origin main")
    else:
        print("\n❌ Please fix the issues above before proceeding")

if __name__ == "__main__":
    main()
