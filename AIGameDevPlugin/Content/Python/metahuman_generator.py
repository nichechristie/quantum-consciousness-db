"""
MetaHuman Generation System
Creates MetaHuman characters from text prompts using AI
"""

import unreal
import asyncio
from ai_connectors import AIConnectorFactory


class MetaHumanGenerator:
    """Generate MetaHuman characters from natural language descriptions"""

    def __init__(self):
        self.ai_connector = None

    async def connect_ai(self, ai_name="ChatGPT"):
        """Connect to AI service"""
        self.ai_connector = AIConnectorFactory.create(ai_name)
        return await self.ai_connector.connect()

    async def generate_metahuman(self, description, character_name=None):
        """Generate MetaHuman specification from description"""
        if character_name is None:
            character_name = "MH_AIGenerated"

        unreal.log(f"👤 Generating MetaHuman: {description}")

        prompt = f"""Create a detailed MetaHuman character specification for Unreal Engine 5:

Character Description: {description}

Provide this JSON format:
{{
    "name": "{character_name}",
    "description": "{description}",
    "gender": "male|female",
    "age": 25,
    "ethnicity": "ethnicity description",
    "face": {{
        "face_shape": "oval|square|round|heart|diamond",
        "skin_tone": "fair|medium|olive|brown|dark",
        "skin_texture": "smooth|textured|aged",
        "wrinkles": "none|light|moderate|heavy",
        "freckles": "none|light|moderate|heavy",
        "facial_structure": {{
            "forehead": "narrow|average|wide",
            "cheekbones": "low|normal|high|prominent",
            "jawline": "soft|defined|strong|angular",
            "chin": "recessed|normal|prominent"
        }}
    }},
    "eyes": {{
        "eye_color": "blue|brown|green|hazel|gray",
        "eye_shape": "almond|round|hooded|monolid",
        "eye_size": "small|medium|large",
        "eyebrow_shape": "straight|arched|angled",
        "eyebrow_thickness": "thin|medium|thick"
    }},
    "nose": {{
        "nose_size": "small|medium|large",
        "nose_bridge": "low|medium|high",
        "nose_tip": "pointed|rounded|bulbous",
        "nostril_size": "small|medium|large"
    }},
    "mouth": {{
        "lip_size": "thin|medium|full",
        "lip_shape": "natural|bow|wide",
        "mouth_width": "narrow|medium|wide"
    }},
    "hair": {{
        "hair_style": "short|medium|long|bald",
        "hair_color": "black|brown|blonde|red|gray|white",
        "hair_type": "straight|wavy|curly|coily",
        "facial_hair": "none|stubble|beard|mustache|goatee",
        "facial_hair_style": "if applicable"
    }},
    "body": {{
        "body_type": "slim|athletic|average|heavy|muscular",
        "height": "short|average|tall",
        "proportions": "standard|custom"
    }},
    "clothing": {{
        "style": "casual|formal|sporty|traditional|fantasy",
        "description": "detailed clothing description"
    }},
    "personality_traits": [
        "trait1",
        "trait2",
        "trait3"
    ],
    "animation_style": "calm|energetic|confident|nervous|etc",
    "voice_type": "deep|medium|high|raspy|smooth"
}}"""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)

        # Parse MetaHuman specification
        mh_data = self._parse_metahuman_json(response)

        if mh_data:
            # Create MetaHuman Blueprint
            return self._create_metahuman_blueprint(mh_data)

        return None

    async def generate_biblical_character(self, character_name):
        """Generate a biblical character as MetaHuman"""
        unreal.log(f"✝️ Generating biblical character: {character_name}")

        prompt = f"""Create a historically and culturally accurate MetaHuman specification for the biblical character: {character_name}

Research the character from the Bible and provide accurate details based on:
- Historical Middle Eastern appearance (1st century AD)
- Their role and status in biblical narratives
- Cultural and regional characteristics
- Age and life stage when most depicted

Provide the detailed JSON format for MetaHuman creation with historically appropriate features."""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)
        mh_data = self._parse_metahuman_json(response)

        if mh_data:
            return self._create_metahuman_blueprint(mh_data)

        return None

    async def generate_multiple_characters(self, descriptions):
        """Generate multiple MetaHumans at once"""
        unreal.log(f"👥 Generating {len(descriptions)} MetaHumans...")

        characters = []
        for i, desc in enumerate(descriptions):
            char_name = f"MH_Character_{i+1}"
            mh = await self.generate_metahuman(desc, char_name)
            if mh:
                characters.append(mh)

            # Rate limiting
            if i < len(descriptions) - 1:
                await asyncio.sleep(3)

        unreal.log(f"✅ Created {len(characters)} MetaHumans!")
        return characters

    def _parse_metahuman_json(self, response):
        """Extract MetaHuman JSON from response"""
        import json
        import re

        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except Exception as e:
                unreal.log_error(f"Failed to parse MetaHuman JSON: {e}")

        return None

    def _create_metahuman_blueprint(self, mh_data):
        """Create MetaHuman Blueprint with specification"""
        char_name = mh_data.get('name', 'MH_AIGenerated')

        unreal.log(f"👤 Creating MetaHuman Blueprint: {char_name}")

        # Create Blueprint in /Game/MetaHumans/AI_Generated/
        blueprint_path = "/Game/MetaHumans/AI_Generated/"
        bp_name = f"BP_{char_name}"
        full_path = f"{blueprint_path}{bp_name}"

        # Ensure directory exists
        unreal.EditorAssetLibrary.make_directory(blueprint_path)

        # Check if already exists
        if unreal.EditorAssetLibrary.does_asset_exist(full_path):
            unreal.log_warning(f"MetaHuman Blueprint already exists: {full_path}")
            return unreal.EditorAssetLibrary.load_asset(full_path)

        # Create Blueprint based on Character class
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", unreal.Character)

        asset = asset_tools.create_asset(
            bp_name,
            blueprint_path,
            unreal.Blueprint,
            factory
        )

        if asset:
            unreal.log(f"✅ Created MetaHuman Blueprint: {full_path}")

            # Store complete specification as metadata
            import json
            spec_json = json.dumps(mh_data, indent=2)

            unreal.EditorAssetLibrary.set_metadata_tag(
                asset,
                "AI_Specification",
                spec_json
            )

            # Store description
            description = mh_data.get('description', 'AI Generated MetaHuman')
            unreal.EditorAssetLibrary.set_metadata_tag(
                asset,
                "Description",
                description
            )

            # Store character traits for quick reference
            if 'personality_traits' in mh_data:
                traits = ", ".join(mh_data['personality_traits'])
                unreal.EditorAssetLibrary.set_metadata_tag(
                    asset,
                    "Personality",
                    traits
                )

            # Save asset
            unreal.EditorAssetLibrary.save_asset(full_path)

            # Create a text file with full specification for manual MetaHuman creation
            self._create_specification_document(mh_data, blueprint_path)

            return asset

        unreal.log_error(f"❌ Failed to create MetaHuman Blueprint")
        return None

    def _create_specification_document(self, mh_data, save_path):
        """Create a text document with MetaHuman specifications"""
        import json
        import os

        char_name = mh_data.get('name', 'Character')

        # Create markdown document
        doc_content = f"""# MetaHuman Specification: {char_name}

## Overview
**Name:** {char_name}
**Description:** {mh_data.get('description', 'N/A')}
**Gender:** {mh_data.get('gender', 'N/A')}
**Age:** {mh_data.get('age', 'N/A')}
**Ethnicity:** {mh_data.get('ethnicity', 'N/A')}

---

## Face Details

### General
- **Face Shape:** {mh_data.get('face', {}).get('face_shape', 'N/A')}
- **Skin Tone:** {mh_data.get('face', {}).get('skin_tone', 'N/A')}
- **Skin Texture:** {mh_data.get('face', {}).get('skin_texture', 'N/A')}
- **Wrinkles:** {mh_data.get('face', {}).get('wrinkles', 'N/A')}
- **Freckles:** {mh_data.get('face', {}).get('freckles', 'N/A')}

### Facial Structure
"""
        if 'facial_structure' in mh_data.get('face', {}):
            struct = mh_data['face']['facial_structure']
            for key, value in struct.items():
                doc_content += f"- **{key.title()}:** {value}\n"

        doc_content += f"""
---

## Eyes
- **Color:** {mh_data.get('eyes', {}).get('eye_color', 'N/A')}
- **Shape:** {mh_data.get('eyes', {}).get('eye_shape', 'N/A')}
- **Size:** {mh_data.get('eyes', {}).get('eye_size', 'N/A')}
- **Eyebrow Shape:** {mh_data.get('eyes', {}).get('eyebrow_shape', 'N/A')}
- **Eyebrow Thickness:** {mh_data.get('eyes', {}).get('eyebrow_thickness', 'N/A')}

---

## Nose
- **Size:** {mh_data.get('nose', {}).get('nose_size', 'N/A')}
- **Bridge:** {mh_data.get('nose', {}).get('nose_bridge', 'N/A')}
- **Tip:** {mh_data.get('nose', {}).get('nose_tip', 'N/A')}
- **Nostril Size:** {mh_data.get('nose', {}).get('nostril_size', 'N/A')}

---

## Mouth
- **Lip Size:** {mh_data.get('mouth', {}).get('lip_size', 'N/A')}
- **Lip Shape:** {mh_data.get('mouth', {}).get('lip_shape', 'N/A')}
- **Mouth Width:** {mh_data.get('mouth', {}).get('mouth_width', 'N/A')}

---

## Hair
- **Style:** {mh_data.get('hair', {}).get('hair_style', 'N/A')}
- **Color:** {mh_data.get('hair', {}).get('hair_color', 'N/A')}
- **Type:** {mh_data.get('hair', {}).get('hair_type', 'N/A')}
- **Facial Hair:** {mh_data.get('hair', {}).get('facial_hair', 'N/A')}
- **Facial Hair Style:** {mh_data.get('hair', {}).get('facial_hair_style', 'N/A')}

---

## Body
- **Body Type:** {mh_data.get('body', {}).get('body_type', 'N/A')}
- **Height:** {mh_data.get('body', {}).get('height', 'N/A')}
- **Proportions:** {mh_data.get('body', {}).get('proportions', 'N/A')}

---

## Clothing
- **Style:** {mh_data.get('clothing', {}).get('style', 'N/A')}
- **Description:** {mh_data.get('clothing', {}).get('description', 'N/A')}

---

## Character Traits
"""

        if 'personality_traits' in mh_data:
            for trait in mh_data['personality_traits']:
                doc_content += f"- {trait}\n"

        doc_content += f"""
---

## Animation & Voice
- **Animation Style:** {mh_data.get('animation_style', 'N/A')}
- **Voice Type:** {mh_data.get('voice_type', 'N/A')}

---

## MetaHuman Creator Instructions

1. Open MetaHuman Creator (https://metahuman.unrealengine.com/)
2. Create new MetaHuman
3. Use the specifications above to customize:
   - Face shape and features
   - Eyes, nose, mouth
   - Hair and facial hair
   - Body type
   - Clothing
4. Export to your Unreal Engine project
5. Replace the placeholder in BP_{char_name}

---

## Full JSON Specification

```json
{json.dumps(mh_data, indent=2)}
```
"""

        # Save to project
        project_dir = unreal.SystemLibrary.get_project_directory()
        docs_dir = os.path.join(project_dir, "Documentation", "AI_Generated_MetaHumans")
        os.makedirs(docs_dir, exist_ok=True)

        doc_file = os.path.join(docs_dir, f"{char_name}_Specification.md")

        try:
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(doc_content)

            unreal.log(f"📄 Created specification document: {doc_file}")
        except Exception as e:
            unreal.log_error(f"Failed to create specification document: {e}")


