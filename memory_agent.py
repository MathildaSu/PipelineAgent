import asyncio
import contextvars
import json
import regex

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from pydantic import BaseModel


from autogen.agentchat.conversable_agent import ConversableAgent
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.agent import Agent
from autogen.oai.client import OpenAIWrapper
from autogen.io.base import IOStream
from autogen.formatting_utils import colored


class MemoryAgent(AssistantAgent):

    DEFAULT_MEMORY_UPDATE_PROMPT = """Use the entire history of the groupchat (presented before this message) to populate and update the current memory json with factual imformation. 

    *** OUTPUT SHOULD ONLY BE VALID JSON.  
    Be very careful to not include anything that renders the output not directly loadable with json.loads(). *** 
    
    For context, current memory: {memory}. 

    Newest response by yourself: {new_response}
    
    Updated memory in JSON format: """

    DEFAULT_MEMORY_REPLY_PROMPT = """Using the above instruction, group chat history, and memory json with important information from the chat history, to solve the conversation delegation agent's task. 

    Respond according to the ***last instruction from Conversation delegation agent***. 

    For cuntext, current memory from chat based on your own outputs: {memory}. 
    
    Newest instruction: {instruction}. 
    
    Output: """

    def __init__(
        self,
        memory_json: Optional[Dict] = None,
        memory_update_prompt: Optional[str] = None,
        memory_reply_prompt: Optional[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.memory_json = memory_json if memory_json != None else {}
        self.memory_update_prompt = (
            memory_update_prompt
            if memory_update_prompt != None
            else self.DEFAULT_MEMORY_UPDATE_PROMPT
        )
        self.memory_reply_prompt = (
            memory_reply_prompt
            if memory_reply_prompt != None
            else self.DEFAULT_MEMORY_REPLY_PROMPT
        )
        self.replace_reply_func(
            ConversableAgent.generate_oai_reply, MemoryAgent.generate_oai_reply
        )
        self.memory_format = self.memory_to_structured_output()

    def memory_to_structured_output(self) -> BaseModel:
        from pydantic import create_model
        def dict_model(name:str,dict_def:dict):
            fields = {}
            for field_name,value in dict_def.items():
                if isinstance(value,tuple):
                    fields[field_name]=value
                elif isinstance(value,dict):
                    fields[field_name]=(dict_model(f'{name}_{field_name}',value),...)
                else:
                    raise ValueError(f"Field {field_name}:{value} has invalid syntax")
            return create_model(name,**fields)

        model = dict_model("memory",self.memory)
        return model


    @property
    def memory(self) -> dict:
        """Return the system message."""
        return self.memory_json

    @property
    def memory_prompt(self) -> str:
        """Return the system message."""
        return self.memory_prompt


    def generate_oai_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[OpenAIWrapper] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """Generate a reply using autogen.oai."""
        client = self.client if config is None else config
        if client is None:
            return False, None
        if messages is None:
            messages = self._oai_messages[sender]
        memory_instruction = self.memory_reply_prompt.format(
            memory=self.memory_json, instruction=messages[-1]['content']
        )
        memory_instruction = [{"content": memory_instruction, "role": "user"}]

        extracted_response = self._generate_oai_reply_from_client(
            client,
            self._oai_system_message + messages[:-1] + memory_instruction,
            self.client_cache,
            
        )

        instruction = [
            {
                "content": self.memory_update_prompt.format(
                    memory=self.memory_json, new_response=extracted_response
                ),
                "name": self.name,
                "role": "user",
            }
        ]
        memory_response = self._generate_oai_reply_from_client(
            self.client, messages + instruction, self.client_cache
        )
        
        iostream = IOStream.get_default()
        iostream.print(colored("***** raw Memory *****", "green"), flush=True)
        iostream.print(memory_response, flush=True)

        pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
        a = pattern.findall(memory_response.strip())
        self.memory_json = json.loads(a[0])
        # print the message received
        iostream.print(colored("***** loaded Memory *****", "green"), flush=True)
        iostream.print(self.memory_json, flush=True)

        return (
            (False, None) if extracted_response is None else (True, extracted_response)
        )

    async def a_generate_oai_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[Any] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """Generate a reply using autogen.oai asynchronously."""
        iostream = IOStream.get_default()
        parent_context = contextvars.copy_context()

        def _generate_oai_reply(
            self, iostream: IOStream, *args: Any, **kwargs: Any
        ) -> Tuple[bool, Union[str, Dict, None]]:
            with IOStream.set_default(iostream):
                return self.generate_oai_reply(*args, **kwargs)

        memory_instruction = self.memory_reply_prompt.format(memory=self.memory_json)

        return await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: parent_context.run(
                _generate_oai_reply,
                self=self,
                iostream=iostream,
                messages=messages + memory_instruction,
                sender=sender,
                config=config,
            ),
        )

