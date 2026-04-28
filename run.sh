#!/bin/bash

# Marshall Defense Database - Quick Start Script for macOS/Linux

echo "=========================================="
echo "🛡️  MARSHALL DEFENSE DATABASE"
echo "=========================================="
echo ""

# Check Python
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Initialize database
echo ""
echo "🌐 Scraping and populating database..."
python scripts/populate_db.py --action populate

# Add sample scores
echo ""
echo "📊 Adding sample readiness scores..."
python scripts/populate_db.py --action add-scores

# Start server
echo ""
echo "=========================================="
echo "🚀 Starting FastAPI Server"
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  🌐 http://localhost:8000"
echo "  📚 http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
