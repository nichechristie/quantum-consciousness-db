"""
Prop Generation System
Generates game props from AI descriptions and places them in the level
"""

import unreal
import asyncio
from ai_connectors import AIConnectorFactory


class PropGenerator:
    """Generate and place props in Unreal Engine levels"""

    def __init__(self):
        self.ai_connector = None

    async def connect_ai(self, ai_name="ChatGPT"):
        """Connect to AI service"""
        self.ai_connector = AIConnectorFactory.create(ai_name)
        return await self.ai_connector.connect()

    async def generate_props_batch(self, theme, count, auto_place=True):
        """Generate multiple props at once"""
        unreal.log(f"🎨 Generating {count} props with theme: {theme}")

        prompt = f"""Generate {count} detailed prop specifications for Unreal Engine 5.

Theme: {theme}

For EACH prop, provide this exact JSON format:
[
  {{
    "name": "PropName1",
    "description": "Detailed visual description",
    "mesh_type": "static_mesh",
    "dimensions": {{"length": 1.0, "width": 1.0, "height": 1.0}},
    "materials": ["Material_Primary", "Material_Secondary"],
    "scale": {{"x": 1.0, "y": 1.0, "z": 1.0}},
    "collision": "simple",
    "physics": false,
    "tags": ["biblical", "environment"]
  }},
  ... {count} total props
]

Make each prop unique and fitting for the theme."""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)

        # Parse and create props
        props_data = self._parse_props_json(response)

        created_props = []
        if props_data and auto_place:
            for i, prop_data in enumerate(props_data):
                actor = self._create_prop_in_level(prop_data, index=i)
                if actor:
                    created_props.append(actor)

        unreal.log(f"✅ Created {len(created_props)} props!")
        return created_props

    async def generate_single_prop(self, description, auto_place=True):
        """Generate a single prop from description"""
        unreal.log(f"🎨 Generating prop: {description}")

        prompt = f"""Create a detailed 3D prop specification for Unreal Engine 5:

Description: {description}

Provide this JSON:
{{
    "name": "PropName",
    "description": "Detailed visual description",
    "mesh_type": "static_mesh",
    "dimensions": {{"length": 1.0, "width": 1.0, "height": 1.0}},
    "materials": ["MaterialName"],
    "scale": {{"x": 1.0, "y": 1.0, "z": 1.0}},
    "collision": "simple",
    "physics": false,
    "tags": ["tag1", "tag2"]
}}"""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)

        # Parse and create
        prop_data = self._parse_single_prop_json(response)

        if prop_data and auto_place:
            return self._create_prop_in_level(prop_data)

        return None

    def _parse_props_json(self, response):
        """Extract array of props from AI response"""
        import json
        import re

        # Try to find JSON array
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except Exception as e:
                unreal.log_error(f"Failed to parse props JSON: {e}")

        return []

    def _parse_single_prop_json(self, response):
        """Extract single prop JSON"""
        import json
        import re

        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except Exception as e:
                unreal.log_error(f"Failed to parse prop JSON: {e}")

        return None

    def _create_prop_in_level(self, prop_data, index=0):
        """Create prop actor in the level"""
        prop_name = prop_data.get('name', f'AI_Prop_{index}')
        unreal.log(f"📦 Creating: {prop_name}")

        # Get editor subsystems
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

        # Calculate spawn location (arrange in grid)
        grid_spacing = 300  # cm
        row_size = 5
        row = index // row_size
        col = index % row_size

        location = unreal.Vector(
            col * grid_spacing,
            row * grid_spacing,
            100  # Above ground
        )
        rotation = unreal.Rotator(0, 0, 0)

        # Spawn actor
        actor = editor_actor_subsystem.spawn_actor_from_class(
            unreal.StaticMeshActor,
            location,
            rotation
        )

        if actor:
            # Set name
            actor.set_actor_label(prop_name)

            # Apply scale
            if 'scale' in prop_data:
                scale_data = prop_data['scale']
                scale = unreal.Vector(
                    scale_data.get('x', 1.0),
                    scale_data.get('y', 1.0),
                    scale_data.get('z', 1.0)
                )
                actor.set_actor_scale3d(scale)

            # Add tags
            if 'tags' in prop_data:
                for tag in prop_data['tags']:
                    actor.tags.append(unreal.Name(tag))

            # Store metadata
            metadata = {
                'description': prop_data.get('description', ''),
                'ai_generated': True,
                'mesh_type': prop_data.get('mesh_type', 'static_mesh'),
                'materials': prop_data.get('materials', [])
            }

            # Add component tag with metadata
            actor.tags.append(unreal.Name("AI_Generated"))

            unreal.log(f"✅ Created: {prop_name} at {location}")
            return actor

        unreal.log_error(f"❌ Failed to create: {prop_name}")
        return None

    def organize_props_in_grid(self, props, spacing=300):
        """Organize existing props in a grid layout"""
        unreal.log(f"📐 Organizing {len(props)} props in grid...")

        row_size = 5
        for i, actor in enumerate(props):
            if actor and actor.is_valid():
                row = i // row_size
                col = i % row_size

                new_location = unreal.Vector(
                    col * spacing,
                    row * spacing,
                    100
                )

                actor.set_actor_location(new_location, False, True)

        unreal.log("✅ Props organized!")


# Convenience function for quick prop generation
def quick_generate_props(theme, count=10):
    """Quick function to generate props from theme"""
    generator = PropGenerator()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    props = loop.run_until_complete(generator.generate_props_batch(theme, count))
    loop.close()

    return props


# Example: Generate 20 biblical props
# quick_generate_props("ancient biblical Middle Eastern environment", 20)
