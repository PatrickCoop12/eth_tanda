// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract Calculator{

    address [] members;

    uint256 public numMembers;
    
    /// @dev How often each member must contribute, in weeks
    uint256 public contributionFrequencyInWeeks;
    
    /**
     * @dev How much each member must contribute at each interval, stored in wei.
     *      However, you can specify this value in the constructor as decimal Ether 
     *      (e.g., 0.002 ether, 0.5 ether, 1 ether, etc.).
     */
    uint256 public contributionAmount;
    
    /// @dev Interval (in weeks) at which the pot is distributed
    uint256 public distributionIntervalInWeeks;
    
    /// @dev Tracks whether a member has contributed in the current cycle
    //mapping(address => bool) public hasContributedThisCycle;
    
    /// @dev How many total contributions have been made this cycle
    //uint256 public contributionsThisCycle;
    
    /// @dev Timestamp for when the current contribution cycle started
    //uint256 public cycleStartTime;
    
    /// @dev Count of completed contribution cycles
    //uint256 public cycleCount;
    
    /// @dev Next timestamp at or after which a distribution can occur
    //uint256 public nextDistributionTime;
    
    /// @dev Tracks whether a member has received their one-time payout
    //mapping(address => bool) public hasReceivedPayout;
    
    /// @dev Index for picking the next unpaid member in the `members` array
    //uint256 public nextPayoutIndex;



    constructor(
        address[] memory _associationMembers,
        uint256 _numMembers,
        uint256 _contributionFrequencyInWeeks,
        uint256 _distributionIntervalInWeeks,
        uint256 _contributionAmount // Pass something like 0.002 ether or 0.5 ether
        ) 
        {
        require(_associationMembers.length == _numMembers, "Please ensure the number of association members match the number of wallet addresses provided.");
        for (uint256 i = 0; i < _numMembers; i++) {
            require(_associationMembers[i] != address(0), "Invalid member address");
        }
        
        members = _associationMembers;
        numMembers = _numMembers;
        contributionFrequencyInWeeks = _contributionFrequencyInWeeks;
        distributionIntervalInWeeks = _distributionIntervalInWeeks;
        contributionAmount = _contributionAmount;
        }


        


    function get_members() public view returns(uint256) {

        return numMembers;
    }

    function get_payout() public view returns(uint256) {

        return distributionIntervalInWeeks;
    }

    function get_contribution() public view returns(uint256) {

        return contributionAmount;
    }

    function get_compFreq() public view returns(uint256) {

        return contributionFrequencyInWeeks;
    }


}