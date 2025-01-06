import os

from autogen import config_list_from_json

llm_config = config_list = config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

llm_config = {
    "timeout": 600,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0.02,
}