#include "AIGameDevPlugin.h"
#include "Styling/SlateStyleRegistry.h"
#include "Framework/Application/SlateApplication.h"
#include "LevelEditor.h"
#include "ToolMenus.h"
#include "EditorUtilityWidget.h"
#include "EditorUtilitySubsystem.h"
#include "EditorAssetLibrary.h"

#define LOCTEXT_NAMESPACE "FAIGameDevPluginModule"

void FAIGameDevPluginModule::StartupModule()
{
	// This code will execute after your module is loaded into memory
	UE_LOG(LogTemp, Log, TEXT("AIGameDevPlugin: Startup"));

	// Register menu extensions
	RegisterMenus();
}

void FAIGameDevPluginModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module
	UE_LOG(LogTemp, Log, TEXT("AIGameDevPlugin: Shutdown"));

	UToolMenus::UnRegisterStartupCallback(this);
	UToolMenus::UnregisterOwner(this);
}

void FAIGameDevPluginModule::OpenAIChatPanel()
{
	UE_LOG(LogTemp, Log, TEXT("Opening AI Chat Panel"));

	// Launch the Python script that creates the editor widget
	FString PythonScript = TEXT("import unreal; import sys; sys.path.append(r'") +
		FPaths::ProjectPluginsDir() + TEXT("AIGameDevPlugin/Content/Python'); import ai_editor_panel; ai_editor_panel.launch_ai_panel()");

	FPythonCommandEx PythonCommand;
	PythonCommand.Command = PythonScript;
	PythonCommand.ExecutionMode = EPythonCommandExecutionMode::ExecuteStatement;

	IPythonScriptPlugin::Get()->ExecPythonCommandEx(PythonCommand);
}

void FAIGameDevPluginModule::RegisterMenus()
{
	// Register menu items
	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FAIGameDevPluginModule::RegisterMenus));

	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(
				FName("AIGameDevTools"),
				LOCTEXT("AIGameDevToolsLabel", "AI Game Dev Tools"),
				LOCTEXT("AIGameDevToolsTooltip", "Open AI Game Development Tools"),
				FSlateIcon(),
				FUIAction(FExecuteAction::CreateRaw(this, &FAIGameDevPluginModule::OpenAIChatPanel))
			);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar.PlayToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("AITools");
			Section.AddEntry(FToolMenuEntry::InitToolBarButton(
				FName("OpenAIPanel"),
				FUIAction(FExecuteAction::CreateRaw(this, &FAIGameDevPluginModule::OpenAIChatPanel)),
				LOCTEXT("AIToolsLabel", "AI Tools"),
				LOCTEXT("AIToolsTooltip", "Open AI Game Development Tools"),
				FSlateIcon()
			));
		}
	}
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FAIGameDevPluginModule, AIGameDevPlugin)
