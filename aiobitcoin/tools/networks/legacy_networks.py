# -*- coding: utf-8 -*-
# this file is deprecated and will soon be folded into all.py
from collections import namedtuple

from aiobitcoin.tools.serialize import h2b

NetworkValues = namedtuple('NetworkValues',
                           ('network_name', 'subnet_name', 'code', 'wif', 'address',
                            'pay_to_script', 'prv32', 'pub32'))

NETWORKS = (
    # DOGE Dogecoin mainnet : dogv/dogp
    NetworkValues(
        "Dogecoin", "mainnet", "DOGE", b'\x9e', b'\x1e', b'\x16', h2b("02FD3955"), h2b("02FD3929")),
    # DOGE Dogecoin testnet : tgpv/tgub
    NetworkValues(
        "Dogecoin", "testnet", "XDT", b'\xf1', b'\x71', b'\xc4', h2b("0432a9a8"), h2b("0432a243")),

    # DRK Dash mainnet : drkv/drkp
    NetworkValues(
        "Dash", "mainnet", "DASH", b'\xcc', b'\x4c', b'\x10', h2b("02fe52f8"), h2b("02fe52cc")),

    # DRK Dash testnet : DRKV/DRKP
    NetworkValues(
        "Dash", "testnet", "tDASH", b'\xef', b'\x8c', b'\x13', h2b("3a8061a0"), h2b("3a805837")),

    # ZEC Zcash mainnet : xprv/xpub
    NetworkValues("Zcash", "mainnet", "ZEC", b'\x80', b'\x1C\xB8',
                  b'\x1C\xBD', h2b("0488ADE4"), h2b("0488B21E")),

    # BTCD BitcoinDark mainnet : xprv/xpub
    NetworkValues("BitcoinDark", "mainnet", "BTCD", b'\x44', b'\x3C', b'\55', h2b('0488ADE4'), h2b('0488B21E')),
)
