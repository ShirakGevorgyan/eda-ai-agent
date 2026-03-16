import os
import time
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from app.services.rag.vector_store import VectorStoreService
from app.core.config import settings

class EDAAgent:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()

        self.retriever_tool = Tool(
            name="eda_knowledge_base",
            func=self.retriever.invoke,
            description="Use this to search inside SDC, Verilog, and EDA files."
        )
        self.list_files_tool = Tool(
            name="list_data_files",
            func=lambda x: os.listdir("data"),
            description="Use this to see names of files in the data folder."
        )
        self.tools = [self.retriever_tool, self.list_files_tool]

    def _get_llm(self, model_name: str):
        if model_name == settings.LOCAL_MODEL_NAME:
            # A1-A2 Level: Local LLM can be slow, so we wait more.
            # We use ChatOllama for llama3.
            return ChatOllama(
                model=model_name,
                # Note: No '/v1' for ChatOllama, just the base URL
                base_url=settings.OLLAMA_BASE_URL.replace("/v1", ""),
                temperature=0,
                num_predict=512, # Limit response length to save CPU
            )
        else:
            return ChatOpenAI(
                model=model_name, 
                api_key=settings.OPENAI_API_KEY,
                temperature=0
            )

    def ask(self, question: str, model_name: str = settings.DEFAULT_MODEL):
        llm = self._get_llm(model_name)
            
            # Create the agent
        agent = create_react_agent(llm, self.tools)

        if model_name == settings.LOCAL_MODEL_NAME:
            system_instruction = (
                "You are an EDA Expert. You have 2 tools: 'list_data_files' and 'eda_knowledge_base'.\n"
                "If the user asks about a file, immediately call 'eda_knowledge_base' with the filename.\n"
                "After you get the file content, give the final answer. Be brief."
            )
        else:
                system_instruction = (
                "You are a Synopsys EDA Expert. Use your tools to search local files "
                "and answer the question based on the technical data found."
            )
            
        full_input = f"{system_instruction}\n\nQuestion: {question}"
        inputs = {"messages": [("user", full_input)]}
            
            # Start the agent (we use a bigger timeout implicitly by letting it run)
        try:
            response = agent.invoke(inputs)
            
            # Debug: Check if the model actually used a tool (you'll see this in terminal)
            return response["messages"][-1].content
        except Exception as e:
            return f"Agent Error: {str(e)}"