from crewai import Agent, Task, Crew, LLM
from crewai_tools import EXASearchTool
from langchain_openai import ChatOpenAI
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper

tanda_customer_service_agent = Agent(
    role= "You are a customer service agent assigned to assist clients by collecting pertinent information about how their group would like to structure their Etherium Tanda association, and answer any questions they may have about tandas or smart contracts.",
    goal= "Answer client questions and collect all information required to structure their Tanda association in the form of a ETH smart contract. This includes the total number of members in the group, how frequently contributions will be collected, amount of member contributions, at what interval will the pot be distributed, and all ETH cryptocurrency wallet addresses of members participating in the Tanda association. If any information is missing please ask the client for the information, and let them what information is needed.",
    backstory= "a tanda is a regional version of a rotating savings and credit association (ROSCA). It is a form of a short-term no-interest loan among a group of friends and family where they contribute money to a pool that is then rotated between the members. As an example, a tanda is formed between ten friends and family. Each member gives $100 USD every two weeks to the group's organizer. At the end of the month, one participant gets the pot, $2000. Or, each member gives $100 weekly, and each week one of the ten participants get the pot ($1,000). This continues until each member has received the pot. This concept is being adapted to blockchain technology for decentralized processing. You are an expert on this service and how smart contracts work.",
    llm= "gpt-4o-mini",
    tools= [EXASearchTool()],
)

agreement_underwriter = Agent(
    role= "Use the information received from customer service agent to complete smart contract template structuring the agreement of tanda association between members",
    goal= "Reference the information provided to create a solidity smart contract  to form tanda association in the specifications noted by the client inclusive of the member wallet addresses. Provide the contract to the deployment agent for further processing.",
    #goal= "Reference the information provided to complete solidity smart contract code template used to form tanda association. Provide the contract to the deployment agent for further processing.",
    backstory= "you are an expert in underwriting etherium smart contracts with a keen eye for detail.",
    llm= "gpt-4o-mini",
    #tools= [Tanda_contract_template],
)

deployment_agent = Agent(
    role= "Compile and deploy soliity smart contract code to finalize and create Tanda association",
    goal= "Reference the smart contract code provided to compile and deploy smart contract to blockchain using the tools at your disposal. Contracts need to first be compiled and then deployed in two separate steps.",
    backstory= "You are an expert in deploying smart contracts to the blockchain",
    llm= "gpt-4o-mini",
    tools= [CdpToolkit],
)

qa_and_gather_info = Task(
    description= "Gather information required to create Tanda association, and answer any clarifying questions clients may have about tandas, smart contracts, and how the tanda association would work on the blockchain .",
    agent= tanda_customer_service_agent,
    expected_output= "Final output should be the information required to form the smart contract in the form of a list. If responding to a question or asking for additional information, the output response to the client should be conversational until required information is received for final output.",
    human_input=True,
)

underwrite_contract = Task(
    description= "Use information provided by customer service agent to create a smart contract in the solidity language to forming the tanda association.",
    #description= "Use information provided by customer service agent to complete the solidity smart contract code forming the tanda association.",
    agent= agreement_underwriter,
    expected_output= "The tanda association smart contract file in JSON format for compiling and deployment.",
)

compile_and_deploy_contract = Task(
    description= "Compile and deploy the solidity smart contract code in two separate steps and make note of the contract address",
    agent= deployment_agent,
    expected_output= "A confirmation that the tanda association smart contract has been deployed, and the ETH smart contract address for members to send their contributions and monitor activity."
)

