from brownie import e
import pytest
from scripts.helper_functions import get_account


@pytest.fixture
def e_power():
    account = get_account()
    yield e.deploy({"from": account})
