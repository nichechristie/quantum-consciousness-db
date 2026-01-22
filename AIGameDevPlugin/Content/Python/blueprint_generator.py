"""
Blueprint Generation System
Generates Blueprints from AI descriptions
"""

import unreal
import asyncio
from ai_connectors import AIConnectorFactory


class BlueprintGenerator:
    """Generate Blueprints from natural language descriptions"""

    def __init__(self):
        self.ai_connector = None

    async def connect_ai(self, ai_name="ChatGPT"):
        """Connect to AI service"""
        self.ai_connector = AIConnectorFactory.create(ai_name)
        return await self.ai_connector.connect()

    async def generate_blueprint(self, description, parent_class="Actor"):
        """Generate a Blueprint from description"""
        unreal.log(f"📘 Generating Blueprint: {description}")

        prompt = f"""Create a complete Blueprint specification for Unreal Engine 5:

Description: {description}
Parent Class: {parent_class}

Provide this JSON format:
{{
    "name": "BP_ComponentName",
    "parent_class": "{parent_class}",
    "description": "What this Blueprint does",
    "variables": [
        {{
            "name": "VariableName",
            "type": "float|int|bool|string|vector|object",
            "default_value": "default",
            "category": "Settings",
            "tooltip": "What this variable does"
        }}
    ],
    "functions": [
        {{
            "name": "FunctionName",
            "description": "What this function does",
            "inputs": [{{"name": "Input1", "type": "float"}}],
            "outputs": [{{"name": "Output1", "type": "bool"}}],
            "logic": "Step by step logic description"
        }}
    ],
    "event_graph": [
        {{
            "event": "BeginPlay|Tick|OnComponentHit",
            "logic": "What happens in this event"
        }}
    ],
    "components": [
        {{
            "name": "ComponentName",
            "type": "StaticMeshComponent|SkeletalMeshComponent|etc",
            "settings": {{"key": "value"}}
        }}
    ]
}}"""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)

        # Parse and create Blueprint
        bp_data = self._parse_blueprint_json(response)

        if bp_data:
            return self._create_blueprint_asset(bp_data)

        return None

    async def generate_blueprint_function(self, function_description):
        """Generate just a Blueprint function"""
        unreal.log(f"🔧 Generating function: {function_description}")

        prompt = f"""Create a Blueprint function for Unreal Engine 5:

Function: {function_description}

Provide this JSON:
{{
    "name": "FunctionName",
    "description": "Clear description",
    "inputs": [
        {{"name": "InputName", "type": "float", "description": "What this input does"}}
    ],
    "outputs": [
        {{"name": "OutputName", "type": "bool", "description": "What this returns"}}
    ],
    "local_variables": [
        {{"name": "TempVar", "type": "int", "default": 0}}
    ],
    "logic_steps": [
        "1. First do this...",
        "2. Then do this...",
        "3. Finally return..."
    ],
    "nodes": [
        {{
            "type": "Branch|ForLoop|Sequence|etc",
            "description": "What this node does"
        }}
    ]
}}"""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)
        return response

    async def generate_gameplay_system(self, system_description):
        """Generate a complete gameplay system"""
        unreal.log(f"⚙️ Generating system: {system_description}")

        prompt = f"""Create a complete gameplay system for Unreal Engine 5:

System: {system_description}

Provide multiple Blueprints that work together:
{{
    "system_name": "SystemName",
    "description": "How the system works",
    "blueprints": [
        {{
            "name": "BP_MainComponent",
            "purpose": "Core functionality",
            "parent_class": "ActorComponent",
            "variables": [...],
            "functions": [...],
            "events": [...]
        }},
        {{
            "name": "BP_HelperActor",
            "purpose": "Supporting functionality",
            "parent_class": "Actor",
            "variables": [...],
            "functions": [...],
            "events": [...]
        }}
    ],
    "integration": "How to integrate into existing project",
    "usage_example": "How to use this system"
}}"""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)

        # Could create multiple Blueprints here
        system_data = self._parse_system_json(response)

        if system_data and 'blueprints' in system_data:
            created_bps = []
            for bp_spec in system_data['blueprints']:
                bp = self._create_blueprint_asset(bp_spec)
                if bp:
                    created_bps.append(bp)

            unreal.log(f"✅ Created {len(created_bps)} Blueprints for system!")
            return created_bps

        return None

    def _parse_blueprint_json(self, response):
        """Extract Blueprint JSON from response"""
        import json
        import re

        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except Exception as e:
                unreal.log_error(f"Failed to parse Blueprint JSON: {e}")

        return None

    def _parse_system_json(self, response):
        """Extract system JSON from response"""
        import json
        import re

        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except Exception as e:
                unreal.log_error(f"Failed to parse system JSON: {e}")

        return None

    def _create_blueprint_asset(self, bp_data):
        """Create Blueprint asset in project"""
        bp_name = bp_data.get('name', 'BP_AIGenerated')
        parent_class_name = bp_data.get('parent_class', 'Actor')

        unreal.log(f"📘 Creating Blueprint: {bp_name}")

        # Get parent class
        parent_class = self._get_parent_class(parent_class_name)

        if not parent_class:
            unreal.log_error(f"Unknown parent class: {parent_class_name}")
            return None

        # Create Blueprint in /Game/Blueprints/AI_Generated/
        blueprint_path = "/Game/Blueprints/AI_Generated/"
        full_path = f"{blueprint_path}{bp_name}"

        # Ensure directory exists
        unreal.EditorAssetLibrary.make_directory(blueprint_path)

        # Check if already exists
        if unreal.EditorAssetLibrary.does_asset_exist(full_path):
            unreal.log_warning(f"Blueprint already exists: {full_path}")
            return unreal.EditorAssetLibrary.load_asset(full_path)

        # Create Blueprint
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", parent_class)

        asset = asset_tools.create_asset(
            bp_name,
            blueprint_path,
            unreal.Blueprint,
            factory
        )

        if asset:
            unreal.log(f"✅ Created Blueprint: {full_path}")

            # Store AI specification as metadata
            description = bp_data.get('description', 'AI Generated Blueprint')
            unreal.EditorAssetLibrary.set_metadata_tag(
                asset,
                "Description",
                description
            )

            # Store full spec
            import json
            spec_json = json.dumps(bp_data, indent=2)
            unreal.EditorAssetLibrary.set_metadata_tag(
                asset,
                "AI_Specification",
                spec_json
            )

            # Save asset
            unreal.EditorAssetLibrary.save_asset(full_path)

            return asset

        unreal.log_error(f"❌ Failed to create Blueprint")
        return None

    def _get_parent_class(self, class_name):
        """Get UClass from name"""
        class_map = {
            "Actor": unreal.Actor,
            "Pawn": unreal.Pawn,
            "Character": unreal.Character,
            "ActorComponent": unreal.ActorComponent,
            "SceneComponent": unreal.SceneComponent,
            "StaticMeshComponent": unreal.StaticMeshComponent,
            "GameMode": unreal.GameModeBase,
            "PlayerController": unreal.PlayerController,
            "Widget": unreal.UserWidget,
            "Object": unreal.Object
        }

        return class_map.get(class_name, unreal.Actor)


# Convenience functions
def quick_generate_blueprint(description, parent="Actor"):
    """Quick Blueprint generation"""
    generator = BlueprintGenerator()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bp = loop.run_until_complete(generator.generate_blueprint(description, parent))
    loop.close()

    return bp


def quick_generate_system(description):
    """Quick system generation"""
    generator = BlueprintGenerator()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    system = loop.run_until_complete(generator.generate_gameplay_system(description))
    loop.close()

    return system


# Examples:
# quick_generate_blueprint("health system with damage and healing", "ActorComponent")
# quick_generate_system("inventory system with pickup, drop, and storage")
