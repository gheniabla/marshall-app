"""
Marshall Defense Database Setup and Launch Script
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")


def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', requirements_file
        ])
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def scrape_and_populate():
    """Scrape companies and populate database"""
    print("\n🌐 Scraping defense companies...")
    
    scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
    sys.path.insert(0, scripts_dir)
    
    from scripts.populate_db import populate_database_from_scraper
    
    try:
        populate_database_from_scraper()
        print("✓ Database populated with defense companies")
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        sys.exit(1)


def start_server():
    """Start FastAPI server"""
    print("\n🚀 Starting FastAPI server...")
    print("   Access at: http://localhost:8000")
    print("   API docs: http://localhost:8000/docs")
    print("\n   Press Ctrl+C to stop\n")
    
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app:app', '--reload', '--host', '0.0.0.0', '--port', '8000'
        ])
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")


def main():
    """Main setup and launch function"""
    print("=" * 60)
    print("🛡️  MARSHALL DEFENSE DATABASE")
    print("=" * 60)
    
    # Check Python
    check_python()
    
    # Install dependencies
    install_dependencies()
    
    # Scrape and populate
    scrape_and_populate()
    
    # Add sample scores
    print("\n📊 Adding sample readiness scores...")
    from scripts.populate_db import add_sample_scores
    add_sample_scores()
    
    # Start server
    start_server()


if __name__ == "__main__":
    main()
