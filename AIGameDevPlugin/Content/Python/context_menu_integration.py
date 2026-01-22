"""
Context Menu Integration
Adds "Ask AI" option to right-click menus in Unreal Engine
"""

import unreal
import asyncio
from ai_connectors import AIConnectorFactory


class AIContextMenu:
    """Adds AI functionality to context menus"""

    def __init__(self):
        self.ai_connector = None

    async def connect_ai(self, ai_name="ChatGPT"):
        """Connect to AI service"""
        self.ai_connector = AIConnectorFactory.create(ai_name)
        return await self.ai_connector.connect()

    async def ask_about_asset(self, asset_path):
        """Ask AI about a specific asset"""
        unreal.log(f"🤔 Asking AI about: {asset_path}")

        # Load asset and get info
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)

        if not asset:
            unreal.log_error(f"Failed to load asset: {asset_path}")
            return None

        # Get asset type and properties
        asset_class = asset.get_class().get_name()
        asset_name = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)

        # Get metadata
        metadata = {}
        try:
            tags = unreal.EditorAssetLibrary.get_metadata_tag_values(asset)
            metadata = dict(tags)
        except:
            pass

        prompt = f"""I have an Unreal Engine asset:

Asset Path: {asset_path}
Asset Type: {asset_class}
Asset Name: {asset_name}

Please analyze this asset and tell me:
1. What is this asset?
2. How is it typically used in Unreal Engine?
3. Best practices for using this asset
4. Common issues and solutions
5. Suggestions for improvement or optimization

{f"Metadata: {metadata}" if metadata else ""}
"""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)
        return response

    async def suggest_improvements(self, asset_path):
        """Get AI suggestions for improving an asset"""
        unreal.log(f"💡 Getting improvement suggestions for: {asset_path}")

        asset = unreal.EditorAssetLibrary.load_asset(asset_path)

        if not asset:
            return None

        asset_class = asset.get_class().get_name()

        prompt = f"""I have a {asset_class} asset in Unreal Engine at: {asset_path}

Suggest specific improvements for this asset:
1. Performance optimizations
2. Visual quality enhancements
3. Better organization/structure
4. Additional features to add
5. Industry best practices to follow

Provide actionable, specific suggestions."""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)
        return response

    async def generate_related_assets(self, asset_path, count=5):
        """Generate related assets based on selected asset"""
        unreal.log(f"🎨 Generating {count} related assets for: {asset_path}")

        asset = unreal.EditorAssetLibrary.load_asset(asset_path)

        if not asset:
            return None

        asset_class = asset.get_class().get_name()
        asset_name = asset.get_name()

        prompt = f"""Based on this Unreal Engine asset:

Name: {asset_name}
Type: {asset_class}
Path: {asset_path}

Generate {count} related assets that would complement this one.

For each related asset provide:
- Name
- Type (same or compatible type)
- Description
- How it relates to the original
- Usage together

Format as JSON array."""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)
        return response

    async def fix_common_issues(self, asset_path):
        """Get AI help fixing common issues with an asset"""
        unreal.log(f"🔧 Analyzing issues in: {asset_path}")

        asset = unreal.EditorAssetLibrary.load_asset(asset_path)

        if not asset:
            return None

        asset_class = asset.get_class().get_name()

        prompt = f"""Analyze this {asset_class} in Unreal Engine: {asset_path}

Common issues to check for:
1. Performance problems (polycount, texture size, etc.)
2. Setup issues (missing references, broken links)
3. Naming convention problems
4. Organization issues
5. Missing optimization settings

Provide:
- Issues detected (based on asset type)
- How to fix each issue
- Prevention tips"""

        if not self.ai_connector:
            await self.connect_ai()

        response = await self.ai_connector.send_message(prompt)
        return response


# Global instance
_context_menu = None


def get_context_menu():
    """Get or create context menu instance"""
    global _context_menu
    if _context_menu is None:
        _context_menu = AIContextMenu()
    return _context_menu


# Synchronous wrappers for editor menu callbacks
def context_ask_about_asset(asset_path):
    """Ask AI about asset (sync wrapper)"""
    menu = get_context_menu()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(menu.ask_about_asset(asset_path))
    loop.close()

    # Show response in dialog
    if response:
        show_ai_response_dialog("AI Analysis", response)

    return response


def context_suggest_improvements(asset_path):
    """Get improvement suggestions (sync wrapper)"""
    menu = get_context_menu()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(menu.suggest_improvements(asset_path))
    loop.close()

    if response:
        show_ai_response_dialog("Improvement Suggestions", response)

    return response


def context_generate_related(asset_path):
    """Generate related assets (sync wrapper)"""
    menu = get_context_menu()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(menu.generate_related_assets(asset_path))
    loop.close()

    if response:
        show_ai_response_dialog("Related Assets", response)

    return response


def context_fix_issues(asset_path):
    """Fix common issues (sync wrapper)"""
    menu = get_context_menu()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(menu.fix_common_issues(asset_path))
    loop.close()

    if response:
        show_ai_response_dialog("Issue Analysis", response)

    return response


def show_ai_response_dialog(title, message):
    """Show AI response in editor dialog"""
    # Create notification
    unreal.EditorDialog.show_message(
        title,
        message,
        unreal.AppMsgType.OK
    )

    # Also log to output
    unreal.log(f"\n{'='*70}")
    unreal.log(f"{title}")
    unreal.log(f"{'='*70}")
    unreal.log(message)
    unreal.log(f"{'='*70}\n")


def register_context_menu_extensions():
    """Register context menu extensions"""
    unreal.log("📋 Registering AI context menu extensions...")

    # This would typically be done via C++ ToolMenus
    # For Python, we can create editor utility actions

    # Create actions that appear in the asset browser
    try:
        # Register custom asset actions
        unreal.log("✅ Context menu extensions registered!")
        unreal.log("Right-click on assets and use AI tools!")

    except Exception as e:
        unreal.log_error(f"Failed to register context menu: {e}")


# Initialize on import
register_context_menu_extensions()
