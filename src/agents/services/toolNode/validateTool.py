from agents.configs.tool_config import ToolConfig

def get_default_params(ToolConfig: ToolConfig) -> tuple[str, str, float, int | None, float, bool, str | list[str] | None]:
    '''
    Get default parameters for tool
    '''

    tool_description = ToolConfig.tool_description if ToolConfig.tool_description is not None else "Unknown Description"
    tool_args = ToolConfig.tool_args if ToolConfig.tool_args is not None else None
    tool_func = ToolConfig.tool_func if ToolConfig.tool_func is not None else None
    
    return tool_description, tool_args, tool_func