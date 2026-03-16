import os
import time
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from app.services.rag.vector_store import VectorStoreService
from app.core.config import settings

from app.services.ai_agent.tools import (
    list_data_files, 
    verilog_syntax_check, 
    timing_calculator
)
class EDAAgent:
    """
    This class creates the 'Brain' of our AI.
    It can think and use 4 different tools
    """
    def __init__(self):
        
        # Step 1: Connect to our Memory (Vector Store)
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()

        # Step 2: Define Tools for the AI
        # Tool 1: Searches inside Verilog and SDC files
        self.retriever_tool = Tool(
            name="eda_knowledge_base",
            func=self.retriever.invoke,
            description="Use this to search inside SDC, Verilog, and EDA files."
        )
        # Combine all tools into one list
        # We use tools from tools.py + our retriever tool
        self.tools = [
            self.retriever_tool, 
            list_data_files, 
            verilog_syntax_check, 
            timing_calculator
        ]

    def _get_llm(self, model_name: str):
        """
        This function chooses the model.
        If the user picks llama3.1, it runs on your computer (Local).
        If not, it runs on OpenAI (Cloud).
        """
        if model_name == settings.LOCAL_MODEL_NAME:
            return ChatOllama(
                model=model_name,
                #just the base URL
                base_url=settings.OLLAMA_BASE_URL.replace("/v1", ""),
                temperature=0,
                num_predict=512, # Limit response length to save CPU :(
            )
        else:
            return ChatOpenAI(
                model=model_name, 
                api_key=settings.OPENAI_API_KEY,
                temperature=0
            )

    def ask(self, question: str, model_name: str = settings.DEFAULT_MODEL):
        """
        This function sends your question to the AI.
        It gives special instructions to the AI based on the model used.
        """
        # Initialize the selected LLM
        llm = self._get_llm(model_name)
            
        # Create the LangGraph Agent (The logic engine)
        agent = create_react_agent(llm, self.tools)

        if model_name == settings.LOCAL_MODEL_NAME:
            # Local models need very clear steps
            system_instruction = (
                "You are an EDA Expert. Follow these steps:\n"
                "1. Use 'list_data_files' to see what you have.\n"
                "2. Use 'eda_knowledge_base' to read technical files.\n"
                "3. Use 'verilog_syntax_check' if the user provides Verilog code.\n"
                "4. Use 'timing_calculator' for frequency and period math.\n"
                "Always be brief and accurate."
            )
        else:
            # OpenAI is smarter and follows general instructions well
            system_instruction = (
                "You are a Synopsys EDA Expert. You have tools for file search, "
                "Verilog syntax checking, and timing calculations. Use them to provide "
                "precise engineering answers."
            )
            
        # Prepare the input
        full_input = f"{system_instruction}\n\nQuestion: {question}"
        inputs = {"messages": [("user", full_input)]}
            
        #Run the Agent and handle errors
        try:
            response = agent.invoke(inputs)
            
            # Return the last message from the AI (the final answer)
            return response["messages"][-1].content
        except Exception as e:
            return f"Agent Error: {str(e)}"