# Convenience functions
def quick_generate_metahuman(description):
    """Quick MetaHuman generation"""
    generator = MetaHumanGenerator()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mh = loop.run_until_complete(generator.generate_metahuman(description))
    loop.close()

    return mh


def quick_generate_biblical_character(name):
    """Quick biblical character generation"""
    generator = MetaHumanGenerator()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mh = loop.run_until_complete(generator.generate_biblical_character(name))
    loop.close()

    return mh


def generate_all_disciples():
    """Generate all 12 disciples + Jesus + Mary Magdalene"""
    characters = [
        "Jesus Christ",
        "Peter (Simon Peter)",
        "Andrew",
        "James (son of Zebedee)",
        "John",
        "Philip",
        "Bartholomew (Nathanael)",
        "Matthew (Levi)",
        "Thomas",
        "James (son of Alphaeus)",
        "Thaddaeus (Judas son of James)",
        "Simon the Zealot",
        "Judas Iscariot",
        "Mary Magdalene"
    ]

    generator = MetaHumanGenerator()

    async def generate_all():
        await generator.connect_ai()
        results = []
        for char in characters:
            unreal.log(f"Generating: {char}")
            mh = await generator.generate_biblical_character(char)
            results.append(mh)
            await asyncio.sleep(5)  # Rate limiting
        return results

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    all_chars = loop.run_until_complete(generate_all())
    loop.close()

    return all_chars


# Examples:
# quick_generate_metahuman("a wise elderly scholar with gray hair and gentle eyes")
# quick_generate_biblical_character("Peter")
# generate_all_disciples()  # Generate all characters for WWYD game!
