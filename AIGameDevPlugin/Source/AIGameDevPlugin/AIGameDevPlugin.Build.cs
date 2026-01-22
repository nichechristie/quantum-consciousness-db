using UnrealBuildTool;

public class AIGameDevPlugin : ModuleRules
{
	public AIGameDevPlugin(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicIncludePaths.AddRange(
			new string[] {
			}
		);

		PrivateIncludePaths.AddRange(
			new string[] {
			}
		);

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"UnrealEd",
				"EditorScriptingUtilities",
				"PythonScriptPlugin",
				"Blutility",
				"UMGEditor",
				"UMG",
				"Slate",
				"SlateCore",
				"InputCore",
				"LevelEditor",
				"EditorStyle",
				"ToolMenus",
				"ContentBrowser",
				"AssetTools"
			}
		);

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"Projects",
				"PropertyEditor",
				"EditorWidgets",
				"HTTP",
				"Json",
				"JsonUtilities"
			}
		);

		DynamicallyLoadedModuleNames.AddRange(
			new string[]
			{
			}
		);
	}
}
