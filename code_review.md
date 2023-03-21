# Cyfrin Code Review

| Title       | Details         |
| ----------- | --------------- |
| Date        | 2023-03-20      |
| Author      | Patrick Collins |
| Reviewer    | Alex Roan       |
| Commit Hash | `e652e60`       |

# Feedback

## Questions
1. Why is `ask` not a view function? What is the purpose of emitting a log when someone makes an ask? 
   1. If you're emitting logs so you can write tests, you can mitigate this by having these be view functions
   2. You could also just [use the return value](https://ethereum.stackexchange.com/questions/92603/how-to-get-the-return-value-of-a-transaction-instead-of-the-transaction-receipt) instead of emitting events
2. I don't understand this question, could you elaborate? 
   1. "2. I want this to receive a call with a decimal number as a literal, and output a decimal number (I guess as a literal, as well?  no 0x?)"

## Code Layout
For future reference, you can use the [chainlink-mix](https://github.com/smartcontractkit/chainlink-mix) or [yearn-strategy-mix](https://github.com/brownie-mix/yearn-strategy-mix) for Brownie templates. 

1. Code isn't compiling since `tab: constant(decimal[10][10])` should be `tab: constant(decimal[9][5])`
2. Place your [test fixtures](https://docs.vyperlang.org/en/stable/style-guide.html#fixtures) in a `conftest.py` file. 
3. No need for a `sandbox` folder, you can place all your code in the same directory as the `requirements.txt` and `README.md` (this is a stylistic suggestion though)
4. `brownie` is recommended to install with `pipx`, which places brownie into a virtual environment. Once in a virtual environment, to add packages, you'd have to `inject` packages into the `brownie` virtual environment. This can be accomplished as such:
```
pipx inject eth-brownie numpy
```

## README.md feedback

A readme should have the following sections:
1. Getting Started
   1. Requirements
   2. Quickstart
2. Usage
   1. Base usage
   2. Running tests

I've created a `README_cyfrin.md` with details. 

## Security

1. Use [GitHub Dependabot](https://github.com/dependabot) to update packages in `requirements.txt`, and only use dependencies that you need. This repo only needs:
```bash
numpy==1.24.2
```
Remove everything else from `requirements.txt`. You can optionally add all the dependencies from `eth-brownie`, but I recommend installing brownie with `pipx` still. 

## Code Quality

I am creating a PR to help give examples of the following suggestions. 

1. Variables named `a`,`x` and `y` are too non-descriptive, use more descriptive names. 
   1. Example:
```python
def change_owner(a: address):
```
to
```python
def change_owner(new_owner: address):
```
2. Add [natspec](https://docs.vyperlang.org/en/stable/natspec.html#example) to functions and contracts to explain their functionality to users. 
3. Variables in Vyper are `private` by default. You don't need to use the [keyword private](https://github.com/SamReeves/e/blob/e652e60c52413012aef5692ad18c7acb952739b0/sandbox/contracts/pi.vy#L13)
4. [Never import `*`](https://github.com/SamReeves/e/blob/e652e60c52413012aef5692ad18c7acb952739b0/sandbox/tests/e_test.py#L2), you want to import exactly the modules you'll be working with 
5. Whenever you send a transaction in `brownie`, it's best practice to `wait` for it to finish, otherwise, you'll run into errors like `brownie.exceptions.RPCRequestError: Web3 is not connected.`
6. When creating loops, it's best practice to use an `_` if the variable in the loop isn't used. ie:
```python
for _ in range(100):
```
7. Remove `print` statements from tests
8. Use `brownie.reverts` instead of `pytest.reverts`. `pytest.reverts` is deprecated. 
9. Don't use "magic numbers". A "magic number" is a number without any explanation of what it is, for example:
```python 
TAB: constant(decimal[9][5]) = [[3.1415926536]]
```
9, 5, and 3.1415926536 are all "magic". It would be better if they were assigned to constants which said what they were for readability.
s
```python
ARRAY_X: constant(uint256) = 9
ARRAY_Y: constant(uint256) = 5
PI: constant(decimal) = 3.1415926536
```

10. Don't need to restore a memory variable as another variable:
```python
def tau_to_the(_x: decimal) -> decimal:
    x: decimal = _x # remove this line and just use _x
```
11.  Have internal function start with an `_`

```python
def _tau_to_the(_x: decimal) -> decimal:
```
12. Consider using the [Fixed](https://eth-brownie.readthedocs.io/en/stable/api-convert.html?highlight=fixed168x10#fixed) package for `decimal` inputs to Vyper contracts.

## Opinionated Code Quality

The following are my opinionated suggestions on code formatting.

1. I prefer this ordering:

```
// version
// imports
// errors
// interfaces
// Structs
// State variables
// Events
// Modifiers
// Functions

// Layout of Functions:
// constructor
// receive function (if exists)
// fallback function (if exists)
// external
// internal
// view & pure functions
```

2. Have storage variables start with `s_`, immutables with `i_`, and constants all uppercase. ie:
```python
s_owner: address
```

3. Have all storage variables private, and create getters for them

For example:

```python
s_owner: address
# 
# ...code
# 
@external
@view
def get_owner() -> address:
    return self.s_owner
```

4. Use a `get_account` function to help with accounts

When you're testing locally, you'll often want to use a different account than when you're testing. Using a function that can handle which network you're on can make it easier to swap accounts between local, testnet, and mainnet chains. 


## Help on running tests on testnets

1. Get an [API Key from Alchemy](https://www.alchemy.com/) for Sepolia
2. Run the following:
```
brownie networks add Ethereum sepolia host=<https://alchemy-key-url> chainid=11155111
```
3. Set your `PRIVATE_KEY` in a file named `.env`. 
4. Deploy an `e` contract:
```
brownie run scripts/deploy_e.py --network sepolia
```
[Example contract](https://sepolia.etherscan.io/address/0xdAA85A6A84F543AD833dAcd24D02F35ed7470912#code)