"""
Setup script untuk membuat struktur folder dan file __init__.py
Jalankan script ini untuk setup project secara otomatis
"""

import os
import sys

def create_directory_structure():
    """Create project directory structure"""
    
    directories = [
        'pages',
        'ml',
        'utils',
        'styles'
    ]
    
    print("🏗️  Creating directory structure...")
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created: {directory}/")
        else:
            print(f"   ⏭️  Already exists: {directory}/")
    
    print()

def create_init_files():
    """Create __init__.py files in all directories"""
    
    init_contents = {
        'pages': """# Pages module
from . import home, model, analysis, comparison, about

__all__ = ['home', 'model', 'analysis', 'comparison', 'about']
""",
        'ml': """# Machine Learning module
from .model_trainer import ModelTrainer, prepare_batch_data, split_data

__all__ = ['ModelTrainer', 'prepare_batch_data', 'split_data']
""",
        'utils': """# Utils module
from .session_manager import (
    init_session_state,
    save_model_results,
    get_model_results,
    clear_all_models,
    get_all_trained_models
)

__all__ = [
    'init_session_state',
    'save_model_results',
    'get_model_results',
    'clear_all_models',
    'get_all_trained_models'
]
""",
        'styles': """# Styles module
from .custom_css import get_custom_css

__all__ = ['get_custom_css']
"""
    }
    
    print("📝 Creating __init__.py files...")
    
    for directory, content in init_contents.items():
        init_file = os.path.join(directory, '__init__.py')
        
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Created: {init_file}")
        else:
            print(f"   ⏭️  Already exists: {init_file}")
    
    print()

def check_required_files():
    """Check if required main files exist"""
    
    required_files = {
        'app.py': 'Main application file',
        'requirements.txt': 'Dependencies file',
        'pages/home.py': 'Home page module',
        'pages/model.py': 'Model training page',
        'pages/analysis.py': 'Analysis page',
        'pages/comparison.py': 'Comparison page',
        'pages/about.py': 'About page',
        'ml/model_trainer.py': 'Model trainer module',
        'utils/session_manager.py': 'Session manager module',
        'styles/custom_css.py': 'Custom CSS module'
    }
    
    print("🔍 Checking required files...")
    
    missing_files = []
    
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"   ✅ Found: {file_path}")
        else:
            print(f"   ❌ Missing: {file_path} ({description})")
            missing_files.append(file_path)
    
    print()
    
    if missing_files:
        print("⚠️  WARNING: Some files are missing!")
        print("   Please ensure all required files are copied to the project directory.")
        print("\n   Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        print()
    else:
        print("✅ All required files found!")
        print()
    
    return len(missing_files) == 0

def create_gitignore():
    """Create .gitignore file"""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Data files
*.xlsx
*.csv
*.xls

# Logs
*.log
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
    else:
        print("⏭️  .gitignore already exists")
    
    print()

def print_next_steps():
    """Print next steps for user"""
    
    print("=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print()
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Run the application:")
    print("   streamlit run app.py")
    print()
    print("3. Open browser at:")
    print("   http://localhost:8501")
    print()
    print("📚 For more information, see:")
    print("   - README.md")
    print("   - QUICK_START.md")
    print()
    print("=" * 60)

def main():
    """Main setup function"""
    
    print("=" * 60)
    print("🚀 ML Dashboard - Automated Setup")
    print("=" * 60)
    print()
    
    # Create directories
    create_directory_structure()
    
    # Create __init__.py files
    create_init_files()
    
    # Create .gitignore
    create_gitignore()
    
    # Check required files
    all_files_present = check_required_files()
    
    # Print next steps
    if all_files_present:
        print_next_steps()
    else:
        print("⚠️  Please copy all required files before running the application.")
        print("   See the file list above for missing files.")
        print()
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during setup: {str(e)}")
        sys.exit(1)