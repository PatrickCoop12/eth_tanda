from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

cdp= CdpAgentkitWrapper()
toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)


tools = toolkit.get_tools()
llm = ChatOpenAI(model='gpt-4o-mini')
react_agent = create_react_agent(llm, tools)

def generate_response(inquiry:str):
    response = react_agent.invoke({"messages":[HumanMessage(content=inquiry)]})

    return response

