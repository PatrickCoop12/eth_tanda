// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract Calculator{

    uint256 result; 

    constructor(uint256 _result) {
        result = _result;
    }

    
    

    // Frequency of contributions is based on a weekly cycle. 
    // A week contains 7 days so if the frequency is set to 1 then it will be once every week. If you wanted for example to make 3 weeks then we would have set frequency to 2, and there would be one contribution made every other week as opposed to three contributions made every week.
    // Note: There are no restrictions on how many times a user can contribute. This is just an implementation detail. We will allow the contract owner to change this in future releases of the dApp so that users can control their
    


    function add(uint256 num) public returns(uint256) {
        result += num;

        return result;
    }

    function get() public view returns(uint256) {

        return result;
    }


}