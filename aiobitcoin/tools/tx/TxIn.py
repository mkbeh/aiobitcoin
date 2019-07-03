from .. import encoding

from ..serialize import b2h, b2h_rev, h2b
from ..serialize.bitcoin_streamer import parse_struct, stream_struct

from .script.tools import disassemble, opcode_list
from .script.vm import verify_script

ZERO = b'\0' * 32


class TxIn(object):
    """
    The part of a Tx that specifies where the Bitcoin comes from.
    """

    def __init__(self, previous_hash, previous_index, script=b'', sequence=4294967295):
        self.previous_hash = previous_hash
        self.previous_index = previous_index
        self.script = script
        self.sequence = sequence
        self.witness = ()

    @classmethod
    def coinbase_tx_in(cls, script):
        tx = cls(previous_hash=ZERO, previous_index=4294967295, script=script)
        return tx

    def stream(self, f, blank_solutions=False):
        script = b'' if blank_solutions else self.script
        stream_struct("#LSL", f, self.previous_hash, self.previous_index, script, self.sequence)

    @classmethod
    def parse(cls, f):
        return cls(*parse_struct("#LSL", f))

    def is_coinbase(self):
        return self.previous_hash == ZERO

    def public_key_sec(self):
        """Return the public key as sec, or None in case of failure."""
        if self.is_coinbase():
            return None
        opcodes = opcode_list(self.script)
        if len(opcodes) == 2 and opcodes[0].startswith("[30"):
            # the second opcode is probably the public key as sec
            sec = h2b(opcodes[1][1:-1])
            return sec
        return None

    def address(self, address_prefix=b'\0'):
        if self.is_coinbase():
            return "(coinbase)"
        # attempt to return the source address
        sec = self.public_key_sec()
        if sec:
            bitcoin_address = encoding.hash160_sec_to_bitcoin_address(
                encoding.hash160(sec), address_prefix=address_prefix)
            return bitcoin_address
        return "(unknown)"

    bitcoin_address = address

    def verify(self, tx_out_script, signature_for_hash_type_f, lock_time, expected_hash_type=None,
               traceback_f=None, flags=None, tx_version=None):
        """
        Return True or False depending upon whether this TxIn verifies.

        tx_out_script: the script of the TxOut that corresponds to this input
        signature_hash: the hash of the partial transaction
        """
        if self.sequence == 0xffffffff:
            lock_time = None
        return verify_script(self.script, tx_out_script, signature_for_hash_type_f, lock_time=lock_time,
                             flags=flags, expected_hash_type=expected_hash_type, traceback_f=traceback_f,
                             witness=self.witness, tx_sequence=self.sequence, tx_version=tx_version)

    def __str__(self):
        if self.is_coinbase():
            return 'TxIn<COINBASE: %s>' % b2h(self.script)
        return 'TxIn<%s[%d] "%s">' % (
            b2h_rev(self.previous_hash), self.previous_index, disassemble(self.script))
