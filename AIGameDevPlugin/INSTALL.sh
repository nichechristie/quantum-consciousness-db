#!/bin/bash

echo "======================================"
echo "AI Game Dev Plugin - Installation"
echo "======================================"
echo ""

# Get project path
PROJECT_PATH="/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7"
PLUGIN_SOURCE="/Users/nicholechristie/quantum_consciousness_db/AIGameDevPlugin"

echo "Project: $PROJECT_PATH"
echo "Plugin Source: $PLUGIN_SOURCE"
echo ""

# Create Plugins directory if it doesn't exist
PLUGINS_DIR="$PROJECT_PATH/Plugins"

if [ ! -d "$PLUGINS_DIR" ]; then
    echo "Creating Plugins directory..."
    mkdir -p "$PLUGINS_DIR"
fi

# Copy plugin
DEST_PLUGIN="$PLUGINS_DIR/AIGameDevPlugin"

echo "Installing plugin..."
echo "From: $PLUGIN_SOURCE"
echo "To: $DEST_PLUGIN"
echo ""

# Remove old version if exists
if [ -d "$DEST_PLUGIN" ]; then
    echo "Removing old version..."
    rm -rf "$DEST_PLUGIN"
fi

# Copy plugin
cp -r "$PLUGIN_SOURCE" "$DEST_PLUGIN"

echo "✅ Plugin copied successfully!"
echo ""

# Check Python dependencies
echo "Checking Python dependencies..."
echo ""

# Try to find Unreal's Python
UE_PYTHON="/Applications/Epic Games/UE_5.7/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3"

if [ -f "$UE_PYTHON" ]; then
    echo "Found Unreal Engine Python at: $UE_PYTHON"

    # Check for required packages
    echo ""
    echo "Installing Python dependencies..."

    "$UE_PYTHON" -m pip install --upgrade pip
    "$UE_PYTHON" -m pip install aiohttp openai google-generativeai anthropic

    echo ""
    echo "✅ Python dependencies installed!"
else
    echo "⚠️  Could not find Unreal Engine Python"
    echo "Please install manually:"
    echo "  pip3 install aiohttp openai google-generativeai anthropic"
fi

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Next Steps:"
echo ""
echo "1. Open your Unreal Engine project"
echo "2. Go to Edit → Plugins"
echo "3. Search for 'AI Game Dev'"
echo "4. Enable the plugin"
echo "5. Enable 'Python Script Plugin' if not enabled"
echo "6. Restart Unreal Engine"
echo ""
echo "7. Set your API keys (in terminal):"
echo "   export OPENAI_API_KEY='your-key-here'"
echo "   export GOOGLE_API_KEY='your-key-here'"
echo ""
echo "8. Launch Unreal and access via:"
echo "   Window → AI Game Dev Tools"
echo ""
echo "Read README.md for full documentation!"
echo ""
