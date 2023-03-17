#@version 0.3.7
"""
@title pi^x
@license MIT
@author magic numbers
"""
owner: public(address)
event lookup:
    sender: address
    x: decimal
    y: decimal

_owner: private(address)
tab: constant(decimal[10][10]) = [[3.1415926536, 9.8696044011, 31.0062766803, 97.409091034, 306.0196847853, 961.3891935753, 3020.2932277768, 9488.5310160706, 29809.0993334462], [1.1212823532, 1.2572741157, 1.4097592791, 1.5807382019, 1.7724538509, 1.9874212249, 2.228460348, 2.498733263, 2.8017855133], [1.0115130699, 1.0231586906, 1.0349383881, 1.0468537062, 1.0589062061, 1.0710974672, 1.0834290873, 1.0959026821, 1.1085198863], [1.0011453853, 1.0022920826, 1.0034400932, 1.0045894188, 1.0057400608, 1.0068920207, 1.0080453001, 1.0091999004, 1.0103558232], [1.0001144795, 1.0002289722, 1.0003434779, 1.0004579968, 1.0005725288, 1.0006870739, 1.0008016321, 1.0009162034, 1.0010307878]]

@external
def __init__():
    self.owner = msg.sender

@internal
@pure
def pi_to_the(_x: decimal) -> decimal:
    x: decimal = _x
    y: decimal = 1.0
    for i in range(11):
        if x != 0.0:
            d: uint256 = convert(x, uint256)
            y *= tab[i][d]
            x -= convert(d, decimal)
            x *= 10.0
        else:
            break
    return y

@external
def ask(x: decimal) -> decimal:
    assert msg.sender != self.owner, "The owner cannot call this function."
    assert x >= 0.0, "Negative powers are not supported."
    assert x < 10.0, "The power limit is 9.999999999"

    y: decimal = self.pi_to_the(x)
    log lookup(msg.sender, x, y)
    return y

@external
def change_owner(a: address):
    assert msg.sender == self.owner, "Only the owner can change the owner."
    assert a != empty(address), "The new owner cannot be the zero address."
    assert a != self.owner, "The new owner cannot be the same as the old owner."
    self.owner = a

@external
def unalive():
    assert msg.sender == self.owner, "Only the owner can unalive the contract."
    selfdestruct(self.owner)