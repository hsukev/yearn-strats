from util import genericStateOfStrat, genericStateOfVault
from brownie import Wei


def test_ops(token, strategy, chain, vault, whale, gov, strategist, ):
    print("----test ops----")

    debt_ratio = 10_000
    vault.addStrategy(strategy, debt_ratio, 0, 1000, {"from": gov})

    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    whalebefore = token.balanceOf(whale)
    vault.deposit(whalebefore, {"from": whale})
    strategy.harvest({"from": strategist})

    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)

    chain.sleep(2592000)
    chain.mine(1)

    strategy.harvest({"from": strategist})

    print("a3crv = ", strategy.balance() / 1e18)

    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)

    print(
        "\nEstimated APR: ",
        "{:.2%}".format(((vault.totalAssets() - 100 * 1e18) * 12) / (100 * 1e18)),
    )

    vault.withdraw({"from": whale})
    print("\nWithdraw")
    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)
    print("Whale profit: ", (token.balanceOf(whale) - whalebefore) / 1e18)


def test_revoke(token, strategy, vault, whale, gov, strategist):
    print("----test revoke----")

    debt_ratio = 10_000
    vault.addStrategy(strategy, debt_ratio, 0, 1000, {"from": gov})

    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    whalebefore = token.balanceOf(whale)
    vault.deposit(whalebefore, {"from": whale})
    strategy.harvest({"from": strategist})

    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)

    vault.revokeStrategy(strategy, {"from": gov})

    strategy.harvest({"from": strategist})

    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)


def test_reduce_limit(token, strategy, vault, whale, gov, strategist):
    print("----test reduce limit----")

    debt_ratio = 10_000
    vault.addStrategy(strategy, debt_ratio, 0, 1000, {"from": gov})

    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    whalebefore = token.balanceOf(whale)
    vault.deposit(whalebefore, {"from": whale})
    strategy.harvest({"from": strategist})

    # round off off dust
    dec = token.decimals()
    assert token.balanceOf(vault) // 10 ** dec == 0
    vault.updateStrategyDebtRatio(strategy, 5_000, {"from": gov})
    strategy.harvest({"from": strategist})

    genericStateOfVault(vault, token)
    assert token.balanceOf(vault) // 10 ** dec > 0
