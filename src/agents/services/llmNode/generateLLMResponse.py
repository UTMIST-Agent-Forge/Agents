from src.agents.configs.llm_config import State, ToolCalls
from src.agents.services.llmNode.validateLLM import validate_model_request, get_default_params, validate_message_request
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import StructuredTool
from langchain_core.runnables import Runnable
from typing import AsyncGenerator
from src.agents.configs.llm_config import LLMConfig, StructuredOutput, Message
import json 
from langchain_core.messages import BaseMessage
from pydantic_core import PydanticCustomError
from openai import OpenAIError
from anthropic import AnthropicError
from dotenv import load_dotenv, find_dotenv
import os
from aiolimiter import AsyncLimiter

#handle each model 
#handle long term and short term memory 

load_dotenv(find_dotenv())
openai_api_key=os.getenv("OPENAI_API_KEY")
anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")

# Rate limiters for each provider
# OpenAI: 60 requests per minute (conservative for tier 1)
# Anthropic: 50 requests per minute (conservative for tier 1)
OPENAI_RPM = int(os.getenv("OPENAI_RPM", "60"))
ANTHROPIC_RPM = int(os.getenv("ANTHROPIC_RPM", "50"))

openai_rate_limiter = AsyncLimiter(max_rate=OPENAI_RPM, time_period=60)
anthropic_rate_limiter = AsyncLimiter(max_rate=ANTHROPIC_RPM, time_period=60)

def get_rate_limiter(provider: str) -> AsyncLimiter:
    '''
    Get the rate limiter for a specific provider
    '''
    if provider == "openai":
        return openai_rate_limiter
    elif provider == "anthropic":
        return anthropic_rate_limiter
    else:
        # For unknown providers, create a default limiter (100 RPM)
        return AsyncLimiter(max_rate=100, time_period=60)

def get_model(provider: str, model: str, temperature: float, max_tokens: int | None, top_p: float, stream: bool, stop: str | list[str] | None) -> BaseChatModel:
    '''
    Get the model
    '''

    if provider == "openai":
     return ChatOpenAI(model=model, 
                       temperature=temperature,
                       max_tokens=max_tokens, #type: ignore
                       top_p=top_p, 
                       streaming=stream, 
                       stop_sequences=stop,
                       api_key=openai_api_key)
    else:
        return ChatAnthropic(model=model, #type: ignore
                             temperature=temperature,
                             max_tokens_to_sample=max_tokens, #type: ignore
                             top_p=top_p, 
                             streaming=stream, 
                             stop=stop,
                             api_key=anthropic_api_key)
    
    #to do add vLLM support for local host models 

def bind_tools(provider: str, model: BaseChatModel, tool_calls: ToolCalls) -> Runnable:
    '''
    Bind tools to the model
    '''
    
    tools = []
    for tool in tool_calls.tool_calls:
        if tool.args_schema:
            tools.append(StructuredTool(
                name=tool.function_name,
                description=tool.function_description,
                args_schema=tool.args_schema, #type: ignore
                func=tool.function
            ))
        else:
            tools.append(StructuredTool(
                name=tool.function_name,
                description=tool.function_description,
                func=tool.function
            ))
            
    return model.bind_tools(tools)

async def generate_structured_output(model: BaseChatModel, provider: str, messages: list[BaseMessage], stream: bool, structured_output: StructuredOutput) -> AsyncGenerator[str]:
    '''
    Generate structured output, openai only 
    '''
    
    structured_output_dict = structured_output.schema.copy()
    structured_output_dict["title"] = structured_output.title
    structured_output_dict["description"] = structured_output.description
    chat_model = model.with_structured_output(structured_output_dict)
    
    if stream:
        raise ValueError("Streaming is not supported for structured output")
    
    if provider in ["openai", "anthropic"]:
        rate_limiter = get_rate_limiter(provider)
        async with rate_limiter:
            output = await chat_model.ainvoke(messages) #works for claude and openai
            yield json.dumps(output)
        
def to_langchain_messages(messages: list[Message]) -> list[BaseMessage]:
    '''
    Convert the messages to langchain messages
    '''
    return [BaseMessage(content=message.content, role=message.role.value) for message in messages]
    
