#@version 0.3.7
"""
@title tau^x
@license MIT
@author magic numbers
"""
s_owner: address
event lookup:
    sender: address
    x: decimal
    y: decimal

TAB: constant(decimal[9][5]) = [[6.2831853072, 39.4784176044, 248.0502134424, 1558.545456544, 9792.629913129, 61528.9083888195, 386597.5331554293, 2429063.940114066, 15262258.858724454], [1.2017606702, 1.4442287084, 1.7356172606, 2.0857965623, 2.5066282746, 3.0123672753, 3.6201445156, 4.3505472993, 5.2283166382], [1.0185486997, 1.0374414537, 1.0566846436, 1.0762847698, 1.0962484528, 1.1165824361, 1.1372935884, 1.1583889057, 1.1798755136], [1.001839567, 1.003682518, 1.0055288592, 1.0073785969, 1.0092317374, 1.0110882868, 1.0129482514, 1.0148116376, 1.0166784516], [1.0001838046, 1.000367643, 1.0005515151, 1.0007354211, 1.0009193609, 1.0011033345, 1.0012873419, 1.0014713831, 1.0016554581]]

@external
def __init__():
    self.s_owner = msg.sender

@external
def ask(x: decimal) -> decimal:
    assert msg.sender != self.s_owner, "The owner cannot call this function."
    assert x >= 0.0, "Negative powers are not supported."
    assert x < 10.0, "The power limit is 9.999999999"

    y: decimal = self._tau_to_the(x)
    log lookup(msg.sender, x, y)
    return y

@external
def change_owner(new_owner: address):
    assert msg.sender == self.s_owner, "Only the owner can change the owner."
    assert new_owner != empty(address), "The new owner cannot be the zero address."
    assert new_owner != self.s_owner, "The new owner cannot be the same as the old owner."
    self.s_owner = new_owner

@external
def unalive():
    assert msg.sender == self.s_owner, "Only the owner can unalive the contract."
    selfdestruct(self.s_owner)

@external
@view
def get_owner() -> address:
    return self.s_owner

@internal
@pure
def _tau_to_the(_x: decimal) -> decimal:
    x: decimal = _x
    y: decimal = 1.0
    for i in range(11):
        if x != 0.0:
            d: uint256 = convert(x, uint256)
            y *= TAB[i][d]
            x -= convert(d, decimal)
            x *= 10.0
        else:
            break
    return y