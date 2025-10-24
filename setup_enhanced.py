"""
Quick Setup and Test Script for Enhanced Features
Creates necessary directories and runs a test workflow
"""

import os
import sys
from pathlib import Path

def setup_directories():
    """Create required directory structure."""
    base_dir = Path("./storage")
    
    directories = [
        base_dir / "sessions",
        base_dir / "memory" / "longterm",
        base_dir / "memory" / "templates",
        base_dir / "archive",
        base_dir / "logs" / "errors",
        base_dir / "cache",
        base_dir / "results"
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")
    
    print("\n✅ Directory structure created successfully!\n")


def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")
    
    required_packages = {
        'flask': 'Flask',
        'loguru': 'loguru',
        'yaml': 'PyYAML',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies satisfied!\n")
    return True


def create_env_template():
    """Create .env template if it doesn't exist."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("Creating .env template...")
        with open(env_file, 'w') as f:
            f.write("# Google Gemini API Key\n")
            f.write("GOOGLE_API_KEY=your_api_key_here\n")
            f.write("\n# Optional: Configure log level\n")
            f.write("LOG_LEVEL=INFO\n")
        print("✓ Created .env template")
        print("  Please add your GOOGLE_API_KEY to the .env file\n")
    else:
        print("✓ .env file already exists\n")


def run_test_workflow():
    """Run a test workflow to verify setup."""
    print("="*80)
    print("RUNNING TEST WORKFLOW")
    print("="*80 + "\n")
    
    try:
        # Import after path setup
        from main_enhanced import main
        
        result = main()
        
        if result == 0:
            print("\n" + "="*80)
            print("✅ TEST WORKFLOW COMPLETED SUCCESSFULLY!")
            print("="*80)
            print("\nYou can now:")
            print("1. Run 'python main_enhanced.py' for command-line workflow")
            print("2. Run 'python adk_web.py' for web interface")
            print("3. Check './storage/sessions/' for session data")
            print("="*80 + "\n")
        else:
            print("\n⚠️  Test workflow completed with warnings")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Test workflow failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return 1


def main():
    """Main setup function."""
    print("\n" + "="*80)
    print("🚀 ENHANCED ADK MULTI-AGENT SYSTEM - SETUP")
    print("="*80 + "\n")
    
    # Step 1: Create directories
    setup_directories()
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing.")
        return 1
    
    # Step 3: Create .env template
    create_env_template()
    
    # Step 4: Ask user if they want to run test
    response = input("Would you like to run a test workflow? (y/n): ").strip().lower()
    
    if response == 'y':
        return run_test_workflow()
    else:
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Add your GOOGLE_API_KEY to .env file")
        print("2. Run 'python main_enhanced.py' to execute workflow")
        print("3. Run 'python adk_web.py' for web interface")
        print("\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
