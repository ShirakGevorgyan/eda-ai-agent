import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from app.services.rag.vector_store import VectorStoreService
from app.core.config import settings

class EDAAgent:
    """
    Expert AI Agent for Synopsys EDA.
    This class creates an AI that can answer questions using local tools.
    """

    def __init__(self):
        # 1. Setup the AI model
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME, 
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )

        # 2. Get the memory tool
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()

        # 3. Create the retriever tool
        self.retriever_tool = Tool(
            name="eda_knowledge_base",
            func=self.retriever.invoke,
            description="IMPORTANT: Use this tool to find information about Verilog, SDC, and EDA tools. "
                        "Always check this tool before answering questions about hardware design."
        )
        self.tools = [self.retriever_tool]

        # 4. Create the LangGraph Agent (Simple version)
        self.agent = create_react_agent(self.llm, self.tools)

    def ask(self, question: str):
        """
        We send a special instruction (System Message) + the User Question.
        """
        # We define who the AI is and what it should do
        system_instruction = (
            "You are a Synopsys EDA Expert. "
            "You must ALWAYS use the 'eda_knowledge_base' tool to check local files first. "
            "If the information is in the file, use it. "
            "Now answer this question: "
        )
        
        # Combine the instruction with the user's question
        full_input = f"{system_instruction} {question}"
        
        # Send to the agent
        inputs = {"messages": [("user", full_input)]}
        response = self.agent.invoke(inputs)
        
        # Return only the final text
        return response["messages"][-1].content