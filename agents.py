import os
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.user_proxy_agent import UserProxyAgent
# from instruct_agent import InstructAgent
from memory_agent import MemoryAgent

# from instruct_last_agent import InstructionAgent
from utils import generate_prompt
from LLM_config import llm_config, llm_CDA_config
import os
from pydantic import BaseModel
from autogen_ext.models.openai import OpenAIChatCompletionClient

print(os.getcwd())

class Component(BaseModel):
        pros: str
        cons: str
        design: str
        details: str

class ComponentsMemory (BaseModel):
        aim: str
        Platform: str
        Components: list[Component] | None = None



DEA = MemoryAgent(
    name="DataEngineerAgent",
    description=generate_prompt("prompts/agents/data-engineer.prompt"),
    # system_message = '''You are a Data Engineer.
    # Your role is to build and manage the data pipelines.
    # You will be tasked with ingesting data from various sources, transforming and cleaning it,
    # and ensuring it is ready for further processing.
    # Your expertise in data manipulation and pipeline orchestration is vital to the project's success, as you create efficient data flows.
    # Instructions:**
    #     - Remember, this is a collaborative design discussion, not a project execution. Refrain from assigning or implementing tasks with deadlines.
    #     - Keep the conversation focused on data engineering choices, technologies, and potential challenges.
    #     - Output your deliverables in full when assigned a task.''',
    system_message=generate_prompt("prompts/agents/data-engineer.prompt"),
    memory_json={
        "aim": "",
        "Platform": "",
        "Component_1": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_2": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_3": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_4": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_5": {"Pros": "", "Cons": "", "Design": "", "details": ""},
    },
    structured_output = ComponentsMemory, 
    # memory_update_prompt= "Read the newest response to the chat, and populate the json with factual imformation. JSON: {memory}",
    # memory_reply_prompt= "With the above instruction and chathistory, together with the following json that may or may not have recorded your proposal and comments, Do what the conversation delegation agent has asked you to. Json summary: {memory}",
    # llm_config=llm_config.update(response_format = ComponentsMemory),
    llm_config=llm_config,
    # model_client = DEA_client, 
    code_execution_config=False,
    # code_execution_config={"use_docker":"amazon/aws-cli"},  # Turn off code execution, by default it is off.
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    default_auto_reply="Data engineer Agent has finished its conversation. ",
    function_map=None,  # No registered functions, by default it is None.
)

IA = MemoryAgent(
    name="InfrustructureAgent",
    description=generate_prompt("prompts/agents/infrastructure.prompt"),
    # system_message = '''You are the Data Architect, responsible for the blueprint and overall design of the data pipeline architecture.
    # Your task is to create a scalable and efficient system to handle large volumes of data.
    # This includes deciding on the architecture, data flow, and technologies to be used, ensuring it meets the platform's analytics requirements.
    # Your role is critical in setting the foundation for the entire data processing system.
    # Instructions:**
    #     - Remember, this is a collaborative design discussion, not a project execution. Refrain from assigning or implementing tasks with deadlines.
    #     - Keep the conversation focused on architectural choices, technologies, and potential challenges.
    #     - Output your deliverables in full when assigned a task.''',
    system_message=generate_prompt("prompts/agents/infrastructure.prompt"),
    memory_json={
        "aim": "",
        "Platform": "",
        "Component_1": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_2": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_3": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_4": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_5": {"Pros": "", "Cons": "", "Design": "", "details": ""},
    },
    structured_output = ComponentsMemory, 
    # memory_update_prompt= "Read the newest response to the chat, and populate the json with factual imformation. JSON: {memory}",
    # memory_reply_prompt= "With the above instruction and chathistory, together with the following json that may or may not have recorded your proposal and comments, Do what the conversation delegation agent has asked you to. Json summary: {memory}",
    # llm_config=llm_config.update(response_format = ComponentsMemory),
    llm_config=llm_config,
    # model_client = IA_client, 
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    default_auto_reply="Infrustructure Agent has finished its conversation. ",
    function_map=None,  # No registered functions, by default it is None.
)


