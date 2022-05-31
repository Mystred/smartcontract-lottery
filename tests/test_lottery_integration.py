from eth_account import Account
from brownie import network, Lottery
import pytest
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
)
from scripts.deploy_lottery import deploy_lottery


def test_can_pick_winner():

    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    # lottery = Lottery[-1]
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    fund_with_link(lottery)

    # Act
    lottery.endLottery({"from": account})
    time.sleep(200)

    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
