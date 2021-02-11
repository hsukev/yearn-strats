from util import genericStateOfStrat, genericStateOfVault
from brownie import Wei


def test_ops(token, strategy, chain, vault, whale, gov, strategist):
    print("\n----test ops----")

    debt_ratio = 10_000
    vault.addStrategy(strategy, debt_ratio, 0, 1000, {"from": gov})

    whalebefore = token.balanceOf(whale)
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
    print("\n----test revoke----")

    debt_ratio = 10_000
    vault.addStrategy(strategy, debt_ratio, 0, 1000, {"from": gov})

    strategy.harvest({"from": strategist})

    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)

    vault.revokeStrategy(strategy, {"from": gov})
    print("\n----revoked----")

    strategy.harvest({"from": strategist})

    genericStateOfStrat(strategy, token, vault)
    genericStateOfVault(vault, token)


def test_reduce_limit(token, strategy, vault, whale, gov, strategist):
    debt_ratio = 10_000
    print(f"\n----test debt ratio {debt_ratio}----")

    vault.addStrategy(strategy, debt_ratio, 0, 1000, {"from": gov})
    strategy.harvest({"from": strategist})

    # round off dust
    dec = token.decimals()
    assert token.balanceOf(vault) // 10 ** dec == 0

    debt_ratio = 5_000
    vault.updateStrategyDebtRatio(strategy, debt_ratio, {"from": gov})
    print(f"\n----test debt ratio {debt_ratio}----")
    strategy.harvest({"from": strategist})

    assert token.balanceOf(vault) // 10 ** dec > 0
