#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class FToolBarBuilder;
class FMenuBuilder;

class FAIGameDevPluginModule : public IModuleInterface
{
public:
	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

	/** This function will be bound to Command */
	void OpenAIChatPanel();

private:
	void RegisterMenus();

	TSharedPtr<class FUICommandList> PluginCommands;
};
