# e

takes a fixed point number, returns e^x

## Why the silly name?

This project features higher math functions for EVM in the form of callable smart contracts.  This is made possible almost entirely by tables of pre-computed values.... magic numbers.

# Getting Started

## Requirements

- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - You'll know you did it right if you can run `git --version` and you see a response like `git version x.x.x`
- [Python](https://www.python.org/downloads/)
  - You'll know you've installed python right if you can run:
    - `python --version` or `python3 --version` and get an output like: `Python x.x.x`
- [pipx](https://pypa.github.io/pipx/installation/)
  - `pipx` is different from [pip](https://pypi.org/project/pip/)
  - You may have to close and re-open your terminal
  - You'll know you've installed it right if you can run:
    - `pipx --version` and see something like `x.x.x.x`
- [eth-brownie (brownie)](https://eth-brownie.readthedocs.io/en/stable/install.html)
  - We recommend using `pipx` but you can [follow the brownie documentation](https://eth-brownie.readthedocs.io/en/stable/install.html) for other installation methods.
  - You'll know you've done it right if you run `brownie --version` and see an output like `Brownie v1.19.3 - Python development framework for Ethereum`

## Quickstart

1. Clone repo and compile

```bash
git clone https://github.com/SamReeves/e
cd e
brownie compile
```

2. Install dependencies

If `brownie` is installed with `pipx` run:

```
pipx inject eth-brownie numpy
```

To add `numpy`, otherwise:

```
pip install -r requirements.txt
```

3. You're ready to go!

Run tests:

```
brownie test -s
```

## Deploying to a testnet/mainnet

1. Add your network

You can add the network that you'd like to work with by running:

```
brownie networks add Ethereum <YOUR_NETWORK> host=<YOUR_RPC_URL> chainid=<CHAIN_ID>
```

Or, set your `WEB3_INFURA_PROJECT_ID` [environment variable](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) to work with [brownie's built-in networks](https://eth-brownie.readthedocs.io/en/stable/network-management.html?highlight=web3_infura_project_id#using-infura).

2. Set your private key
  
Set your `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. If you get lost, you can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/).

You'll also need testnet ETH if working on a testnet. You can get ETH into your wallet by using the [faucets located here](https://faucets.chain.link/). If you're new to this, [watch this video.](https://www.youtube.com/watch?v=P7FX_1PePX0). Look at the `sepolia` section for those specific testnet faucets.

You can add your environment variables to a `.env` file. You can use the `.env.exmple` as a template, just fill in the values and rename it to '.env'. Then, uncomment the line `# dotenv: .env` in `brownie-config.yaml`

Here is what your `.env` should look like:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
```

AND THEN RUN `source .env` TO ACTIVATE THE ENV VARIABLES
(You'll need to do this every time you open a new terminal, or [learn how to set them easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))

![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+) **WARNING** ![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+)

DO NOT SEND YOUR PRIVATE KEY WITH FUNDS IN IT ONTO GITHUB

Otherwise, you can build, test, and deploy on your local environment.

You can also use brownie's built-in [account management](https://eth-brownie.readthedocs.io/en/stable/account-management.html) for more security. 

3. Run the deploy script

```
brownie run scripts/deploy_e.py --network <network_name>
```

## Gas Coverage

```
brownie test --gas
```

This will give you an output like:

```
e <Contract>
   ├─ constructor  -  avg: 640077  avg (confirmed): 640077  low: 640077  high: 640077
   ├─ ask          -  avg:  39982  avg (confirmed):  40063  low:  22757  high:  41266
   ├─ change_owner -  avg:  26362  avg (confirmed):  28270  low:  22548  high:  28270
   └─ unalive      -  avg:  13915  avg (confirmed):  13915  low:  13915  high:  13915
```

With gas estimates of each function. You can multiply those by gas pricing to get how much they will cost. 

Example:
```bash
gas_amount * gas_price * native_token_price = total_cost_of_transaction

# ETH Mainnet Costs
640077 gas * 0.000000012533291801 ETH (~12 GWEI) * $1,800/ETH =  $14.440089268995619

# Arbitrum Costs
640077 gas * 0.0000000001 ETH (~0.1 GWEI) * $1,800/ETH =  $0.11

# Polygon Costs
640077 gas * 0.000000119252126067 MATIC (~119 GWEI) * $1.11/MATIC =  $0.08
```

## Testnet Tests

To run a test on a testnet, do the following:

1. Add an account named `not_owner` with a new private key

```
brownie accounts new <id>
```
Then enter your private key and a password. 

2. Add sepolia ETH to that private key & your private key associated with `PRIVATE_KEY`

3. Run the following:

```
brownie test -k test_integration_zero --network sepolia
```

You'll see a passing test. 