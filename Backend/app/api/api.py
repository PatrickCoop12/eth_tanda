from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
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

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a customer service agent assigned to assist clients by collecting pertinent information about how their group would like to structure their Etherium Tanda association, and answer any questions they may have about tandas or smart contracts. Use the conversation history below to respond to questions conversationally.\n {chat_history}"),
    ('user', "{input}"),
    ("placeholder", "{agent_scratchpad}")])

agent = create_tool_calling_agent(llm, tools=tools, prompt=prompt2)

tanda_formation_agent = AgentExecutor(agent=agent, tools=tools, verbose=True)


def generate_response(inquiry:str, chat_history:str):
    response = tanda_formation_agent.invoke({"input":[HumanMessage(content=inquiry),
                                             "chat_history": chat_history]})

    return response

