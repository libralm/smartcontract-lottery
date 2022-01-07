from os import link
from brownie import (
    network,
    accounts,
    MockV3Aggregator,
    config,
    Contract,
    LinkToken,
    VRFCoordinatorMock,
)
from brownie.network import web3
import eth_account
from web3 import Web3

DECIMALS = 8

STARTING_PRICE = 400000000000

LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["eth-mainnet-fork", "bsc-main-fork"]


def getAccount():
    print("network name:", network.show_active())
    if network.show_active() in (
        LOCAL_BLOCKCHAIN_ENVIRONMENT
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print("local network")
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["METAMASK_ACCOUNT2_PRIVATE_KEY"])
        # return accounts.load("metamast-account2")


def deploy_mock():
    account = getAccount()
    if len(MockV3Aggregator) <= 0:
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": account}
        )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})


contract_to_mock = {
    "usd_price_feed": MockV3Aggregator,
    "vrf_cordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This funtion will grab the contract addresses from the brownie config if defined, otherwise, it will deploy a mock version of that contract, and return that mock contract.
    Args:
    contract_name(string)
    Returns:
        brownie.network.contract.ProjectContract: The most recently deloyed version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        print(f"contract_type的长度:{len(contract_type)}")
        if len(contract_type) <= 0:
            deploy_mock()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract
