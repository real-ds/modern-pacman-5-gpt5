#!/bin/bash

echo "🎮 Building PAC-MAN for Web Deployment..."
echo "========================================"

# Check if pygbag is installed
if ! python -m pygbag --version &> /dev/null; then
    echo "❌ Pygbag not found. Installing..."
    pip install pygbag --break-system-packages
fi

# Create build directory if it doesn't exist
mkdir -p build

echo "📦 Copying game files..."
# Copy necessary files to build directory
cp main.py build/ 2>/dev/null || :
cp -r src build/ 2>/dev/null || :
cp -r assets build/ 2>/dev/null || :
cp requirements.txt build/ 2>/dev/null || :

echo "🔨 Building with Pygbag..."
# Build with Pygbag
cd build
python -m pygbag .

echo ""
echo "✅ Build complete!"
echo ""
echo "📱 To test locally:"
echo "   1. Navigate to the build directory"
echo "   2. Run: python -m http.server 8000"
echo "   3. Open http://localhost:8000 in your browser"
echo ""
echo "🌐 To deploy:"
echo "   - Upload the build/ directory to your web host"
echo "   - Works with GitHub Pages, Netlify, Vercel, etc."
echo ""
echo "🎉 Happy gaming!"
