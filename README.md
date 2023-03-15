# e

takes a fixed point number, returns e^x

### Why the silly name?

This project features higher math functions for EVM in the form of callable smart contracts.  This is made possible almost entirely by tables of pre-computed values.... magic numbers.

### What's the problem here?

Tested locally, everything seems to work great.  Test nets: not so much.

I assume this is related to version incompatibilities, however, it's nearly certain that my test cases are not written correctly.  Instead of testing direct output, they examine the logs.  The numerical tests are satisfied by figures delivered as emission events...

So, I tried to rewrite this in solidity and yul, only to find that fixed point numbers are available (only in) solidity, but you cannot write to or from them.  Heading to remix, I try to compile and upload through their weird webapp, and I find that the compiler is using version 0.2.16?  The current version is really dissimilar.  So, I rewrite for vyper 0.2.16 (from 0.3.7) and I deploy to a testnet successfully.  Any time I query the contract, I receive a type error.  It seems that inputs are being received always as bytes32 (or some similar literal), and casting to a decimal crashes is ways that I didn't encounter when testing locally with version 0.3.7

### Why the heck are we doing this?

I implemented a gaussian curve in a contract when I made a new financial derivative for my master's thesis.  It was during this process that I realized the horrible state of computing (pun intended huehuehue) on EVM, nearly devoid of any math outside of integer operations.  So, I feel kind of responsible to bring some aspects of scientific computing to the blockchain... I guess we call it DeSci?

### What do I want from this audit?

1. I want to understand how the heck to compile and deploy vyper contracts correctly, without using remix or some other crutch.  I'm aware that brownie is actually the tool to use, but every bit of documentation or youtube on the subject is the SAME USELESS example, deploying in two lines a built-in cookie-cutter "Token".  The method in the docs is not relevant.

2. I want this to receive a call with a decimal number as a literal, and output a decimal number (I guess as a literal, as well?  no 0x?)

3. Some kind of gas fee study, to see how much it actually will cost to deploy to mainnet a whole mess of contracts similar to this one, and whether or not it makes sense to call this function instead of including it in every binary that would use the function.  I imagine there will be some magical coefficient that indicates how many calls will be equal to an independent deployment...

# RUNNINNG THE TESTS

    source venv/bin/activate

or make your own environment with 

    pip3 install -r requirements.txt

Then,

cd sandbox && brownie test -s

