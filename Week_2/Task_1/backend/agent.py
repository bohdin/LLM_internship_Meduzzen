from langchain_community.chat_models.openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os
from tools import tools

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL")

gpt_chat = ChatOpenAI(model="gpt-4", api_key=API_KEY)
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=gpt_chat,
    memory=memory,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)