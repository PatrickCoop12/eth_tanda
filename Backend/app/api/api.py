from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initializing CDP tools for agent use
cdp= CdpAgentkitWrapper()
toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)
toolkit.get_tools()[13].invoke(input={"asset_id":"eth"})

def complete_contract_template(number_of_members: str, contribution_frequency: str, distribution_frequency: str,
                               contribution_amount: str, wallet_addresses: list) -> dict:


    contract_template = {'solidity_version': '0.8.26',
                         'solidity_input_json': '{"language":"Solidity","settings":{"remappings":[],"outputSelection":{"*":{"*":["abi","evm.bytecode"]}}},"sources":{"contracts/Calculator.sol":{"content":"// SPDX-License-Identifier: MIT\\npragma solidity ^0.8.26;\\n\\ncontract Tanda {\\n    /// @dev Number of participants in the tanda\\n    uint256 internal numMembers;\\n    \\n    /// @dev How often each member must contribute, in weeks\\n    uint256 internal contributionFrequencyInWeeks;\\n    \\n    /**\\n     * @dev How much each member must contribute at each interval, stored in wei.\\n     *      However, you can specify this value in the constructor as decimal Ether \\n     *      (e.g., 0.002 ether, 0.5 ether, 1 ether, etc.).\\n     */\\n    uint256 internal contributionAmount;\\n    \\n    /// @dev Interval (in weeks) at which the pot is distributed\\n    uint256 internal distributionIntervalInWeeks;\\n    \\n    /// @dev List of all members’ addresses\\n    address[] internal members;\\n    \\n    /// @dev Tracks whether a member has contributed in the current cycle\\n    mapping(address => bool) internal hasContributedThisCycle;\\n    \\n    /// @dev How many total contributions have been made this cycle\\n    uint256 internal contributionsThisCycle;\\n    \\n    /// @dev Timestamp for when the current contribution cycle started\\n    uint256 internal cycleStartTime;\\n    \\n    /// @dev Count of completed contribution cycles\\n    uint256 internal cycleCount;\\n    \\n    /// @dev Next timestamp at or after which a distribution can occur\\n    uint256 internal nextDistributionTime;\\n    \\n    /// @dev Tracks whether a member has received their one-time payout\\n    mapping(address => bool) internal hasReceivedPayout;\\n    \\n    /// @dev Index for picking the next unpaid member in the `members` array\\n    uint256 internal nextPayoutIndex;\\n\\n    /**\\n     * @param _numMembers                  Number of participants in the tanda\\n     * @param _contributionFrequencyInWeeks How often they must contribute (in weeks)\\n     * @param _distributionIntervalInWeeks  How often the pot should be distributed (in weeks)\\n     * @param _contributionAmountInWei    Amount each member contributes per interval, in wei\\n     *                                      (e.g., 0.05 ether = 50000000000000000 wei).\\n     * @param _members                     Array of member addresses (must match _numMembers in length)\\n     */\\n    constructor(\\n        uint256 _numMembers,\\n        uint256 _contributionFrequencyInWeeks,\\n        uint256 _distributionIntervalInWeeks,\\n        uint256 _contributionAmountInWei, // Pass something like 0.002 ether or 0.5 ether\\n        address[] memory _members\\n    ) {\\n        require(_members.length == _numMembers, \\"Members array size mismatch\\");\\n        for (uint256 i = 0; i < _numMembers; i++) {\\n            require(_members[i] != address(0), \\"Invalid member address\\");\\n        }\\n        \\n        numMembers = _numMembers;\\n        contributionFrequencyInWeeks = _contributionFrequencyInWeeks;\\n        distributionIntervalInWeeks = _distributionIntervalInWeeks;\\n        \\n        // Store the contribution amount in wei. Solidity automatically converts,\\n        // so if the constructor argument is 0.002 ether, that becomes 2000000000000000 wei.\\n        contributionAmount = _contributionAmountInWei;\\n        \\n        members = _members;\\n        \\n        // Initialize cycle and distribution timing\\n        cycleStartTime = block.timestamp;\\n        nextDistributionTime = block.timestamp + (distributionIntervalInWeeks * 1 weeks);\\n        \\n        cycleCount = 0;\\n        contributionsThisCycle = 0;\\n        nextPayoutIndex = 0;\\n    }\\n\\n    /**\\n     * @notice Each member should call `contribute()` once per contribution cycle,\\n     *         sending exactly `contributionAmount` wei (equivalent to the specified decimal Ether).\\n     */\\n    function contribute() external payable {\\n        // Must be a valid member\\n        require(allPaidOut() == false, \\"Everyone has been paid out once, effectively ending the Tanda. Thank you for participating! Restart a new agreement if you would like to continue with this Tanda.\\" );\\n        \\n        require(isMember(msg.sender), \\"Not a registered member\\");\\n        // Must not have contributed already this cycle\\n        require(!hasContributedThisCycle[msg.sender], \\"Already contributed this cycle\\");\\n        // Must send the exact required contribution\\n        require(msg.value == contributionAmount, \\"Incorrect contribution amount\\");\\n\\n        require(allPaidOut() == false, \\"Everyone has been paid out once. Thank you for participating! Restart a new agreement if you would like to continue with this Tanda.\\" );\\n        \\n        // Ensure the contribution is within the current cycle window\\n        uint256 cycleDuration = contributionFrequencyInWeeks * 1 weeks;\\n        require(\\n            block.timestamp < (cycleStartTime + cycleDuration),\\n            \\"Contribution window for this cycle is closed\\"\\n        );\\n        \\n        // Record contribution\\n        hasContributedThisCycle[msg.sender] = true;\\n        contributionsThisCycle += 1;\\n\\n        // If all members have contributed this cycle, finalize the cycle\\n        if (contributionsThisCycle == numMembers && block.timestamp >= (cycleStartTime + cycleDuration)) {\\n            finalizeCycle();\\n        }\\n    }\\n\\n    /**\\n     * @notice Finalizes the current contribution cycle if either:\\n     *         1) The contribution window has passed, or\\n     *         2) All members have contributed.\\n     */\\n    function finalizeCycle() public {\\n\\n        require(isMember(msg.sender), \\"Not a registered member\\");\\n        uint256 cycleDuration = contributionFrequencyInWeeks * 1 weeks;\\n        \\n        // Can only finalize if the window is past and everyone contributed\\n        require(\\n            block.timestamp >= (cycleStartTime + cycleDuration) &&\\n            contributionsThisCycle == numMembers,\\n            \\"Cannot finalize cycle until agreed distribution interval time has passed\\"\\n        );\\n\\n        // Advance to the next cycle\\n        cycleCount += 1;\\n        \\n        // Reset per-cycle contribution tracking\\n        for (uint256 i = 0; i < numMembers; i++) {\\n            hasContributedThisCycle[members[i]] = false;\\n        }\\n        contributionsThisCycle = 0;\\n        \\n        // Start a new cycle window from now\\n        cycleStartTime = block.timestamp;\\n    }\\n\\n    /**\\n     * @notice Trigger the distribution of the entire contract balance to the next unpaid member\\n     *         if the current time is past `nextDistributionTime`.\\n     */\\n    function triggerDistribution() external {\\n        //require(\\n        //    block.timestamp >= nextDistributionTime,\\n        //    \\"It is not yet time for distribution\\"\\n        //);\\n\\n        // Find the next member who has not been paid\\n        require(isMember(msg.sender), \\"Not a registered member\\");\\n        address payable recipient;\\n        bool found = false;\\n\\n        for (uint256 i = 0; i < numMembers; i++) {\\n            // Round-robin search from nextPayoutIndex\\n            uint256 idx = (nextPayoutIndex + i) % numMembers;\\n            address member = members[idx];\\n            if (!hasReceivedPayout[member]) {\\n                recipient = payable(member);\\n                nextPayoutIndex = idx + 1; // Next time start from the next address\\n                found = true;\\n                break;\\n            }\\n        }\\n        require(found, \\"All members have already been paid\\");\\n\\n        // Mark the recipient as paid and transfer full balance\\n        hasReceivedPayout[recipient] = true;\\n        uint256 balance = address(this).balance;\\n        require(balance > 0, \\"No funds to distribute\\");\\n\\n        (bool success, ) = recipient.call{value: balance}(\\"\\");\\n        require(success, \\"Transfer failed\\");\\n\\n        // Schedule the next distribution time\\n        nextDistributionTime += (distributionIntervalInWeeks * 1 weeks);\\n    }\\n\\n    /**\\n     * @dev Check if a given address is in the `members` array.\\n     */\\n    function isMember(address _addr) internal view returns (bool) {\\n        for (uint256 i = 0; i < numMembers; i++) {\\n            if (members[i] == _addr) {\\n                return true;\\n            }\\n        }\\n        return false;\\n    }\\n\\n    /**\\n     * @notice Helper to check if everyone has received the pot already.\\n     */\\n    function allPaidOut() public view returns (bool) {\\n        require(isMember(msg.sender), \\"Not a registered member\\");\\n        for (uint256 i = 0; i < numMembers; i++) {\\n            if (!hasReceivedPayout[members[i]]) {\\n                return false;\\n            }\\n        }\\n        return true;\\n    }\\n\\n    function confirmContributionAmount() public view returns (uint256) {\\n        require(isMember(msg.sender), \\"Not a registered member\\");\\n\\n        return contributionAmount;\\n    }\\n\\n    function confirmWhoHasContributed(address member_address) public view returns (bool) {\\n        require(isMember(msg.sender), \\"Not a registered member\\");\\n\\n        return hasContributedThisCycle[member_address];\\n    }\\n\\n    /**\\n     * @dev Prevent direct ETH transfers outside `contribute()`.\\n     */\\n    receive() external payable {\\n        revert(\\"Use contribute() to deposit\\");\\n    }\\n\\n}"}}}',
                         'contract_name': 'Tanda', 'constructor_args': {"_numMembers": f"{number_of_members}",
                                                                        "_contributionFrequencyInWeeks": f"{contribution_frequency}",
                                                                        "_distributionIntervalInWeeks": f"{distribution_frequency}",
                                                                        "_contributionAmountInWei": f"{contribution_amount}",
                                                                        "_members": wallet_addresses}}

    return contract_template


