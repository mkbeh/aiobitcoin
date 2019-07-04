# -*- coding: utf-8 -*-

#    BitcoinLib - Python Cryptocurrency Library
#    MNEMONIC class for BIP0039 Mnemonic Key management
#    © 2016 - 2018 June - 1200 Web Development <http://1200wd.com/>
#    © 2019 July - mkbeh
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import hashlib

from aiobitcoin.encoding import change_base, normalize_string, to_bytes
from aiobitcoin.config.config import *
from aiobitcoin.config.secp256k1 import *


class Mnemonic:
    def __init__(self, language=DEFAULT_LANGUAGE):
        """
        Init Mnemonic class and read wordlist of specified language

        :param language: use specific wordlist, i.e. chinese, dutch (in development), english, french, italian,
        japanese or spanish. Leave empty for default 'english'
        :type language: str

        """
        self._wordlist = []

        with open(os.path.join(WORDLIST_DIR, '%s.txt' % language)) as f:
            self._wordlist = [w.strip() for w in f.readlines()]

    @staticmethod
    def checksum(data):
        """
        Calculates checksum for given data key

        :param data: key string
        :type data: bytes, hexstring

        :return str: Checksum of key in bits
        """
        data = to_bytes(data)

        if len(data) % 4 > 0:
            raise ValueError('Data length in bits should be divisible by 32, but it is not (%d bytes = %d bits).' %
                             (len(data), len(data) * 8))

        tx_hash = hashlib.sha256(data).digest()
        return change_base(tx_hash, 256, 2, 256)[:len(data) * 8 // 32]

    def to_mnemonic(self, data, add_checksum=True, check_on_curve=True):
        """
        Convert key data entropy to Mnemonic sentence

        :param data: Key data entropy
        :type data: bytes, hexstring
        :param add_checksum: Included a checksum? Default is True
        :type add_checksum: bool
        :param check_on_curve: Check if data integer value is on secp256k1 curve. Should be enabled when not
        testing and working with crypto
        :type check_on_curve: bool

        :return str: Mnemonic passphrase consisting of a space seperated list of words
        """
        data = to_bytes(data)
        data_int = change_base(data, 256, 10)

        if check_on_curve and not 0 < data_int < secp256k1_n:
            raise ValueError("Integer value of data should be in secp256k1 domain between 1 and secp256k1_n-1")

        if add_checksum:
            binresult = change_base(data_int, 10, 2, len(data) * 8) + self.checksum(data)
            wi = change_base(binresult, 2, 2048)
        else:
            wi = change_base(data_int, 10, 2048)

        return normalize_string(' '.join([self._wordlist[i] for i in wi]))

    def generate(self, strength=128, add_checksum=True, encoding=True):
        """
        Generate a random Mnemonic key

        Uses cryptographically secure os.urandom() function to generate data. Then creates a Mnemonic sentence with
        the 'to_mnemonic' method.
        :param strength: Key strength in number of bits, default is 128 bits. It advised to specify 128 bits or more,
        i.e.: 128, 256, 512 or 1024
        :type strength: int
        :param add_checksum: Included a checksum? Default is True
        :type add_checksum: bool
        :param encoding
        :type encoding: bool

        :return str: Mnemonic passphrase consisting of a space seperated list of words
        """
        if strength % 32 > 0:
            raise ValueError("Strenght should be divisible by 32")

        data = os.urandom(strength // 8)
        ceed = self.to_mnemonic(data, add_checksum=add_checksum)

        return ceed.encode('utf-8') if encoding else ceed
