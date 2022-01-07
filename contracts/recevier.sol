//SPDX-License-Identifier:MIT
pragma solidity ^0.8.0;

import "@openzeppelin/openzeppelin-contracts@4.4.1/contracts/access/Ownable.sol";

contract recevier is Ownable {
    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }

    receive() external payable {}

    fallback() external payable {}
}
