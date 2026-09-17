import os
from .null import NullProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider
def client():
    return {"openai":OpenAIProvider, "anthropic":AnthropicProvider}.get(os.getenv("LLM_PROVIDER", "null").lower(), NullProvider)()
