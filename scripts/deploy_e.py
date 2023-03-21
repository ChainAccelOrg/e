from brownie import e
from scripts.helper_functions import get_account, is_verifiable_contract

# Wait 5 blocks to verify
BLOCK_CONFIRMATIONS_FOR_VERIFICATION = 5


def deploy_e():
    account = get_account()
    e_contract = e.deploy({"from": account})

    if is_verifiable_contract():
        e_contract.tx.wait(BLOCK_CONFIRMATIONS_FOR_VERIFICATION)
        e.publish_source(e_contract)

    return e_contract


def main():
    deploy_e()