async def generate_response(LLMConfig: LLMConfig, state: State, structured_output: StructuredOutput) -> AsyncGenerator[str]:
    
    try:
        model, provider, temperature, max_tokens, top_p, stream, stop = get_default_params(LLMConfig)
        validate_model_request(provider, model, temperature, max_tokens, top_p, stream, stop)
        validate_message_request(state)
        base_model = get_model(provider, model, temperature, max_tokens, top_p, stream, stop)
        messages = to_langchain_messages(state["messages"])
        rate_limiter = get_rate_limiter(provider)
        
        if LLMConfig.structured_output:
            async for resp in generate_structured_output(base_model, provider, messages, stream, LLMConfig.structured_output):
               yield resp
            return
        
        model = base_model
        if LLMConfig.tool_calls:
            model = bind_tools(provider, model, LLMConfig.tool_calls)

        if provider == "openai":
            if stream:
                async with rate_limiter:
                    async for resp in model.astream(messages):
                        if resp.tool_call_chunks: #type: ignore
                            if resp.tool_call_chunks[0]["name"]: #type:ignore
                                yield json.dumps({"name": resp.tool_call_chunks[0]["name"]}) #type: ignore
                            if resp.tool_call_chunks[0]["args"]: #type: ignore
                                yield json.dumps({"arguments": resp.tool_call_chunks[0]["args"]}) #type: ignore
                        if resp.content:
                            yield json.dumps({"content": resp.content})
                        else:
                            yield ""
                return
            else:
                async with rate_limiter:
                    resp = await model.ainvoke(messages)
                    if resp.additional_kwargs["tool_calls"]:
                        yield json.dumps({"name": resp.additional_kwargs["tool_calls"][0]["function"]["name"], "arguments": resp.additional_kwargs["tool_calls"][0]["function"]["arguments"]})
                    if resp.content:
                        yield json.dumps({"content": resp.content})
                    else:
                        yield ""
                return 
                
        if provider == "anthropic":
            if stream:
                async with rate_limiter:
                    async for resp in model.astream(messages):
                        if resp.tool_call_chunks: #type: ignore
                            if resp.tool_call_chunks[0]["name"]: #type: ignore
                                yield json.dumps({"name": resp.tool_call_chunks[0]["name"]}) #type: ignore
                            if resp.tool_call_chunks[0]["args"]: #type: ignore
                                yield json.dumps({"arguments": resp.tool_call_chunks[0]["args"]}) #type: ignore
                        if resp.content:
                            yield json.dumps({"content": resp.content})
                        else:
                            yield ""
                return
            else:
                async with rate_limiter:
                    resp = await model.ainvoke(messages)
                    if resp.tool_calls: #type: ignore
                        yield json.dumps({"name": resp.tool_calls[0]["name"], "arguments": resp.tool_calls[0]["args"]}) #type: ignore
                    if resp.content:
                        yield json.dumps({"content": resp.content})
                    else:
                        yield ""
                return
            
    # Certain errors spawn retries
    except OpenAIError as e:
        # Convert OpenAI API errors to Pydantic custom errors
        status_code = getattr(e, "status_code", None)
        error_msg = str(e)
        
        if status_code in (400, 422):
            raise PydanticCustomError(
                "openai_bad_request",
                "Bad request sent to OpenAI API: {error}",
                {"error": error_msg}
            )
        elif status_code == 401:
            raise PydanticCustomError(
                "openai_unauthorized",
                "Unauthorized to access OpenAI API: {error}",
                {"error": error_msg}
            )
        elif status_code == 403:
            raise PydanticCustomError(
                "openai_permission_denied",
                "Permission denied to access OpenAI API: {error}",
                {"error": error_msg}
            )
        elif status_code == 404:
            raise PydanticCustomError(
                "openai_not_found",
                "Requested OpenAI resource not found: {error}",
                {"error": error_msg}
            )
        elif status_code == 409:
            raise PydanticCustomError(
                "openai_conflict",
                "Conflict in OpenAI requests: {error}",
                {"error": error_msg}
            )
        elif status_code == 429:
            raise PydanticCustomError(
                "openai_rate_limit",
                "OpenAI rate limit exceeded: {error}",
                {"error": error_msg}
            )
        elif status_code in (502, 503, 504):
            raise PydanticCustomError(
                "openai_service_unavailable",
                "OpenAI service unavailable (status {status}): {error}",
                {"status": status_code, "error": error_msg}
            )
        else:
            raise PydanticCustomError(
                "openai_internal_error",
                "OpenAI internal server error: {error}",
                {"error": error_msg}
            )
            
    except AnthropicError as e:
        status_code = getattr(e, "status_code", None)
        error_msg = str(e)
        if status_code in (400, 422):
            raise PydanticCustomError(
                "anthropic_bad_request",
                "Bad request sent to anthropic API: {error}",
                {"error": error_msg}
            )
        elif status_code == 401:
            raise PydanticCustomError(
                "anthropic_unauthorized",
                "Unauthorized to access anthropic API: {error}",
                {"error": error_msg}
            )
        elif status_code == 403:
            raise PydanticCustomError(
                "anthropic_permission_denied",
                "Permission denied to access anthropic API: {error}",
                {"error": error_msg}
            )
        elif status_code == 404:
            raise PydanticCustomError(
                "anthropic_not_found",
                "Requested anthropic resource not found: {error}",
                {"error": error_msg}
            )
        elif status_code == 409:
            raise PydanticCustomError(
                "anthropic_conflict",
                "Conflict in anthropic requests: {error}",
                {"error": error_msg}
            )
        elif status_code == 429:
            raise PydanticCustomError(
                "anthropic_rate_limit",
                "anthropic rate limit exceeded: {error}",
                {"error": error_msg}
            )
        elif status_code in (502, 503, 504):
            raise PydanticCustomError(
                "anthropic_service_unavailable",
                "anthropic service unavailable (status {status}): {error}",
                {"status": status_code, "error": error_msg}
            )
        else:
            raise PydanticCustomError(
                "anthropic_internal_error",
                "anthropic internal server error: {error}",
                {"error": error_msg}
            )
            
    except Exception as e:
        # Convert any other exceptions to Pydantic custom error
        raise PydanticCustomError(
            "llm_response_error",
            "Error generating LLM response: {error}",
            {"error": str(e)}
        )
        