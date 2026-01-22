"""
Test Script for AI Game Dev Plugin
Run this in Unreal Python console to verify everything works
"""

import unreal
import sys
import os


def test_plugin_installation():
    """Test that the plugin is installed correctly"""
    print("\n" + "="*70)
    print("AI GAME DEV PLUGIN - INSTALLATION TEST")
    print("="*70 + "\n")

    tests_passed = 0
    tests_failed = 0

    # Test 1: Python imports
    print("Test 1: Checking Python imports...")
    try:
        import ai_editor_panel
        import ai_connectors
        import prop_generator
        import blueprint_generator
        import metahuman_generator
        import context_menu_integration

        print("✅ All Python modules imported successfully!")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Failed to import modules: {e}")
        tests_failed += 1

    # Test 2: Check dependencies
    print("\nTest 2: Checking Python dependencies...")
    try:
        import aiohttp
        import asyncio
        print("✅ aiohttp installed")

        try:
            import openai
            print("✅ openai installed")
        except:
            print("⚠️  openai not installed (ChatGPT won't work)")

        try:
            import google.generativeai
            print("✅ google-generativeai installed")
        except:
            print("⚠️  google-generativeai not installed (Gemini won't work)")

        try:
            import anthropic
            print("✅ anthropic installed")
        except:
            print("⚠️  anthropic not installed (Claude won't work)")

        tests_passed += 1
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        tests_failed += 1

    # Test 3: Check API keys
    print("\nTest 3: Checking API keys...")
    api_keys_found = []

    if os.getenv('OPENAI_API_KEY'):
        print("✅ OPENAI_API_KEY found")
        api_keys_found.append("OpenAI")
    else:
        print("⚠️  OPENAI_API_KEY not set")

    if os.getenv('GOOGLE_API_KEY'):
        print("✅ GOOGLE_API_KEY found")
        api_keys_found.append("Google")
    else:
        print("⚠️  GOOGLE_API_KEY not set")

    if os.getenv('ANTHROPIC_API_KEY'):
        print("✅ ANTHROPIC_API_KEY found")
        api_keys_found.append("Anthropic")
    else:
        print("⚠️  ANTHROPIC_API_KEY not set")

    if api_keys_found:
        print(f"✅ Found API keys for: {', '.join(api_keys_found)}")
        tests_passed += 1
    else:
        print("❌ No API keys found!")
        tests_failed += 1

    # Test 4: Test AI connection
    print("\nTest 4: Testing AI connection...")

    if api_keys_found:
        try:
            from ai_connectors import AIConnectorFactory
            import asyncio

            async def test_connection():
                # Use first available AI
                ai_name = "ChatGPT" if "OpenAI" in api_keys_found else api_keys_found[0]
                connector = AIConnectorFactory.create(ai_name)

                if await connector.connect():
                    print(f"✅ Successfully connected to {ai_name}!")
                    return True
                else:
                    print(f"❌ Failed to connect to {ai_name}")
                    return False

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            connected = loop.run_until_complete(test_connection())
            loop.close()

            if connected:
                tests_passed += 1
            else:
                tests_failed += 1

        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            tests_failed += 1
    else:
        print("⚠️  Skipping connection test (no API keys)")
        tests_failed += 1

    # Test 5: Test Unreal integration
    print("\nTest 5: Testing Unreal Engine integration...")
    try:
        # Test basic Unreal functions
        editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        asset_lib = unreal.EditorAssetLibrary

        print("✅ Unreal Editor subsystems accessible")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Unreal integration failed: {e}")
        tests_failed += 1

    # Results
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print("="*70 + "\n")

    if tests_failed == 0:
        print("🎉 ALL TESTS PASSED! Plugin is ready to use!")
        print("\nQuick start:")
        print("  import prop_generator")
        print("  prop_generator.quick_generate_props('biblical items', 5)")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip3 install aiohttp openai google-generativeai anthropic")
        print("2. Set API keys: export OPENAI_API_KEY='your-key'")
        print("3. Restart Unreal Engine")

    return tests_passed, tests_failed


def quick_test():
    """Quick test - just check if everything loads"""
    print("\n🔍 Quick Plugin Test...\n")

    try:
        import ai_editor_panel
        import prop_generator
        import blueprint_generator
        import metahuman_generator

        print("✅ Plugin loaded successfully!")
        print("\nYou can now use:")
        print("  - prop_generator.quick_generate_props()")
        print("  - blueprint_generator.quick_generate_blueprint()")
        print("  - metahuman_generator.quick_generate_metahuman()")
        print("  - ai_editor_panel.launch_ai_panel()")

        return True

    except Exception as e:
        print(f"❌ Plugin test failed: {e}")
        return False


def demo_prop_generation():
    """Demo: Generate a few props"""
    print("\n🎨 Demo: Generating 3 biblical props...\n")

    try:
        import prop_generator

        props = prop_generator.quick_generate_props(
            "ancient biblical pottery and vessels",
            3
        )

        print(f"\n✅ Generated {len(props) if props else 0} props!")
        print("Check your level for the new props!")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


def demo_metahuman():
    """Demo: Generate a biblical character"""
    print("\n👤 Demo: Generating biblical character...\n")

    try:
        import metahuman_generator

        mh = metahuman_generator.quick_generate_biblical_character("Peter")

        if mh:
            print("\n✅ Generated MetaHuman specification for Peter!")
            print("Check /Game/MetaHumans/AI_Generated/ for the Blueprint")
            print("Check Documentation folder for detailed specifications")
        else:
            print("❌ Failed to generate MetaHuman")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


# Run full test when imported
if __name__ == "__main__":
    test_plugin_installation()


# Make functions available for manual testing
# Usage in Unreal Python console:
#   import test_plugin
#   test_plugin.quick_test()
#   test_plugin.demo_prop_generation()
#   test_plugin.demo_metahuman()
