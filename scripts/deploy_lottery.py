from scripts.helpful_scripts import fund_with_link, get_account, get_contract
from brownie import Lottery, config, network
import time


#  address _priceFeedAddress,
#         address _vrfCoordinator,
#         address _link,
#         uint256 _fee,
#         bytes32 _keyhash
def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator_address").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
    )

    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")
    print(value)


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(
        lottery.address,
    )
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    # We need to wait for the call back by the chainlink nodes.
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
