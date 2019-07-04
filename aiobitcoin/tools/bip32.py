# -*- coding: utf-8 -*-

# Copyright (C) 2017-2019 The btclib developers 2019 mkbeh
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""BIP32 Hierarchical Deterministic Wallet functions.

A deterministic wallet is a hash-chain of private/public key pairs that
derives from a single root, which is the only element requiring backup.
Moreover, there are schemes where public keys can be calculated without
accessing private keys.

A hierarchical deterministic wallet is a tree of multiple hash-chains,
derived from a single root, allowing for selective sharing of keypair
chains.

Here, the HD wallet is implemented according to BIP32 bitcoin standard
https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki.
"""

from hmac import HMAC
from hashlib import sha512

from . import base58
from .curve import mult
from .curves import secp256k1 as ec
from .utils import Octets, int_from_octets, octets_from_point


# VERSION BYTES =      4 bytes     Base58 encode starts with
MAINNET_PRV = b'\x04\x88\xAD\xE4'  # xprv
TESTNET_PRV = b'\x04\x35\x83\x94'  # tprv
SEGWIT_PRV = b'\x04\xb2\x43\x0c'
PRV = (MAINNET_PRV, TESTNET_PRV, SEGWIT_PRV)

MAINNET_PUB = b'\x04\x88\xB2\x1E'  # xpub
TESTNET_PUB = b'\x04\x35\x87\xCF'  # tpub
SEGWIT_PUB = b'\x04\xb2\x47\x46'
PUB = (MAINNET_PUB, TESTNET_PUB, SEGWIT_PUB)

MAINNET_ADDRESS = b'\x00'          # 1
TESTNET_ADDRESS = b'\x6F'          # m or n
ADDRESS = (MAINNET_ADDRESS, TESTNET_ADDRESS)

# [  : 4] version
# [ 4: 5] depth
# [ 5: 9] parent pubkey fingerprint
# [ 9:13] child index
# [13:45] chain code
# [45:78] key (private/public)


def xmprv_from_seed(seed: Octets, version: Octets, decode: bool = True) -> bytes:
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
    xmprv = base58.encode_check(xmprv)

    return xmprv.decode('utf-8') if decode else xmprv


def xpub_from_xprv(xprv: Octets, decode: bool = True) -> bytes:
    """Neutered Derivation (ND)

    Computation of the extended public key corresponding to an extended
    private key (“neutered” as it removes the ability to sign transactions)
    """

    xprv = base58.decode_check(xprv, 78)
    if xprv[45] != 0:
        raise ValueError("extended key is not a private one")

    i = PRV.index(xprv[:4])

    # serialization data
    xpub = PUB[i]                              # version
    # unchanged serialization data
    xpub += xprv[4: 5]                         # depth
    xpub += xprv[5: 9]                         # parent pubkey fingerprint
    xpub += xprv[9:13]                         # child index
    xpub += xprv[13:45]                        # chain code

    p = int_from_octets(xprv[46:])
    P = mult(ec, p)
    xpub += octets_from_point(ec, P, True)          # public key
    xpub = base58.encode_check(xpub)

    return xpub.decode('utf-8') if decode else xpub
