# -*- coding: utf-8 -*-
from hmac import HMAC
from hashlib import sha512

from . import base58
from .utils import Octets, int_from_octets


# VERSION BYTES =      4 bytes     Base58 encode starts with
MAINNET_PRV = b'\x04\x88\xAD\xE4'  # xprv
TESTNET_PRV = b'\x04\x35\x83\x94'  # tprv
SEGWIT_PRV = b'\x04\xb2\x43\x0c'
PRV = [MAINNET_PRV, TESTNET_PRV, SEGWIT_PRV]


def xmprv_from_seed(seed: Octets, version: Octets) -> bytes:
    """derive the master extended private key from the seed"""

    if isinstance(version, str):  # hex string
        version = bytes.fromhex(version)
    if version not in PRV:
        m = f"invalid private version ({version})"
        raise ValueError(m)

    # serialization data
    xmprv = version                               # version
    xmprv += b'\x00'                              # depth
    xmprv += b'\x00\x00\x00\x00'                  # parent pubkey fingerprint
    xmprv += b'\x00\x00\x00\x00'                  # child index

    # actual extended key (key + chain code) derivation
    if isinstance(seed, str):  # hex string
        seed = bytes.fromhex(seed)
    hd = HMAC(b"Bitcoin seed", seed, sha512).digest()
    mprv = int_from_octets(hd[:32])
    xmprv += hd[32:]                              # chain code
    xmprv += b'\x00' + mprv.to_bytes(32, 'big')   # private key

    return base58.encode_check(xmprv)
