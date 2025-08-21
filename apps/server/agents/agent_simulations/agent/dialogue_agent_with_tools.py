from typing import List, Optional
import requests  # Add this import
import json  # Add this import

# Remove LangChain imports we won't need
# from langchain.agents import AgentType, initialize_agent
from langchain.schema import AIMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI

from agents.agent_simulations.agent.dialogue_agent import DialogueAgent
from agents.conversational.output_parser import ConvoOutputParser
from config import Config
from memory.zep.zep_memory import ZepMemory
from services.run_log import RunLogsManager
from typings.agent import AgentWithConfigsOutput


class DialogueAgentWithTools(DialogueAgent):
    def __init__(
        self,
        name: str,
        agent_with_configs: AgentWithConfigsOutput,
        system_message: SystemMessage,
        model: ChatOpenAI,
        tools: List[any],
        session_id: str,
        sender_name: str,
        is_memory: bool = False,
        run_logs_manager: Optional[RunLogsManager] = None,
        **tool_kwargs,
    ) -> None:
        super().__init__(name, agent_with_configs, system_message, model)
        self.tools = tools
        self.session_id = session_id
        self.sender_name = sender_name
        self.is_memory = is_memory
        self.run_logs_manager = run_logs_manager
        self.api_url = "http://localhost:8090/agent/run"  # XAgent API endpoint

    def send(self) -> str:
        """
        Applies the XAgent to the message history
        and returns the message string
        """

        # Prepare the prompt as in the original code
        prompt = "\n".join(self.message_history + [self.prefix])
        
        # Prepare tools for XAgent API
        tools_list = []
        for tool in self.tools:
            # Extract tool information - this might need adjustment based on your tool structure
            tool_dict = {
                "name": getattr(tool, 'name', 'unnamed_tool'),
                "description": getattr(tool, 'description', 'No description available'),
                "parameters": {}  # You might need to add parameters based on tool args
            }
            tools_list.append(tool_dict)
        
        # Prepare payload for XAgent
        payload = {
            "task": prompt,
            "tools": tools_list,
            "model": "gpt-3.5-turbo",  # Use appropriate model name
            "history": self.message_history  # Include conversation history
        }
        
        try:
            # Call XAgent API
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            agent_response = result.get('response', 'No response from XAgent')
        except requests.exceptions.RequestException as e:
            agent_response = f"Error calling XAgent: {e}"
        
        # Create AI message with the response
        message = AIMessage(content=agent_response)
        
        # Handle memory if enabled
        if self.is_memory:
            memory = ZepMemory(
                session_id=self.session_id,
                url=Config.ZEP_API_URL,
                api_key=Config.ZEP_API_KEY,
                memory_key="chat_history",
                return_messages=True,
            )
            memory.human_name = self.sender_name
            memory.ai_name = self.agent_with_configs.agent.name
            memory.auto_save = False
            # Save the response to memory
            memory.save_ai_message(agent_response)
        
        return message.content