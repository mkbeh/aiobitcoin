# -*- coding: utf-8 -*-

#    BitcoinLib - Python Cryptocurrency Library
#    ENCODING - Methods for encoding and conversion
#    © 2016 - 2018 October - 1200 Web Development <http://1200wd.com/>
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

import logging
import binascii
import copy
import math
import numbers
import sys
import unicodedata

from aiobitcoin.config import config


_logger = logging.getLogger(__name__)


class EncodingError(Exception):
    """ Log and raise encoding errors """
    def __init__(self, msg=''):
        self.msg = msg
        _logger.error(msg)

    def __str__(self):
        return self.msg


code_strings = {
    2: b'01',
    3: b' ,.',
    10: b'0123456789',
    16: b'0123456789abcdef',
    32: b'abcdefghijklmnopqrstuvwxyz234567',
    58: b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
    256: b''.join([bytes(bytearray((x,))) for x in range(256)]),
    'bech32': b'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
}


def to_hexstring(string):
    """
    Convert Bytes or ByteArray to hexadecimal string

    :param string: Variable to convert to hex string
    :type string: bytes, bytearray, str

    :return: hexstring
    """
    string = normalize_var(string)

    if isinstance(string, (str, bytes)):
        try:
            binascii.unhexlify(string)
            if config.PY3:
                return str(string, 'ISO-8859-1')
            else:
                return string
        except (TypeError, binascii.Error):
            pass

    s = binascii.hexlify(string)

    if config.PY3:
        return str(s, 'ISO-8859-1')
    else:
        return s


def _get_code_string(base):
    if base in code_strings:
        return code_strings[base]
    else:
        return list(range(0, base))


def change_base(chars, base_from, base_to, min_length=0, output_even=None, output_as_list=None):
    """
    Convert input chars from one base to another.

    From and to base can be any base. If base is not found a array of index numbers will be returned

    Examples:
    > change_base('FF', 16, 10) will return 256
    > change_base(100, 16, 2048) will return [100]

    :param chars: Input string
    :type chars: any
    :param base_from: Base number or name from input
    :type base_from: int, str
    :param base_to: Base number or name for output
    :type base_to: int, str
    :param min_length: Minimal output length. Required for decimal, advised for all output to avoid leading zeros
    conversion problems.
    :type min_length: int
    :param output_even: Specify if output must contain a even number of characters. Sometimes handy for hex conversions.
    :type output_even: bool
    :param output_as_list: Always output as list instead of string.
    :type output_as_list: bool

    :return str, list: Base converted input as string or list.
    """
    if base_from == 10 and not min_length:
        raise EncodingError("For a decimal input a minimum output length is required!")

    code_str = _get_code_string(base_to)

    if not isinstance(base_to, int):
        base_to = len(code_str)
    elif int(base_to) not in code_strings:
        output_as_list = True

    code_str_from = _get_code_string(base_from)
    if not isinstance(base_from, int):
        base_from = len(code_str)
    if not isinstance(code_str_from, (bytes, list)):
        raise EncodingError("Code strings must be a list or defined as bytes")

    output = []
    input_dec = 0
    addzeros = 0
    inp = normalize_var(chars, base_from)

    # Use binascii and int for standard conversions to speedup things
    if not min_length:
        if base_from == 256 and base_to == 16:
            return to_hexstring(inp)
        elif base_from == 16 and base_to == 256:
            return binascii.unhexlify(inp)
    if base_from == 16 and base_to == 10:
        return int(inp, 16)

    if output_even is None and base_to == 16:
        output_even = True

    if isinstance(inp, numbers.Number):
        input_dec = inp
    elif isinstance(inp, (str, list, bytes, bytearray)):
        factor = 1
        while len(inp):
            if isinstance(inp, list):
                item = inp.pop()
            else:
                item = inp[-1:]
                inp = inp[:-1]
            try:
                pos = code_str_from.index(item)
            except ValueError:
                try:
                    pos = code_str_from.index(item.lower())
                except ValueError:
                    return False
            input_dec += pos * factor

            # Add leading zero if there are leading zero's in input
            if not pos * factor:
                if not config.PY3:
                    firstchar = code_str_from[0]
                else:
                    firstchar = chr(code_str_from[0]).encode('utf-8')
                if isinstance(inp, list):
                    if not len([x for x in inp if x != firstchar]):
                        addzeros += 1
                elif not len(inp.strip(firstchar)):
                    addzeros += 1
            factor *= base_from
    else:
        raise EncodingError("Unknown input format %s" % inp)

    # Convert decimal to output base
    while input_dec != 0:
        input_dec, remainder = divmod(input_dec, base_to)
        output = [code_str[remainder]] + output

    if base_to != 10:
        pos_fact = math.log(base_to, base_from)
        expected_length = len(str(chars)) / pos_fact
        zeros = int(addzeros / pos_fact)
        if addzeros == 1:
            zeros = 1

        for _ in range(zeros):
            if base_to != 10 and not expected_length == len(output):
                output = [code_str[0]] + output

        # Add zero's to make even number of digits on Hex output (or if specified)
        if output_even and len(output) % 2:
            output = [code_str[0]] + output

        # Add leading zero's
        while len(output) < min_length:
            output = [code_str[0]] + output

    if not output_as_list and isinstance(output, list):
        if len(output) == 0:
            output = 0
        elif isinstance(output[0], bytes):
            output = b''.join(output)
        elif isinstance(output[0], int):
            co = ''
            for c in output:
                co += chr(c)
            output = co
        else:
            output = ''.join(output)
    if base_to == 10:
        return int(0) or (output != '' and int(output))
    if config.PY3 and base_to == 256 and not output_as_list:
        return output.encode('ISO-8859-1')
    else:
        return output


def normalize_var(var, base=256):
    """
    For Python 2 convert variable to string
    For Python 3 convert to bytes
    Convert decimals to integer type
    :param var: input variable in any format
    :type var: str, byte, bytearray, unicode
    :param base: specify variable format, i.e. 10 for decimal, 16 for hex
    :type base: int
    :return: Normalized var in string for Python 2, bytes for Python 3, decimal for base10
    """
    try:
        if config.PY3 and isinstance(var, str):
            var = var.encode('ISO-8859-1')
    except ValueError:
        try:
            var = var.encode('utf-8')
        except ValueError:
            raise EncodingError("Unknown character '%s' in input format" % var)

    if base == 10:
        return int(var)
    elif isinstance(var, list):
        return copy.deepcopy(var)
    else:
        return var


def to_bytes(string, unhexlify=True):
    """
    Convert String, Unicode or ByteArray to Bytes
    :param string: String to convert
    :type string: str, unicode, bytes, bytearray
    :param unhexlify: Try to unhexlify hexstring
    :type unhexlify: bool
    :return: Bytes var
    """
    s = normalize_var(string)

    if unhexlify:
        try:
            s = binascii.unhexlify(s)
            return s
        except (TypeError, binascii.Error):
            pass
    return s


def normalize_string(string):
    """
    Normalize a string to the default NFKD unicode format
    See https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization

    :param string: string value
    :type string: bytes, bytearray, str

    :return: string
    """
    if isinstance(string, str if sys.version < '3' else bytes):
        utxt = string.decode('utf8')
    elif isinstance(string, config.TYPE_TEXT):
        utxt = string
    else:
        raise TypeError("String value expected")

    return unicodedata.normalize('NFKD', utxt)
