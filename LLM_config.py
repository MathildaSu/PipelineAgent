import os

from autogen import config_list_from_json


config_list = [
    {
        "model": "deepseek-r1:7b",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    },
    # {
    #     "model": "claude",
    #     "base_url": "http://localhost:11434/v1",
    #     "api_key": "ollama",
    # },
#     {
#     "model": "qwen2.5-coder:7b",
#     "base_url": "http://localhost:11434/v1",
#     "api_key": "ollama",
#   }
]


llm_config = {
    "timeout": 600,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0.02,
}

llm_CDA_config = {
    "timeout": 600,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0.02,
    # "max_tokens": 80,  # Force brief responses
    # "stop": ["\n\n"],  # Prevent verbose output

}

