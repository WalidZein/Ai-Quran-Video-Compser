#!/bin/bash

# AI Quran Video Composer Installation Script
# This script automates the installation process for Unix-based systems (macOS, Linux)

set -e  # Exit on any error

echo "🕌 AI Quran Video Composer - Installation Script"
echo "================================================"

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $python_version is not compatible. Please install Python 3.8 or higher."
    exit 1
fi

# Check FFmpeg
echo "📋 Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n1 | awk '{print $3}')
    echo "✅ FFmpeg $ffmpeg_version is installed"
else
    echo "❌ FFmpeg is not installed."
    echo "Please install FFmpeg first:"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  macOS: brew install ffmpeg"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg"
        echo "  CentOS/RHEL: sudo yum install ffmpeg"
    fi
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Get your API keys:"
echo "   - Pexels API: https://www.pexels.com/api/"
echo "   - OpenAI API: https://platform.openai.com/api-keys"
echo "3. Start Jupyter: jupyter notebook"
echo "4. Open video_gen.ipynb and follow the instructions"
echo ""
echo "🕌 Happy video creating!" 