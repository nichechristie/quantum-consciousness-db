# AI Plugin Quick Start for WWYD Game

Get your biblical multiplayer game powered by AI in 5 minutes!

---

## Installation (2 minutes)

### Step 1: Run the installer

```bash
cd /Users/nicholechristie/quantum_consciousness_db/AIGameDevPlugin
./INSTALL.sh
```

This automatically:
- Copies plugin to your WWYD project
- Installs Python dependencies
- Sets up everything you need

### Step 2: Set API Key

```bash
export OPENAI_API_KEY='sk-proj-your-key-here'
```

Add to `~/.zshrc` to make permanent.

### Step 3: Enable in Unreal

1. Open WWYD project
2. Edit → Plugins
3. Enable "AI Game Dev Plugin"
4. Enable "Python Script Plugin"
5. Restart Unreal

---

## Generate All 14 Characters (1 minute)

Open Unreal Python console (Window → Developer Tools → Output Log → Python tab):

```python
import metahuman_generator
metahuman_generator.generate_all_disciples()
```

This creates MetaHuman specifications for:
- ✝️ Jesus Christ
- 👥 All 12 disciples
- ♀️ Mary Magdalene

Each character gets:
- Detailed specification document
- Blueprint in `/Game/MetaHumans/AI_Generated/`
- Historical accuracy (1st century Middle Eastern)
- Personality traits
- Physical descriptions

**Location:** Check `Documentation/AI_Generated_MetaHumans/` for spec files

---

## Generate Environment Props (1 minute)

```python
import prop_generator

# Temple items
prop_generator.quick_generate_props("ancient Jerusalem temple religious items", 15)

# Marketplace items
prop_generator.quick_generate_props("biblical marketplace pottery baskets fabrics", 20)

# Village items
prop_generator.quick_generate_props("1st century Galilean village furniture and tools", 25)
```

Props appear in your level, auto-arranged in a grid!

---

## Generate Game Systems (1 minute)

```python
import blueprint_generator

# Faith system
blueprint_generator.quick_generate_blueprint(
    "faith power system that increases near Jesus and enables miracles for disciples",
    "ActorComponent"
)

# Healing system
blueprint_generator.quick_generate_blueprint(
    "divine healing system where disciples can heal other players by touch",
    "ActorComponent"
)

# Miracle system
blueprint_generator.quick_generate_system(
    "water to wine miracle - Jesus can turn water pots into wine, with visual effects and multiplayer sync"
)
```

Blueprints created at: `/Game/Blueprints/AI_Generated/`

---

## Quick Commands Reference

### Generate Single Prop
```python
import prop_generator
generator = prop_generator.PropGenerator()
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
prop = loop.run_until_complete(
    generator.generate_single_prop("stone water jar from Cana wedding")
)
loop.close()
```

### Generate Specific Character
```python
import metahuman_generator
judas = metahuman_generator.quick_generate_biblical_character("Judas Iscariot")
```

### Generate Custom Character
```python
import metahuman_generator
character = metahuman_generator.quick_generate_metahuman(
    "Roman centurion, age 35, battle-worn, stern but fair"
)
```

### Ask AI About Anything
```python
import ai_editor_panel
panel = ai_editor_panel.launch_ai_panel()
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
response = loop.run_until_complete(
    panel.send_message("How should I implement the faith power system?")
)
loop.close()
print(response)
```

---

## WWYD-Specific Examples

### Generate All Temple Props
```python
import prop_generator

temple_items = [
    "stone altar with carved details",
    "bronze menorah seven branches",
    "incense altar small bronze",
    "offering basin stone carved",
    "temple curtain rich fabric",
    "stone columns ornate capitals",
    "scroll storage wooden case",
    "oil lamp bronze multi-wick",
    "ceremonial basin large bronze",
    "stone tablets replica"
]

# Generate each as a unique prop
for item in temple_items:
    import asyncio
    generator = prop_generator.PropGenerator()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generator.generate_single_prop(item))
    loop.close()
```

### Generate Miracle Blueprints
```python
import blueprint_generator

miracles = [
    "water walking - allows Jesus to walk on water surface with visual effects",
    "storm calming - Jesus can calm weather with gesture and sound effects",
    "feeding 5000 - multiply fish and bread items in player inventories",
    "casting out demons - special ability to remove negative status effects",
    "raising dead - revival ability with unique animation and effects"
]

for miracle in miracles:
    blueprint_generator.quick_generate_blueprint(miracle, "ActorComponent")
```

