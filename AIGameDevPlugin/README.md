# AI Game Dev Plugin for Unreal Engine 5

Transform your Unreal Engine workflow with AI-powered tools directly integrated into the editor!

## Features

### 1. AI Chat Panel
- Interactive AI assistant inside Unreal Engine
- Ask questions about any game development topic
- Get instant code examples and solutions
- Multiple AI models supported (ChatGPT, Gemini, Claude)

### 2. Prop Generation from Prompts
- Type a description → Get a prop in your level
- Generate multiple props at once
- Automatic grid placement
- Perfect for rapid prototyping

**Example:**
```python
# In Unreal Python console:
import prop_generator
prop_generator.quick_generate_props("ancient biblical Middle Eastern environment", 20)
```

### 3. Blueprint Code Generation
- Describe what you want → Get Blueprint specifications
- Generate complete gameplay systems
- Create custom functions
- Auto-create Blueprint assets

**Example:**
```python
import blueprint_generator
blueprint_generator.quick_generate_blueprint("health system with damage and healing", "ActorComponent")
```

### 4. MetaHuman Generation
- Create MetaHumans from text descriptions
- Generate biblical/historical characters
- Detailed specification documents
- Ready-to-customize Blueprints

**Example:**
```python
import metahuman_generator
metahuman_generator.quick_generate_biblical_character("Peter")
# Or generate all disciples at once:
metahuman_generator.generate_all_disciples()
```

### 5. Context Menu Integration
- Right-click any asset
- "Ask AI" options
- Get analysis and suggestions
- Generate related assets

### 6. Auto-Placement System
- Generated items placed automatically
- Grid layout organization
- Smart positioning
- No manual placement needed

---

## Installation

### Step 1: Copy Plugin to Your Project

```bash
# Copy the AIGameDevPlugin folder to your project's Plugins directory
cp -r AIGameDevPlugin "/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7/Plugins/"
```

Or manually:
1. Open your Unreal Engine project folder
2. Create a `Plugins` folder if it doesn't exist
3. Copy `AIGameDevPlugin` into the `Plugins` folder

### Step 2: Install Python Dependencies

The plugin needs the AI connector libraries. Install them:

```bash
# Navigate to Unreal Engine's Python directory
cd "/Applications/Epic Games/UE_5.7/Engine/Binaries/ThirdParty/Python3/Mac/bin"

# Install required packages
./pip3 install aiohttp openai google-generativeai anthropic
```

Or if using your system Python with Unreal:

```bash
pip3 install aiohttp openai google-generativeai anthropic
```

### Step 3: Set API Keys

**Option A: Environment Variables (Recommended)**

Add to your `~/.zshrc`:

```bash
export OPENAI_API_KEY='sk-proj-your-key-here'
export GOOGLE_API_KEY='AIzaSy-your-key-here'
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

Then: `source ~/.zshrc`

**Option B: In Unreal Python Console**

Open Unreal Engine → Window → Developer Tools → Output Log → Python tab:

```python
import os
os.environ['OPENAI_API_KEY'] = 'your-key-here'
os.environ['GOOGLE_API_KEY'] = 'your-key-here'
```

### Step 4: Enable Plugin in Unreal

1. Open your Unreal Engine project
2. Go to Edit → Plugins
3. Search for "AI Game Dev"
4. Check the box to enable it
5. Restart Unreal Engine

### Step 5: Enable Python Plugin

1. In Edit → Plugins
2. Search for "Python"
3. Enable "Python Script Plugin"
4. Restart Unreal Engine

---

## Usage

### Opening the AI Panel

**Method 1: Main Menu**
- Window → AI Game Dev Tools

**Method 2: Toolbar**
- Click the "AI Tools" button in the toolbar

**Method 3: Python Console**
```python
import ai_editor_panel
ai_editor_panel.launch_ai_panel()
```

### Generating Props

**In Python Console:**

```python
# Generate 20 biblical props
import prop_generator
generator = prop_generator.PropGenerator()

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
props = loop.run_until_complete(
    generator.generate_props_batch("ancient Middle Eastern temple items", 20)
)
loop.close()
```

**Quick function:**
```python
import prop_generator
props = prop_generator.quick_generate_props("biblical furniture and decorations", 10)
```

### Generating Blueprints

```python
import blueprint_generator

# Generate a single Blueprint
bp = blueprint_generator.quick_generate_blueprint(
    "inventory system with pickup and drop",
    "ActorComponent"
)

# Generate a complete system
system = blueprint_generator.quick_generate_system(
    "faith power system that increases when near Jesus"
)
```

### Generating MetaHumans

```python
import metahuman_generator

# Generate a custom character
mh = metahuman_generator.quick_generate_metahuman(
    "elderly wise teacher with gray beard and kind eyes"
)

# Generate a biblical character
peter = metahuman_generator.quick_generate_biblical_character("Peter")

# Generate all disciples for WWYD game
all_characters = metahuman_generator.generate_all_disciples()
# This creates: Jesus, 12 disciples, and Mary Magdalene
```

### Using Context Menu

1. Right-click any asset in Content Browser
2. Select "Ask AI About This"
3. Get instant AI analysis

*(Context menu registration happens automatically)*

---

## For Your WWYD Game

Perfect for your biblical multiplayer game! Here's how:

### Generate All Characters

```python
import metahuman_generator
metahuman_generator.generate_all_disciples()
```

This creates MetaHuman specifications for:
- Jesus Christ
- All 12 disciples
- Mary Magdalene

Each character includes:
- Historically accurate appearance
- Cultural details (1st century Middle Eastern)
- Personality traits
- Complete specification document

### Generate Environment Props

```python
import prop_generator
prop_generator.quick_generate_props(
    "ancient Jerusalem marketplace items - pottery, baskets, fabrics, tools",
    30
)
```

### Create Game Systems

```python
import blueprint_generator