@tool
def deploy_contract(number_of_members: str, contribution_frequency: str, distribution_frequency: str,
                    contribution_amount: str, wallet_addresses: list):
    """ tool used to deploy a ETH Smart Contract to the blockchain. tool takes output from contract
    template completion tool to send API request completing deployment. Wallet addressses should be passed
    a list of strings. Invoke this tool to create contract for deployment. parameters passed for
    contribution and distribution frequency should be noted as a numeric string representing number of
    weeks for each interval."""

    try:
        contract_template = complete_contract_template(number_of_members, contribution_frequency,
                                                       distribution_frequency, contribution_amount, wallet_addresses)
        response = toolkit.get_tools()[1].invoke(input=contract_template)
        return response
    except:
        return "Something went wrong"


# Creating tool variable and binding with LLM to create agent
tools = [deploy_contract]
llm = ChatOpenAI(model='gpt-4o-mini')

prompt = ChatPromptTemplate.from_messages([
    ("system", "A tanda is a regional version of a rotating savings and credit association (ROSCA). "
               "It is a form of a short-term no-interest loan among a group of friends and family where "
               "they contribute money to a pool that is then rotated between the members. As an example, "
               "a tanda is formed between ten friends and family. Each member gives $100 USD every two "
               "weeks to the group's organizer. At the end of the month, one participant gets the pot, $2000."
               " Or, each member gives $100 weekly, and each week one of the ten participants get the pot ($1,000). "
               "This continues until each member has received the pot. This concept is being adapted to blockchain"
               " technology for decentralized processing. You are an expert on this service and how smart contracts "
               "work.\n \n You are a customer service agent assigned to assist clients by collecting pertinent "
               "information about how their group would like to structure their Etherium Tanda association, and "
               "answer any questions they may have about tandas, how they operate on the blockchain, and "
               "smart contracts. Answer client questions and collect all information required to structure their"
               " Tanda association in the form of a ETH smart contract. This includes the total number of members"
               " in the group, how frequently contributions will be collected, amount of member contributions in "
               "etherium, at what interval will the pot be distributed, and all ETH cryptocurrency wallet addresses "
               "of members participating in the Tanda association. If any information is missing please ask the client "
               "for the information, and let them what information is needed. Use the tools provided to complete the "
               "smart contract template with the details from the client and deploy the contract onto the blockchain. "
               "Once deployed provide the client with the contract address, ask the user to visit the 'Instructions "
               "After Deployment Page' to learn how to interact with their contract on the blockchain. This is a page "
               "on the website clients will use to interacting with you. \n \n Use the conversation history below to"
               " respond to questions conversationally.\n {chat_history}"),
    ('user', "{input}"),
    ("placeholder", "{agent_scratchpad}")])

agent = create_tool_calling_agent(llm, tools=tools, prompt=prompt)

tanda_formation_agent = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Create generate response function that will be called on API requests
def generate_response(inquiry:str, chat_history:str):
    response = tanda_formation_agent.invoke({"input":[HumanMessage(content=inquiry)],
                                             "chat_history": chat_history})

    return response