MLA = MemoryAgent(
    name="MachineLearningEngineerAgent",
    description=generate_prompt("prompts/agents/machine-learning.prompt"),
    # system_message = '''You are a Machine Learning Engineer.
    # Your expertise in AI and machine learning is vital to enhancing the data pipeline.
    # You will research, design, and deploy ML models for recommendation engines, predictive analytics, and intelligent data processing.
    # Your role involves model training, optimization, and integration, adding a layer of intelligence to the system.
    # Instructions:**
    #     - Remember, this is a collaborative design discussion, not a project execution. Refrain from assigning or implementing tasks with deadlines.
    #     - Keep the conversation focused on design choices, technologies, and potential challenges.
    #     - Output your deliverables in full when assigned a task.''',
    system_message=generate_prompt("prompts/agents/machine-learning.prompt"),
    memory_json={
        "aim": "",
        "Platform": "",
        "Component_1": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_2": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_3": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_4": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_5": {"Pros": "", "Cons": "", "Design": "", "details": ""},
    },
    structured_output = ComponentsMemory, 
    # memory_update_prompt= "Read the newest response to the chat, and populate the json with factual imformation. JSON: {memory}",
    # memory_reply_prompt= "With the above instruction and chathistory, together with the following json that may or may not have recorded your proposal and comments, Do what the conversation delegation agent has asked you to. Json summary: {memory}",
    # llm_config=llm_config.update(response_format = ComponentsMemory),
    llm_config=llm_config,
    # model_client = MLA_client, 
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    default_auto_reply="Machine learning Agent has finished its conversation. ",
    function_map=None,  # No registered functions, by default it is None.
)

BOA = MemoryAgent(
    name="BusinessObjectiveAgent",
    description=generate_prompt("prompts/agents/business-objective.prompt"),
    # system_message = '''You are a Business Objective Engineer.
    # Your expertise in business Requirements and Success Metrics is vital to understand the requirements of the proposed data pipelines.
    # You will provide business insights, business needs, resources needs for the data pipeline.
    # Your role is critical in ensuring the business using the proposed data pipeline is most efficient in cost effectiveness.
    # Instructions:**
    #     - Remember, this is a collaborative design discussion, not a project execution. Refrain from assigning or implementing tasks with deadlines.
    #     - Keep the conversation focused on design choices, technologies, and potential challenges, and business objectives.
    #     - Output your deliverables in full when assigned a task.''',
    system_message=generate_prompt("prompts/agents/business-objective.prompt"),
    memory_json=dict({
        "aim": "",
        "Platform": "",
        "Component_1": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_2": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_3": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_4": {"Pros": "", "Cons": "", "Design": "", "details": ""},
        "Component_5": {"Pros": "", "Cons": "", "Design": "", "details": ""},
    }),
    structured_output = ComponentsMemory, 
    # memory_update_prompt= "Read the newest response to the chat, and populate the json with factual imformation. JSON: {memory}",
    # memory_reply_prompt= "With the above instruction and chathistory, together with the following json that may or may not have recorded your proposal and comments, Do what the conversation delegation agent has asked you to. Json summary: {memory}",
    # llm_config=llm_config.update(response_format = ComponentsMemory),
    llm_config=llm_config,
    # model_client = BOA_client, 
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    default_auto_reply="Business Objective Agent has finished its conversation. ",
    function_map=None,  # No registered functions, by default it is None.
)


class CDMemory(BaseModel):
    num_proposals:int|None =0
    num_discussions: int|None =0
    num_consensus: int|None =0
    final_output_obtained: bool|None=False



