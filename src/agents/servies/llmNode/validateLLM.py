# Middleware to convert the request to the correct format for the LLM

from typing import Any, Optional
import re
from src.agents.configs.llm_config import LLMConfig, State, Role


# These are all gonna be options in a dropdown in the UI
# Keep models below 7B
OPENAI_REGEX = re.compile(
r"^(gpt-5(?:-(?:mini|nano))|gpt-4(?:-turbo|\.1(?:-(?:mini|nano))?|o(?:-mini)?))(?:-\d{4}-\d{2}-\d{2})?$")
OPENAI_REASONING_REGEX = re.compile(
r"^(o1(?:-(?:mini|preview))?|o3(?:-mini)?|o4(?:-mini)?)(?:-\d{4}-\d{2}-\d{2})?$")
ANTHROPIC_REGEX = re.compile(
r"(anthropic|anthropic)\.claude-(3-((sonnet|haiku|opus)|\d-(haiku|sonnet))|(sonnet|haiku|opus)-4(-\d)?)-\d{8}-v\d:\d$")
# Support qwen 2.5 and qwen 3
QWEN_REGEX = re.compile(
    r"Qwen2\.5-(7|0\.5|1\.5|3|1\.7|0\.9)B(-Instruct)?|Qwen3-(1\.7|0\.6|4)B")
DEEPSEEK_REGEX = re.compile(r"deepseek-(coder-((6\.7|1\.3)b-instruct|7b-instruct-v1\.5)|llm-7b-chat)")
LLAMA_REGEX = re.compile(r"(Llama-(2|3.2)-(7b-(chat-hf)|(3|1)B-Instruct))|(CodeLlama-7b-Instruct-hf)")
MISTRAL_REGEX = re.compile(r"mistralai/Mistral-7B-Instruct-v0.(2|3)")

def validate_model_request(provider: str, model: str, temperature: float, max_tokens: int | None, top_p: float, stream: bool, stop: str | list[str] | None) -> bool:
    '''
    Validate the request
    '''
    # Request Validation
    if provider == "openai":
        if not OPENAI_REGEX.fullmatch(model):
            raise ValueError(f"Invalid model: {model}, supported models: {OPENAI_REGEX.pattern}")
    elif provider == "anthropic":
        if not ANTHROPIC_REGEX.fullmatch(model):
            raise ValueError(f"Invalid model: {model}, supported models: {ANTHROPIC_REGEX.pattern}")
    elif provider == "qwen":
        if not QWEN_REGEX.fullmatch(model):
            raise ValueError(f"Invalid model: {model}, supported models: {QWEN_REGEX.pattern}")
    elif provider == "deepseek":
        if not DEEPSEEK_REGEX.fullmatch(model):
            raise ValueError(f"Invalid model: {model}, supported models: {DEEPSEEK_REGEX.pattern}")
    elif provider == "llama":
        if not LLAMA_REGEX.fullmatch(model):
            raise ValueError(f"Invalid model: {model}, supported models: {LLAMA_REGEX.pattern}")
    elif provider == "mistral":
        if not MISTRAL_REGEX.fullmatch(model):
            raise ValueError(f"Invalid model: {model}, supported models: {MISTRAL_REGEX.pattern}")
    else:
        raise ValueError(f"Invalid provider: {provider}, supported providers: openai, anthropic, qwen, deepseek, llama, mistral")
    
    if (provider == "openai" and (temperature < 0 or temperature > 2)) or (provider != "openai" and (temperature < 0 or temperature > 1)):
        raise ValueError("Temperature must be between 0 and 2 for openai, and between 0 and 1 for other providers")
    if max_tokens is not None and max_tokens <= 0:
        raise ValueError("Max tokens must be greater than 0")
    if top_p is not None and (top_p < 0 or top_p > 1):
        raise ValueError("Top p must be between 0 and 1")

    
    return True 
    
def get_default_params(LLMConfig: LLMConfig) -> tuple[str, str, float, int | None, float, bool, str | list[str] | None]:
    
    model = LLMConfig.model if LLMConfig.model is not None else "gpt-5"
    provider = LLMConfig.provider if LLMConfig.provider is not None else "openai"
    temperature = LLMConfig.temperature if LLMConfig.temperature is not None else 1
    max_tokens = LLMConfig.max_tokens if LLMConfig.max_tokens is not None else None
    top_p = LLMConfig.top_p if LLMConfig.top_p is not None else 1
    stream = LLMConfig.stream if LLMConfig.stream is not None else False
    stop = LLMConfig.stop if LLMConfig.stop is not None else None
    
    return model, provider, temperature, max_tokens, top_p, stream, stop 

def validate_message_request(state: State) -> bool:
    
    messages = state["messages"]
    
    if len(messages) == 0:
        raise ValueError("Cannot pass empty messages")
    
    user_messages = [msg for msg in messages if msg.role == Role.USER]
    assistant_messages = [msg for msg in messages if msg.role == Role.ASSISTANT]
    system_messages = [msg for msg in messages if msg.role == Role.SYSTEM]
    
    if len(user_messages) == 0:
        raise ValueError("Cannot pass empty user messages")
    if len(assistant_messages) == 0:
        raise ValueError("Cannot pass empty assistant messages")
    if len(system_messages) == 0:
        raise ValueError("Cannot pass empty system messages")
    
    if len(system_messages) > 1:
        raise ValueError("Cannot pass more than one system message")
    
    last_role = None
    for message in messages:
      if message.role == Role.SYSTEM:
        continue
      
      if not message.content:
        raise ValueError("Cannot pass empty message content")
      
      if last_role == message.role:
        raise ValueError("Message seqence must alternate between user and assistant")
      
      last_role = message.role
      
    if last_role != Role.USER:
        raise ValueError("Must pass user message as the last message")
    
    return True

