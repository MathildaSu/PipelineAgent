import os
import autogen
from autogen import ConversableAgent
from utils import generate_prompt
from LLM_config import llm_config

DEA = ConversableAgent(
    "DEA",
    description = generate_prompt("prompts/agents/data-engineer.prompt"), 
    system_message = generate_prompt("prompts/system-message.prompt"),
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply = 3, 
    human_input_mode = "TERMINATE", 
    default_auto_reply = "Data engineer Agent has finished its conversation. ", 
    function_map=None,  # No registered functions, by default it is None.
)


IA = ConversableAgent(
    "IA",
    description = generate_prompt("prompts/agents/infrastructure.prompt"), 
    system_message = generate_prompt("prompts/system-message.prompt"), 
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply = 3, 
    human_input_mode = "TERMINATE", 
    default_auto_reply = "Infrustructure Agent has finished its conversation. ", 
    function_map=None,  # No registered functions, by default it is None.
)

MLA = ConversableAgent(
    "MLA",
    description = generate_prompt("prompts/agents/machine-learning.prompt"), 
    system_message = generate_prompt("prompts/system-message.prompt"), 
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply = 3, 
    human_inpu_mode = "TERMINATE", 
    default_auto_reply = "Machine learning Agent has finished its conversation. ", 
    function_map=None,  # No registered functions, by default it is None.
)


BOA = ConversableAgent(
    "BOA",
    description = generate_prompt("prompts/agents/business-objective.prompt"), 
    system_message = generate_prompt("prompts/system-message.prompt"), 
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply = 3, 
    human_input_mode = "TERMINATE", 
    default_auto_reply = "Business Objective Agent has finished its conversation. ", 
    function_map=None,  # No registered functions, by default it is None.
)

CDA = ConversableAgent(
    "CDA",
    description = generate_prompt("prompts/agents/conversation-delegation.prompt"), 
    system_message = """Based on your instruction, and the conversation history, choose the next speaker. Ask the next speaker to focus on the current step in the conversation, or progress into the next step. """, 
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply = 3, 
    human_input_mode = "TERMINATE", 
    default_auto_reply = "Conversation Delegation Agent has finished its conversation. ", 
    function_map=None,  # No registered functions, by default it is None.
)


KIA = ConversableAgent(
    "KIA",
    description = generate_prompt("prompts/agents/knowledge-integration.prompt"), 
    system_message = """Based on your instruction, and the conversation history, summarise the conversations up until now, and update shared and agreed upon design/coding files. """, 
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply = 3, 
    human_input_mode = "TERMINATE", 
    default_auto_reply = "Conversation Delegation Agent has finished its conversation. ", 
    function_map=None,  # No registered functions, by default it is None.
)

ERA = ConversableAgent(
    "ERA",
    description = generate_prompt("propmts/agents/evaluate-and-refine.prompt"), 
    system_message = """Based on your instruction, and the conversation history, evaluate the design and coding proposed in the score out of 10 in the four criterea: Quality score, Efficiency score, Compliance score, Maintainability score. """, 
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply = 3, 
    human_input_mode = "TERMINATE", 
    default_auto_reply = "Conversation Delegation Agent has finished its conversation. ", 
    function_map=None,  # No registered functions, by default it is None.
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "use_docker": "amazon/aws-cli",
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, and the reason why the task is not solved yet.""",
)
