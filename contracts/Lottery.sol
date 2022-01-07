//SPDX-License-Identifier:MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/openzeppelin-contracts@4.4.1/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;

    uint256 public jackpot;

    mapping(address => uint256) sender_feed_map;

    uint256 usdEntryFee;

    uint256 MINIUM_USD = 10;

    address payable public winner;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        LOTTERY
    }

    LOTTERY_STATE public lottery_state;

    AggregatorV3Interface internal ethUsdPriceFeed;

    bytes32 internal keyHash;

    uint256 internal fee;

    uint256 public randomResult;

    bytes32 public _requestId;

    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfAddress,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    ) VRFConsumerBase(_vrfAddress, _linkToken) {
        usdEntryFee = MINIUM_USD * 10**18;
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        keyHash = _keyhash;
        fee = _fee;
    }

    function getJackpot() public view returns (uint256) {
        return jackpot;
    }

    function openLottery() public payable onlyOwner {
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function closeLottery() public payable onlyOwner {
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }

    function withdraw(address _tokenAddress) public payable onlyOwner {
        // Token token = new Token(_tokenAddress);
        // token.wowToken.transfer(owner(), token.balance);
    }

    function enter() public payable {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery system is not open,pls wait...."
        );
        uint256 costToEnter = getEnteranceFee();
        require(
            msg.value >= costToEnter,
            "Your investment must be greater than 50USD!"
        );
        jackpot += msg.value;
        players.push(payable(msg.sender));
    }

    // 0.013205513964834427 eth
    //0.094323605425493784 bnb
    //0.094903346002722249
    //0.190069672010439342
    function getEnteranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        //18decimals eth price
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        if (isRunLottery()) {
            randomRunLottery();
        }
    }

    function getLinkBalance() public view onlyOwner returns (uint256) {
        return LINK.balanceOf(address(this));
    }

    function getWinner() public view returns (address) {
        return winner;
    }

    function getRandomResult() public view returns (uint256) {
        return randomResult;
    }

    function getFee() public view onlyOwner returns (uint256) {
        return fee;
    }

    function isRunLottery() public view onlyOwner returns (bool) {
        require(
            LINK.balanceOf(address(this)) >= fee,
            "Not enough LINK - fill contract with faucet"
        );
        return true;
    }

    function randomRunLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.LOTTERY;
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
    }

    function sendLottery() public onlyOwner {}

    //Callback function can't contain other function
    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        require(randomness > 0, "random-not-found");
        randomResult = randomness;
        uint256 index = randomResult % players.length;
        winner = players[index];
        uint256 blance = (jackpot * 9) / 10;
        jackpot = 0;
        if (!winner.send(blance)) {
            jackpot = (blance * 10) / 9;
            return;
        }
        players = new address payable[](0);
        lottery_state == LOTTERY_STATE.OPEN;
    }

    receive() external payable {
        enter();
    }

    fallback() external payable {
        enter();
    }
}
