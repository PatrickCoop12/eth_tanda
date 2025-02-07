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

# Initializing CDP tools for agent use
cdp= CdpAgentkitWrapper()
toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)

# Creating tool variable and binding with LLM to create agent
tools = toolkit.get_tools()
llm = ChatOpenAI(model='gpt-4o-mini')

prompt = ChatPromptTemplate.from_messages([
    ("system", "A tanda is a regional version of a rotating savings and credit association (ROSCA). "
               "It is a form of a short-term no-interest loan among a group of friends and family where they contribute "
               "money to a pool that is then rotated between the members. As an example, a tanda is formed between ten friends and family. "
               "Each member gives $100 USD every two weeks to the group's organizer. At the end of the month, one participant gets the pot, "
               "$2000. Or, each member gives $100 weekly, and each week one of the ten participants get the pot ($1,000). This continues until "
               "each member has received the pot. This concept is being adapted to blockchain technology for decentralized processing. You are an "
               "expert on this service and how smart contracts work.\n "
               "\n You are a customer service agent assigned to assist clients by collecting pertinent information about "
               "how their group would like to structure their Etherium Tanda association, and answer any questions they "
               "may have about tandas or smart contracts.Answer client questions and collect all information required to "
               "structure their Tanda association in the form of a ETH smart contract. This includes the total number of members in the group, "
               "how frequently contributions will be collected, amount of member contributions, at what interval will the pot be distributed, "
               "and all ETH cryptocurrency wallet addresses of members participating in the Tanda association. "
               "If any information is missing please ask the client for the information, and let them what information is needed."
               "\n Use the conversation history below to respond to questions conversationally."
               "\n {chat_history}"),
    ('user', "{input}"),
    ("placeholder", "{agent_scratchpad}")])

agent = create_tool_calling_agent(llm, tools=tools, prompt=prompt)

tanda_formation_agent = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Create generate response function that will be called on API requests
def generate_response(inquiry:str, chat_history:str):
    response = tanda_formation_agent.invoke({"input":[HumanMessage(content=inquiry)],
                                             "chat_history": chat_history})

    return response['output']

