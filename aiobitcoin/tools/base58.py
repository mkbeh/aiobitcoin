# -*- coding: utf-8 -*-
from typing import Union, Optional

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


def decode_to_int(v: Union[str, bytes]) -> int:
    """Decode Base58 encoded bytes or string as integer."""

    v = _str_to_bytes(v)

    i = 0
    for char in v:
        i *= __base
        i += __digits.index(char)
    return i


def decode(v: Union[str, bytes],
           output_size: Optional[int] = None) -> bytes:
    """Decode Base58 encoded bytes or string.

    Decode Base58 encoded bytes or string,
    optionally ensuring required output size.
    """

    v = _str_to_bytes(v)

    # preserve leading-0s
    # base58 leading-1s become leading-0s
    nPad = len(v)
    v = v.lstrip(__digits[0:1])
    vlen = len(v)
    nPad -= vlen
    result = b'\0' * nPad

    if vlen:
        i = decode_to_int(v)
        nbytes = (i.bit_length() + 7) // 8
        result = result + i.to_bytes(nbytes, 'big')

    if output_size is not None and len(result) != output_size:
        m = "Invalid decoded size: "
        m += f"{len(result)} bytes instead of {output_size}"
        raise ValueError(m)

    return result


def decode_check(v: Union[str, bytes],
                 output_size: Optional[int] = None) -> bytes:
    """Decode Base58 encoded bytes or string, verifying checksum.

    Decode Base58 encoded bytes or string, verifying checksum and
    optionally ensuring required output size.
    """

    if output_size is not None:
        output_size += 4

    result = decode(v, output_size)
    result, checksum = result[:-4], result[-4:]

    digest = double_sha256(result)
    if checksum != digest[:4]:
        m = f"Invalid checksum: '{checksum}' instead of '{digest[:4]}'"
        raise ValueError(m)

    return result