# -*- coding: utf-8 -*-


class BitcoinErrors(Exception):
    def __init__(self, error_msg=''):
        Exception.__init__(self, f'{error_msg}')


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

