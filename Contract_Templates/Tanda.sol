// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract Tanda {
    /// @dev Number of participants in the tanda
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
    
    /// @dev List of all members’ addresses
    address[] public members;
    
    /// @dev Tracks whether a member has contributed in the current cycle
    mapping(address => bool) public hasContributedThisCycle;
    
    /// @dev How many total contributions have been made this cycle
    uint256 public contributionsThisCycle;
    
    /// @dev Timestamp for when the current contribution cycle started
    uint256 public cycleStartTime;
    
    /// @dev Count of completed contribution cycles
    uint256 public cycleCount;
    
    /// @dev Next timestamp at or after which a distribution can occur
    uint256 public nextDistributionTime;
    
    /// @dev Tracks whether a member has received their one-time payout
    mapping(address => bool) public hasReceivedPayout;
    
    /// @dev Index for picking the next unpaid member in the `members` array
    uint256 public nextPayoutIndex;

    /**
     * @param _numMembers                  Number of participants in the tanda
     * @param _contributionFrequencyInWeeks How often they must contribute (in weeks)
     * @param _distributionIntervalInWeeks  How often the pot should be distributed (in weeks)
     * @param _contributionAmountInEther    Amount each member contributes per interval, in decimal Ether
     *                                      (e.g., 0.002 ether, 0.5 ether, 1 ether).
     * @param _members                     Array of member addresses (must match _numMembers in length)
     */
    constructor(
        uint256 _numMembers,
        uint256 _contributionFrequencyInWeeks,
        uint256 _distributionIntervalInWeeks,
        uint256 _contributionAmountInEther, // Pass something like 0.002 ether or 0.5 ether
        address[] memory _members
    ) {
        require(_members.length == _numMembers, "Members array size mismatch");
        for (uint256 i = 0; i < _numMembers; i++) {
            require(_members[i] != address(0), "Invalid member address");
        }
        
        numMembers = _numMembers;
        contributionFrequencyInWeeks = _contributionFrequencyInWeeks;
        distributionIntervalInWeeks = _distributionIntervalInWeeks;
        
        // Store the contribution amount in wei. Solidity automatically converts,
        // so if the constructor argument is 0.002 ether, that becomes 2000000000000000 wei.
        contributionAmount = _contributionAmountInEther;
        
        members = _members;
        
        // Initialize cycle and distribution timing
        cycleStartTime = block.timestamp;
        nextDistributionTime = block.timestamp + (distributionIntervalInWeeks * 1 weeks);
        
        cycleCount = 0;
        contributionsThisCycle = 0;
        nextPayoutIndex = 0;
    }

    /**
     * @notice Each member should call `contribute()` once per contribution cycle,
     *         sending exactly `contributionAmount` wei (equivalent to the specified decimal Ether).
     */
    function contribute() external payable {
        // Must be a valid member
        require(allPaidOut() == false, "Everyone has been paid out once, effectively ending the Tanda. Thank you for participating! Restart a new agreement if you'd like to continue with this Tanda." );
        
        require(isMember(msg.sender), "Not a registered member");
        // Must not have contributed already this cycle
        require(!hasContributedThisCycle[msg.sender], "Already contributed this cycle");
        // Must send the exact required contribution
        require(msg.value == contributionAmount, "Incorrect contribution amount");

        require(allPaidOut() == false, "Everyone has been paid out once. Thank you for participating! Restart a new agreement if you'd like to continue with this Tanda." );
        
        // Ensure the contribution is within the current cycle window
        uint256 cycleDuration = contributionFrequencyInWeeks * 1 weeks;
        require(
            block.timestamp < (cycleStartTime + cycleDuration),
            "Contribution window for this cycle is closed"
        );
        
        // Record contribution
        hasContributedThisCycle[msg.sender] = true;
        contributionsThisCycle += 1;

        // If all members have contributed this cycle, finalize the cycle
        if (contributionsThisCycle == numMembers) {
            finalizeCycle();
        }
    }

    /**
     * @notice Finalizes the current contribution cycle if either:
     *         1) The contribution window has passed, or
     *         2) All members have contributed.
     */
    function finalizeCycle() public {
        uint256 cycleDuration = contributionFrequencyInWeeks * 1 weeks;
        
        // Can only finalize if the window is past or everyone contributed
        require(
            block.timestamp >= (cycleStartTime + cycleDuration) ||
            contributionsThisCycle == numMembers,
            "Cannot finalize cycle yet"
        );

        // Advance to the next cycle
        cycleCount += 1;
        
        // Reset per-cycle contribution tracking
        for (uint256 i = 0; i < numMembers; i++) {
            hasContributedThisCycle[members[i]] = false;
        }
        contributionsThisCycle = 0;
        
        // Start a new cycle window from now
        cycleStartTime = block.timestamp;
    }

    /**
     * @notice Trigger the distribution of the entire contract balance to the next unpaid member
     *         if the current time is past `nextDistributionTime`.
     */
    function triggerDistribution() external {
        //require(
        //    block.timestamp >= nextDistributionTime,
        //    "It is not yet time for distribution"
        //);

        // Find the next member who hasn't been paid
        address payable recipient;
        bool found = false;

        for (uint256 i = 0; i < numMembers; i++) {
            // Round-robin search from nextPayoutIndex
            uint256 idx = (nextPayoutIndex + i) % numMembers;
            address member = members[idx];
            if (!hasReceivedPayout[member]) {
                recipient = payable(member);
                nextPayoutIndex = idx + 1; // Next time start from the next address
                found = true;
                break;
            }
        }
        require(found, "All members have already been paid");

        // Mark the recipient as paid and transfer full balance
        hasReceivedPayout[recipient] = true;
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to distribute");

        (bool success, ) = recipient.call{value: balance}("");
        require(success, "Transfer failed");

        // Schedule the next distribution time
        nextDistributionTime += (distributionIntervalInWeeks * 1 weeks);
    }

    /**
     * @dev Check if a given address is in the `members` array.
     */
    function isMember(address _addr) public view returns (bool) {
        for (uint256 i = 0; i < numMembers; i++) {
            if (members[i] == _addr) {
                return true;
            }
        }
        return false;
    }

    /**
     * @notice Helper to check if everyone has received the pot already.
     */
    function allPaidOut() public view returns (bool) {
        for (uint256 i = 0; i < numMembers; i++) {
            if (!hasReceivedPayout[members[i]]) {
                return false;
            }
        }
        return true;
    }

    /**
     * @dev Prevent direct ETH transfers outside `contribute()`.
     */
    receive() external payable {
        revert("Use contribute() to deposit");
    }
}
