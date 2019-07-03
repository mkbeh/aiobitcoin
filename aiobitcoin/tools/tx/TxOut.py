"""
Deal with the part of a Tx that specifies where the Bitcoin goes to.
"""

from ..convention import satoshi_to_mbtc

from ..serialize.bitcoin_streamer import parse_struct, stream_struct

from .pay_to import script_obj_from_script
from .script import tools


class TxOut(object):

    COIN_VALUE_CAST_F = int

    """
    The part of a Tx that specifies where the Bitcoin goes to.
    """

    def __init__(self, coin_value, script):
        assert isinstance(script, bytes)
        self.coin_value = self.COIN_VALUE_CAST_F(coin_value)
        self.script = script

    def stream(self, f):
        stream_struct("QS", f, self.coin_value, self.script)

    @classmethod
    def parse(cls, f):
        return cls(*parse_struct("QS", f))

    def __str__(self):
        return '%s<%s mbtc "%s">' % (
            self.__class__.__name__,
            satoshi_to_mbtc(self.coin_value),
            tools.disassemble(self.script)
        )

    def address(self, netcode=None):
        # attempt to return the destination address, or None on failure
        return script_obj_from_script(self.script).address(netcode=netcode)

    bitcoin_address = address

    def hash160(self):
        # attempt to return the destination hash160, or None on failure
        info = script_obj_from_script(self.script).info()
        return info.get("hash160")
