import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from app.services.rag.vector_store import VectorStoreService
from app.core.config import settings

class EDAAgent:
    """
    This is an Expert AI Agent for Synopsys EDA.
    It can change its 'brain' (model) dynamically.
    """

    def __init__(self):
        # 1. Setup Memory and Tools (These don't change)
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()

        # Tool 1: Search inside documents
        self.retriever_tool = Tool(
            name="eda_knowledge_base",
            func=self.retriever.invoke,
            description="IMPORTANT: Use this tool to find information inside Verilog, SDC, and EDA files."
        )

        # Tool 2: List file names
        self.list_files_tool = Tool(
            name="list_data_files",
            func=lambda x: os.listdir("data"),
            description="Use this tool to see the names of all files in the data folder."
        )
        
        self.tools = [self.retriever_tool, self.list_files_tool]

    def _get_llm(self, model_name: str):
        """
        This helper function creates the LLM brain.
        It uses the model name sent from the UI.
        """
        if model_name == settings.LOCAL_MODEL_NAME:
            return ChatOpenAI(
                model=model_name,
                api_key="ollama",
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0
            )
        else:
            return ChatOpenAI(
                model=model_name, 
                api_key=settings.OPENAI_API_KEY,
                temperature=0
            )

    def ask(self, question: str, model_name: str = settings.DEFAULT_MODEL):
        """
        1. Create a new LLM with the selected model.
        2. Create a new Agent.
        3. Get the answer.
        """
        # Step 1: Initialize the brain with the specific model
        llm = self._get_llm(model_name)
        
        # Step 2: Create the LangGraph agent for this specific LLM
        agent = create_react_agent(llm, self.tools)

        # Step 3: Instructions for the expert
        system_instruction = (
            "You are a Synopsys EDA Expert. "
            "You must ALWAYS check the 'list_data_files' to see what files you have. "
            "Then use 'eda_knowledge_base' to read them. "
            "Now answer this question: "
        )
        
        full_input = f"{system_instruction} {question}"
        
        # Step 4: Run the agent
        inputs = {"messages": [("user", full_input)]}
        response = agent.invoke(inputs)
        
        return response["messages"][-1].content