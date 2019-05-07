# -*- coding: utf-8 -*-


class BitcoinErrors(Exception):
    pass


class InvalidPrivateKeyEncoding(BitcoinErrors):
    pass


class PrivateKeyForThisAddressAlreadyInWallet(BitcoinErrors):
    pass


class InvalidAddress(BitcoinErrors):
    pass


class InvalidIpOrSubnet(BitcoinErrors):
    pass


class NoConnectionToTheDaemon(BitcoinErrors):
    pass

