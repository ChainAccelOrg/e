import pytest
from brownie import chain
from scripts.helper_functions import get_account, network
import random
import numpy as np

random.seed(hash(float("inf")))
start = chain.time()
base = 2.718281828459045


def test_integration_zero(e_power):
    if network.show_active() not in ["sepolia", "mainnet"]:
        pytest.skip("Only for testnet testing")
    tx = e_power.ask("0.0", {"from": get_account(id="not_owner")})
    tx.wait(1)
    tx.info()
    assert np.isclose(float(tx.events["lookup"]["y"]), 1)