# Faith system
blueprint_generator.quick_generate_blueprint(
    "faith power system that tracks player's faith level and increases near Jesus",
    "ActorComponent"
)

# Healing system
blueprint_generator.quick_generate_blueprint(
    "divine healing ability that Jesus and disciples can use on players",
    "ActorComponent"
)
```

---

## Configuration

### Change AI Model

Default is ChatGPT. To use a different model:

```python
import ai_editor_panel
panel = ai_editor_panel.get_panel()

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(panel.initialize_ai("Gemini"))  # or "Claude"
loop.close()
```

### Adjust Prop Placement Spacing

```python
import prop_generator
generator = prop_generator.PropGenerator()
generator.organize_props_in_grid(props, spacing=500)  # 500cm spacing
```

---

## Troubleshooting

### "No module named 'aiohttp'"

Install Python dependencies:
```bash
pip3 install aiohttp openai google-generativeai anthropic
```

### "API key not found"

Set environment variables:
```bash
export OPENAI_API_KEY='your-key'
```

Or set in Python console before using:
```python
import os
os.environ['OPENAI_API_KEY'] = 'your-key-here'
```

### "Failed to connect to AI"

Check:
1. API key is set correctly
2. Internet connection is active
3. API key has sufficient credits
4. No rate limits exceeded

### Plugin Doesn't Appear

1. Check plugin is in correct folder: `YourProject/Plugins/AIGameDevPlugin/`
2. Restart Unreal Engine
3. Enable Python Script Plugin
4. Check Edit → Plugins → AI Game Dev is enabled

### Python Scripts Not Running

1. Enable Python Script Plugin
2. Check Output Log for Python errors
3. Ensure Python path includes plugin directory

---

## Advanced Usage

### Custom Prop Attributes

```python
import prop_generator
generator = prop_generator.PropGenerator()

# Customize the prompt for more control
generator.ai_connector.send_message("""
Create 5 stone water jars like those from the Cana wedding miracle.
Each should be slightly different in size and weathering.
""")
```

### Batch MetaHuman Generation

```python
import metahuman_generator
generator = metahuman_generator.MetaHumanGenerator()

characters = [
    "Roman centurion in armor",
    "Jewish merchant",
    "Temple priest",
    "Young shepherd boy",
    "Elderly woman vendor"
]

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
results = loop.run_until_complete(
    generator.generate_multiple_characters(characters)
)
loop.close()
```

### Complex Blueprint Systems

```python
import blueprint_generator
generator = blueprint_generator.BlueprintGenerator()

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
system = loop.run_until_complete(generator.generate_gameplay_system("""
Complete miracle system where:
- Jesus can turn water to wine
- Disciples can perform healing
- Players witness miracles and gain faith
- Miracles have visual effects
- Multiplayer synchronized
"""))
loop.close()
```

---

## File Structure

```
AIGameDevPlugin/
├── AIGameDevPlugin.uplugin          # Plugin definition
├── README.md                         # This file
├── Source/
│   └── AIGameDevPlugin/
│       ├── Public/
│       │   └── AIGameDevPlugin.h    # Plugin header
│       ├── Private/
│       │   └── AIGameDevPlugin.cpp  # Plugin implementation
│       └── AIGameDevPlugin.Build.cs # Build configuration
└── Content/
    └── Python/
        ├── ai_editor_panel.py       # Main AI panel
        ├── ai_connectors.py         # AI service connections
        ├── prop_generator.py        # Prop generation
        ├── blueprint_generator.py   # Blueprint generation
        ├── metahuman_generator.py   # MetaHuman generation
        └── context_menu_integration.py  # Context menu
```

---

## API Keys

### Get Your API Keys

**OpenAI (ChatGPT)**
- https://platform.openai.com/api-keys
- Free tier: $5 credit for 3 months
- Pay-as-you-go: ~$0.002 per request

**Google (Gemini)**
- https://makersuite.google.com/app/apikey
- Free tier: 60 requests/minute
- Very generous free limits

**Anthropic (Claude)**
- https://console.anthropic.com/
- Requires billing setup
- $5 minimum deposit

### Keep Keys Secure

- Never commit API keys to git
- Use environment variables
- Don't share keys publicly
- Rotate keys periodically

---

## Support

### Getting Help

1. Check Output Log for errors
2. Enable Python debugging
3. Test AI connection separately
4. Verify API key is working

### Common Issues

**Rate Limits**: Wait 60 seconds between large batches
**Connection Errors**: Check internet and API key
**Import Errors**: Install Python dependencies
**Plugin Not Loading**: Check UE5 version compatibility

---

## Version History

**v1.0** - Initial Release
- AI chat panel
- Prop generation
- Blueprint generation
- MetaHuman generation
- Context menu integration
- Auto-placement system

---

## Credits

Built with:
- Unreal Engine 5.7
- OpenAI API (ChatGPT)
- Google Generative AI (Gemini)
- Anthropic API (Claude)
- Python 3

Created for the WWYD biblical adventure game.

---

## License

MIT License - Feel free to use and modify for your projects!

---

## Quick Reference

**Generate Props:**
```python
import prop_generator
prop_generator.quick_generate_props("description", count)
```

**Generate Blueprint:**
```python
import blueprint_generator
blueprint_generator.quick_generate_blueprint("description", "ParentClass")
```

**Generate MetaHuman:**
```python
import metahuman_generator
metahuman_generator.quick_generate_metahuman("description")
```

**Generate Biblical Character:**
```python
import metahuman_generator
metahuman_generator.quick_generate_biblical_character("Peter")
```

---

Made with AI for AI-powered game development! 🤖🎮✨