### Generate NPC Crowd Characters
```python
import metahuman_generator
generator = metahuman_generator.MetaHumanGenerator()

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

crowd = [
    "Jewish merchant selling fabrics",
    "Roman soldier patrolling",
    "Elderly woman with basket",
    "Young boy shepherd",
    "Pharisee in traditional robes",
    "Tax collector at booth",
    "Fisherman with nets",
    "Temple priest in ceremonial dress"
]

loop.run_until_complete(generator.generate_multiple_characters(crowd))
loop.close()
```

---

## Workflow Tips

### 1. Generate Props First
Create environment props before placing them. The AI will arrange them in a grid, then you can move them manually to exact positions.

### 2. Generate Characters in Batches
Create all characters at once using `generate_all_disciples()` or batch functions. This ensures consistent style.

### 3. Use Specifications as Reference
The generated `.md` files contain detailed specs. Use these when creating actual MetaHumans in MetaHuman Creator.

### 4. Iterate on Blueprints
Generate a basic Blueprint, then ask AI to improve it:
```python
import ai_editor_panel
panel = ai_editor_panel.get_panel()
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
response = loop.run_until_complete(panel.send_message(
    "Improve the faith system Blueprint to include multiplayer synchronization"
))
loop.close()
print(response)
```

---

## Testing the Plugin

Run the test script:
```python
import test_plugin
test_plugin.test_plugin_installation()
```

Or quick test:
```python
import test_plugin
test_plugin.quick_test()
```

Run a demo:
```python
import test_plugin
test_plugin.demo_prop_generation()  # Generate 3 props
test_plugin.demo_metahuman()        # Generate Peter
```

---

## Troubleshooting

### "No module named 'ai_editor_panel'"
The plugin isn't installed or Python can't find it.

**Fix:**
```bash
cd /Users/nicholechristie/quantum_consciousness_db/AIGameDevPlugin
./INSTALL.sh
```
Then restart Unreal.

### "API key not found"
**Fix:**
```python
import os
os.environ['OPENAI_API_KEY'] = 'your-key-here'
```

### Connection Errors
Your API key might be invalid or out of credits.

**Check credits:**
- OpenAI: https://platform.openai.com/account/usage
- Get new key: https://platform.openai.com/api-keys

### Props Not Appearing
**Fix:**
```python
# Check if they were created
import unreal
actors = unreal.EditorLevelLibrary.get_all_level_actors()
ai_props = [a for a in actors if "AI_" in a.get_name()]
print(f"Found {len(ai_props)} AI-generated props")
```

---

## Performance Tips

### Rate Limiting
Don't generate too many items at once. Add delays:

```python
import asyncio
import prop_generator

generator = prop_generator.PropGenerator()

async def generate_with_delay():
    await generator.connect_ai()
    for i in range(10):
        await generator.generate_single_prop(f"biblical item {i+1}")
        await asyncio.sleep(5)  # Wait 5 seconds between each

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(generate_with_delay())
loop.close()
```

### Use Batch Functions
Batch functions are optimized:
```python
# Better - one request for 20 items
prop_generator.quick_generate_props("items", 20)

# Slower - 20 separate requests
for i in range(20):
    prop_generator.quick_generate_props("items", 1)
```

---

## Next Steps

1. **Generate all characters** → Use in MetaHuman Creator
2. **Generate environment props** → Populate levels
3. **Generate game systems** → Implement mechanics
4. **Ask AI for help** → Solve specific problems

Check the main README.md for complete documentation!

---

## Your Game Characters

The plugin will generate specifications for your 14 playable characters:

1. Jesus Christ (leader, can perform all miracles)
2. Peter (impulsive, strong faith)
3. Andrew (Peter's brother, missionary)
4. James (son of Zebedee, bold)
5. John (beloved disciple, writer)
6. Philip (practical, analytical)
7. Bartholomew (skeptical turned believer)
8. Matthew (former tax collector)
9. Thomas (doubting, needs proof)
10. James (son of Alphaeus, quiet)
11. Thaddaeus (asking questions)
12. Simon the Zealot (former revolutionary)
13. Judas Iscariot (betrayer, complex)
14. Mary Magdalene (devoted follower)

Each gets a unique, historically accurate MetaHuman specification!

---

Happy game development! 🎮✝️✨
