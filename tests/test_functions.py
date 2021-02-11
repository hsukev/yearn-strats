from util import genericStateOfStrat, genericStateOfVault
import brownie


def test_func(token, strategy, chain, vault, whale, gov, strategist, dai, crv):
    debt_ratio = 10_000
    vault.addStrategy(strategy, debt_ratio, 0, 1000, {"from": gov})

    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    whalebefore = token.balanceOf(whale)
    vault.deposit(whalebefore, {"from": whale})

    chain.sleep(2592000)
    chain.mine(1)

    strategy.balanceOfUnclaimedReward()
