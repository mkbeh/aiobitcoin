# -*- coding: utf-8 -*-
from typing import Union

from .utils import double_sha256


# used digits
__digits = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__base = len(__digits)


def _str_to_bytes(v: Union[str, bytes]) -> bytes:
    """Encode string to bytes, stripping leading/trailing white spaces"""

    if isinstance(v, str):
        v = v.strip()
        v = v.encode()

    return v


def encode_from_int(i: int) -> bytes:
    """Encode an integer using Base58."""

    if i == 0:
        return __digits[0:1]

    result = b""
    while i:
        i, idx = divmod(i, __base)
        result = __digits[idx:idx+1] + result

    return result


def encode(v: Union[str, bytes]) -> bytes:
    """Encode bytes or string using Base58."""

    v = _str_to_bytes(v)

    # preserve leading-0s
    # leading-0s become base58 leading-1s
    nPad = len(v)
    v = v.lstrip(b'\0')
    vlen = len(v)
    nPad -= vlen
    result = __digits[0:1] * nPad

    if vlen:
        i = int.from_bytes(v, 'big')
        result += encode_from_int(i)

    return result


def encode_check(v: Union[str, bytes]) -> bytes:
    """Encode bytes or string using checksummed Base58."""

    v = _str_to_bytes(v)

    digest = double_sha256(v)
    return encode(v + digest[:4])
