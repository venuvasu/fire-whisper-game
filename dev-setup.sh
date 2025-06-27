#!/bin/bash
# Fire Whisper RPG - Complete Development Setup

echo "🔥 Fire Whisper RPG - Development Setup"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is required but not installed."
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
fi

echo "✅ pip found: $(python3 -m pip --version)"

# Install Python backend dependencies
echo ""
echo "📦 Installing Python dependencies..."
python3 -m pip install -r backend/requirements.txt

# Install additional required packages for development
echo "📦 Installing development packages..."
python3 -m pip install python-dotenv

# Check if Node.js is installed (optional for frontend)
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
    echo "✅ npm found: $(npm --version)"
    
    # Install frontend dependencies if frontend exists
    if [ -d "frontend" ]; then
        echo ""
        echo "🎨 Installing frontend dependencies..."
        cd frontend
        npm install
        cd ..
    fi
else
    echo "⚠️  Node.js not found. Frontend development will not be available."
    echo "   Install Node.js from: https://nodejs.org/"
fi

# Set up environment variables
echo ""
echo "🔧 Setting up environment configuration..."

# Check if .env.local already exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local from template..."
    cp .env.example .env.local
    echo "⚠️  Please edit .env.local and add your Claude API key!"
else
    echo "✅ .env.local already exists"
fi

# Make scripts executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py
chmod +x tests/automation/*.py

# Check AWS CLI (optional for AWS deployment)
if command -v aws &> /dev/null; then
    echo "✅ AWS CLI found: $(aws --version)"
else
    echo "⚠️  AWS CLI not found. AWS deployment will not be available."
    echo "   Install from: https://aws.amazon.com/cli/"
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🚀 Quick Start Commands:"
echo ""
echo "📝 1. Configure your API key:"
echo "   Edit .env.local and add your CLAUDE_API_KEY"
echo ""
echo "🎮 2. Test the game locally:"
echo "   python3 scripts/local_runner.py"
echo ""
echo "🧪 3. Run tests:"
echo "   python3 tests/automation/test_runner.py"
echo ""
echo "🏷️  4. Check version:"
echo "   python3 scripts/version_manager.py info"
echo ""
echo "☁️  5. Deploy to AWS (optional):"
echo "   python3 scripts/aws_deploy.py"
echo ""
echo "🔥 Ready to develop Fire Whisper RPG!"