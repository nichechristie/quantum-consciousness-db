"""
AI Game Dev Plugin - Editor Panel
Main UI for AI integration in Unreal Engine
"""

import unreal
import asyncio
import sys
import os

# Add plugin directory to path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

from ai_connectors import AIConnectorFactory


class AIEditorPanel:
    """Main AI editor panel for Unreal Engine"""

    def __init__(self):
        self.ai_connector = None
        self.current_ai = "ChatGPT"
        self.conversation_history = []

    async def initialize_ai(self, ai_name="ChatGPT"):
        """Initialize AI connection"""
        self.current_ai = ai_name
        self.ai_connector = AIConnectorFactory.create(ai_name)

        if await self.ai_connector.connect():
            unreal.log(f"✅ Connected to {ai_name}")
            return True
        else:
            unreal.log_error(f"❌ Failed to connect to {ai_name}")
            return False

    async def send_message(self, message):
        """Send message to AI and get response"""
        if not self.ai_connector:
            await self.initialize_ai()

        unreal.log(f"📤 Sending: {message}")
        response = await self.ai_connector.send_message(message)

        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    async def generate_prop(self, prompt, auto_place=True):
        """Generate a prop from text prompt"""
        unreal.log(f"🎨 Generating prop: {prompt}")

        message = f"""Create a detailed 3D prop specification for Unreal Engine 5:

Prop Description: {prompt}

Provide in this JSON format:
{{
    "name": "PropName",
    "description": "Detailed description",
    "mesh_type": "static_mesh or skeletal_mesh",
    "materials": ["Material1", "Material2"],
    "scale": {{"x": 1.0, "y": 1.0, "z": 1.0}},
    "collision": "simple or complex",
    "physics": true/false,
    "lod_levels": 3,
    "tags": ["tag1", "tag2"]
}}"""

        response = await self.send_message(message)

        # Parse response and create prop
        prop_data = self._parse_json_response(response)

        if prop_data and auto_place:
            self._create_and_place_prop(prop_data)

        return response

    async def generate_blueprint(self, prompt):
        """Generate Blueprint code from prompt"""
        unreal.log(f"📘 Generating Blueprint: {prompt}")

        message = f"""Generate complete Blueprint logic for Unreal Engine 5:

Description: {prompt}

Provide:
1. Blueprint class name and parent class
2. All variables (type, default value, category)
3. All functions with logic
4. Event Graph setup
5. Construction Script if needed

Format as detailed Blueprint instructions that can be manually created or scripted."""

        response = await self.send_message(message)
        return response

    async def generate_metahuman(self, prompt):
        """Generate MetaHuman from text description"""
        unreal.log(f"👤 Generating MetaHuman: {prompt}")

        message = f"""Create a detailed MetaHuman character specification:

Description: {prompt}

Provide detailed settings for:
1. Face shape and features
2. Skin tone and texture
3. Hair style and color
4. Eye color and shape
5. Body type and proportions
6. Clothing style
7. Age and gender
8. Personality traits (for animation reference)

Format as MetaHuman Creator parameters."""

        response = await self.send_message(message)

        # Create MetaHuman blueprint
        self._create_metahuman_blueprint(response)

        return response

    def _parse_json_response(self, response):
        """Extract JSON from AI response"""
        import json
        import re

        # Try to find JSON in response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                unreal.log_warning("Failed to parse JSON from response")
        return None

    def _create_and_place_prop(self, prop_data):
        """Create and place prop in level"""
        unreal.log(f"📦 Creating prop: {prop_data.get('name', 'NewProp')}")

        # Get editor subsystems
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        editor_level_lib = unreal.EditorLevelLibrary()

        # Create a basic static mesh actor
        location = unreal.Vector(0, 0, 100)  # Spawn above ground
        rotation = unreal.Rotator(0, 0, 0)

        # Spawn empty actor
        actor = editor_actor_subsystem.spawn_actor_from_class(
            unreal.StaticMeshActor,
            location,
            rotation
        )

        if actor:
            actor.set_actor_label(prop_data.get('name', 'AI_Generated_Prop'))

            # Apply scale if provided
            if 'scale' in prop_data:
                scale_data = prop_data['scale']
                scale = unreal.Vector(
                    scale_data.get('x', 1.0),
                    scale_data.get('y', 1.0),
                    scale_data.get('z', 1.0)
                )
                actor.set_actor_scale3d(scale)

            unreal.log(f"✅ Created and placed: {actor.get_actor_label()}")
            return actor

        return None

    def _create_metahuman_blueprint(self, metahuman_spec):
        """Create MetaHuman Blueprint from specification"""
        unreal.log("👤 Creating MetaHuman Blueprint...")

        # Get asset tools
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

        # Create blueprint in /Game/MetaHumans/AI_Generated/
        blueprint_path = "/Game/MetaHumans/AI_Generated/"
        blueprint_name = "BP_AIMetaHuman"

        # Ensure directory exists
        unreal.EditorAssetLibrary.make_directory(blueprint_path)

        # Create Blueprint based on Character class
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", unreal.Character)

        asset = asset_tools.create_asset(
            blueprint_name,
            blueprint_path,
            unreal.Blueprint,
            factory
        )

        if asset:
            unreal.log(f"✅ Created MetaHuman Blueprint: {blueprint_path}{blueprint_name}")

            # Save the specification as metadata
            unreal.EditorAssetLibrary.set_metadata_tag(
                asset,
                "AI_Specification",
                metahuman_spec
            )

            return asset

        return None


# Global panel instance
_ai_panel = None


def launch_ai_panel():
    """Launch the AI editor panel"""
    global _ai_panel

    unreal.log("🚀 Launching AI Game Dev Panel...")

    if _ai_panel is None:
        _ai_panel = AIEditorPanel()

    # Create editor utility widget
    widget_path = "/AIGameDevPlugin/AI_Panel_Widget"

    # Try to load existing widget
    widget_asset = unreal.EditorAssetLibrary.load_asset(widget_path)

    if not widget_asset:
        unreal.log("Creating new editor widget...")
        # Widget will be created manually in editor or via additional script
        unreal.log(f"Please create an Editor Utility Widget at: {widget_path}")
        unreal.log("Then bind its functions to this Python module")

    unreal.log("✅ AI Panel initialized!")
    return _ai_panel


def get_panel():
    """Get the current AI panel instance"""
    global _ai_panel
    if _ai_panel is None:
        return launch_ai_panel()
    return _ai_panel


# Expose functions for Blueprint/Widget use
@unreal.ufunction(static=True, ret=str, params=[str])
def ai_send_message(message):
    """Send message to AI (synchronous wrapper)"""
    panel = get_panel()

    # Run async in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(panel.send_message(message))
    loop.close()

    return response


@unreal.ufunction(static=True, ret=str, params=[str])
def ai_generate_prop(prompt):
    """Generate prop from prompt (synchronous wrapper)"""
    panel = get_panel()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(panel.generate_prop(prompt, auto_place=True))
    loop.close()

    return response


@unreal.ufunction(static=True, ret=str, params=[str])
def ai_generate_blueprint(prompt):
    """Generate Blueprint from prompt (synchronous wrapper)"""
    panel = get_panel()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(panel.generate_blueprint(prompt))
    loop.close()

    return response


@unreal.ufunction(static=True, ret=str, params=[str])
def ai_generate_metahuman(prompt):
    """Generate MetaHuman from prompt (synchronous wrapper)"""
    panel = get_panel()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(panel.generate_metahuman(prompt))
    loop.close()

    return response


if __name__ == "__main__":
    launch_ai_panel()
