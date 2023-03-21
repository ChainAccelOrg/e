import pytest
from brownie import chain, reverts
import random
import numpy as np

random.seed(hash(float("inf")))
start = chain.time()
base = 2.718281828459045


def test_init_owner(e_power):
    print(e_power.get_owner())


def test_zero(e_power, accounts):
    # Consider using the `Fixed` package for decimal inputs to vyper contracts
    # To make it more explicit, this will help as well when trying to do
    # arithmetic with regular integers and float
    # tx = e_power.ask(Fixed("0.0"), {"from": accounts[1]})
    tx = e_power.ask("0.0", {"from": accounts[1]})
    tx.wait(1)
    tx.info()
    assert np.isclose(float(tx.events["lookup"]["y"]), 1)


def test_one(e_power, accounts):
    tx = e_power.ask("1.0", {"from": accounts[1]})
    tx.wait(1)
    assert np.isclose(float(tx.events["lookup"]["y"]), base)


def test_one_to_nine(e_power, accounts):
    for i in range(1, 10):
        tx = e_power.ask(str(i), {"from": accounts[1]})
        tx.wait(1)
        real = np.exp(i)
        test = float(tx.events["lookup"]["y"])
        assert np.isclose(real, test)
        print(f"{i} = {real} = {test}")


def test_change_owner(e_power, accounts):
    tx = e_power.change_owner(accounts[1], {"from": accounts[0]})
    tx.wait(1)
    assert e_power.get_owner() == accounts[1]


def test_change_from_non_owner(e_power, accounts):
    with reverts():
        e_power.change_owner(accounts[1], {"from": accounts[2]})


def test_more_than_ten(e_power, accounts):
    with reverts():
        e_power.ask("10.0", {"from": accounts[1]})


def test_ask_negative(e_power, accounts):
    with reverts():
        e_power.ask("-1.0", {"from": accounts[1]})


def test_one_point_one(e_power, accounts):
    tx = e_power.ask("1.1", {"from": accounts[1]})
    tx.wait(1)
    real = np.exp(1.1)
    test = float(tx.events["lookup"]["y"])
    print(f"1.1 -> real {real} test {test}")
    assert np.isclose(real, test)


def test_one_point_zero_one(e_power, accounts):
    tx = e_power.ask("1.01", {"from": accounts[1]})
    tx.wait(1)
    real = np.exp(1.01)
    test = float(tx.events["lookup"]["y"])
    print(f"1.01 -> real {real} test {test}")
    assert np.isclose(real, test)


def test_min(e_power, accounts):
    tx = e_power.ask("0.000000001", {"from": accounts[1]})
    tx.wait(1)
    real = np.exp(0.000000001)
    test = float(tx.events["lookup"]["y"])
    print(f"0.000000001 -> real {real} test {test}")
    assert np.isclose(real, test)


def test_random_less_than_one(e_power, accounts):
    for _ in range(100):
        n = random.random()
        n = round(n, 10)
        tx = e_power.ask(str(n), {"from": accounts[1]})
        tx.wait(1)
        real = np.exp(n)
        test = float(tx.events["lookup"]["y"])
        print(f"{n} -> real {real} test {test}")
        assert np.isclose(real, test)


def test_random_less_than_ten(e_power, accounts):
    for _ in range(100):
        n = random.random() * 10
        n = round(n, 10)
        tx = e_power.ask(str(n), {"from": accounts[1]})
        tx.wait(1)
        real = np.exp(n)
        test = float(tx.events["lookup"]["y"])
        print(f"{n} -> real {real} test {test}")
        assert np.isclose(real, test)


def test_max(e_power, accounts):
    tx = e_power.ask("9.999999999", {"from": accounts[1]})
    tx.wait(1)
    real = np.exp(9.999999999)
    test = float(tx.events["lookup"]["y"])
    print(f"9.999999999 -> real {real} test {test}")
    assert np.isclose(real, test)


def test_unalive(e_power, accounts):
    tx = e_power.unalive({"from": accounts[0]})
    tx.wait(1)

    # UNCOMMENT TO SEE IF THE CONTRACT IS ALIVE
    # e_power.ask('1.0', {'from': accounts[1]})
