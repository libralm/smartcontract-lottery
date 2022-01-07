import math
from os import link
from brownie import (
    config,
    accounts,
    Lottery,
    network,
    MockV3Aggregator,
    Contract,
    LinkToken,
    recevier,
)
from brownie.network import contract
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
    deploy_mock,
    getAccount,
    get_contract,
)
import web3
from web3.main import Web3


def deploy_lottery():
    account = getAccount()
    # if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
    #     price_feed_address = config["networks"][network.show_active()]["usd_price_feed"]
    #     link_token = config["networks"][network.show_active()]["link_token"]
    #     vrf_cordinator = config["networks"][network.show_active()]["vrf_cordinator"]
    #     key_hash = config["networks"][network.show_active()]["key_hash"]
    #     fee = config["networks"][network.show_active()]["fee"]

    # else:
    #     deploy_mock()
    #     price_feed_address = MockV3Aggregator[-1].address

    print("网络名字：", network.show_active())
    lottery = Lottery.deploy(
        get_contract("usd_price_feed").address,
        get_contract("vrf_cordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["key_hash"],
        Web3.toWei(config["networks"][network.show_active()]["fee"] * 1, "ether"),
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def fund_link_to_me():
    account = getAccount()
    link_token = Contract.from_explorer(get_contract("link_token").address)
    tx = link_token.transfer(account, 100000000000000000, {"from": account})
    tx.wait(1)


def deploy_recevier():
    account = getAccount()
    recevier.deploy({"from": account})


def withdraw_recevier():
    account = getAccount()
    rec = recevier[-1]
    rec.withdraw({"from": account})


def startlottery():
    account = getAccount()
    # 0x64CDF2e13bB4B545D51E1A57aa221FbD2Bbf5Ae1
    lottery = Lottery[-1]
    link_token = Contract.from_explorer(get_contract("link_token").address)
    lottery.openLottery({"from": account})
    tx = link_token.transfer(lottery.address, 10000000000000000000, {"from": account})
    tx.wait(1)
    enterance_fee = lottery.getEnteranceFee()
    for num in range(0, 3):
        lottery.enter({"from": account, "value": enterance_fee})
    tx1 = lottery.startLottery({"from": account})
    tx1.wait(1)
    lottery.closeLottery({"from": account})


def openLottery():
    account = getAccount()
    lottery = Lottery[-1]
    lottery.openLottery({"from": account})


def withdraw():
    account = getAccount()
    # Fetching from a remote source
    # contract = Contract.from_explorer("0x65fa5bb7eb3Fa3Fa11a4F1AB3aDAc805dc85353C")
    # print(contract)
    lottery = Lottery[-1]
    lottery.withdraw({"from": account})


def isRunLottery():
    account = getAccount()
    lottery = Lottery[-1]
    isRun = lottery.isRunLottery({"from": account})


def getWinner():
    account = getAccount()
    lottery = Lottery[-1]
    num = lottery.getWinner()
    print(num)


def enter():
    account = getAccount()
    lottery = Lottery[-1]
    lottery.enter({"from": account})


# 9,900000000000000000
def main():
    # deploy_lottery()
    # startlottery()
    # openLottery()
    # isRunLottery()
    # withdraw()
    # getWinner()
    # deploy_recevier()
    withdraw_recevier()