CDA = MemoryAgent(
    name="ConversationDelegationAgent",
    description=generate_prompt("prompts/agents/conversation-delegation.prompt"),
    # system_message = """You are the Conversation Delegation Agent, responsible for coordinating the efforts of the data pipeline engineering team in creating conceptual designs and architecture for a different company to implement.
    # Your role is to break down the complex discusion of designing an efficient data pipeline into propose, discuss, and consolidate steps.
    # You may facilitate discussion between team members where their expertise aligns.
    # You will need to consider the strengths and responsibilities of each agent in your team:
    # - Machine learning Engineer
    # - Data Engineer
    # - Infrustructure Engineer
    # - Business Objective Engineer
    # - Knowledge Intergration
    # - Evaluate and Refinement
    # Your system messages should provide clear instructions for next speaker, ensuring a well-organized and productive workflow.
    # Once all tasks are completed, you will summarize the overall design of the data pipeline, provide a high-level overview of the data pipeline's functionality, produce any required file, and end with "TERMINATE". """,
    system_message=generate_prompt("prompts/agents/conversation-delegation.prompt"),
    memory_json={
        "Number of proposals": 0,
        "number of discussions": 0,
        "number of consensus": 0,
        "final output json obtained": "false",
    },
    structured_output = CDMemory, 
    # llm_config=llm_config.update(response_format = ComponentsMemory),
    llm_config=llm_CDA_config,
    # model_client = CDA_client, 
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    default_auto_reply="Conversation Delegation Agent has finished its conversation. ",
    function_map=None,  # No registered functions, by default it is None.
)


KIA = AssistantAgent(
    "KownledgeIntergrationAgent",
    description=generate_prompt("prompts/agents/knowledge-integration.prompt"),
    # system_message = '''You are a Kownledge Intergration Engineer.
    # Your are great at summarising important meeting points. You are also working to maintain a shared document that is up-to-date with the design consensus.
    # Your role is critical in ensuring everyone in the discussion has mutual understanding of each other.
    # Instructions:**
    #     - Remember, this is a collaborative design discussion, not a project execution. Refrain from assigning or implementing tasks with deadlines.
    #     - Summarise the conversations based on the full history, and update shared and agreed upon design/coding files.
    #     - Keep the conversation focused on design choices, technologies, and potential challenges, and business objectives.
    #     - Output your summarise and document in full.''',
    system_message=generate_prompt("prompts/agents/knowledge-integration.prompt"),
    llm_config=llm_config,
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    default_auto_reply="Conversation Delegation Agent has finished its conversation. ",
    function_map=None,  # No registered functions, by default it is None.
)

ERA = AssistantAgent(
    "EveluateRefinementAgent",
    description=generate_prompt("prompts/agents/evaluate-and-refine.prompt"),
    # system_message = """You are a Evaluation and Refinement Analyst, your role is to ensure the integrity and reliability of the data pipeline. You will develop data validation rules, monitor data quality, and implement cleansing processes. Your task is to identify and rectify inconsistencies, ensuring the data is accurate and trustworthy for downstream analytics and decision-making processes.
    # Instructions:**
    #     - Remember, this is a collaborative design discussion, not a project execution. Refrain from assigning or implementing tasks with deadlines.
    #     - Evaluate the design and coding proposed in the score out of 10 in the four criterea: Quality score, Efficiency score, Compliance score, Maintainability score.
    #     - Keep the conversation focused on design choices, technologies, and potential challenges.
    #     - Output your evaluations in. """,
    system_message=generate_prompt("prompts/agents/evaluate-and-refine.prompt"),
    llm_config=llm_config,
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    default_auto_reply="Conversation Delegation Agent has finished its conversation. ",
    function_map=None,  # No registered functions, by default it is None.
)

DJE = AssistantAgent(
    name="DocumentationEngineer",
    description=generate_prompt("prompts/agents/evaluate-and-refine.prompt"),
    system_message=generate_prompt("prompts/agents/evaluate-and-refine.prompt"),
    llm_config=llm_config,
    code_execution_config=False,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    # llm_config=llm_config,
    code_execution_config=False,
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, and the reason why the task is not solved yet.""",
)
