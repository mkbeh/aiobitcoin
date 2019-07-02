# -*- coding: utf-8 -*-

"""Assorted conversion utilities.

Most conversions from SEC 1 v.2 2.3 are included.

https://www.secg.org/sec1-v2.pdf
"""

from typing import Union
from hashlib import sha256
# from .curve import Curve, Point


# bytes or hex string
Octets = Union[str, bytes]


def int_from_octets(o: Octets) -> int:
    """Return an integer from an octet sequence (bytes or hex string).

    Return an integer from an octet sequence (bytes or hex string)
    according to SEC 1 v.2, section 2.3.8.
    """
    if isinstance(o, str):  # hex string
        o = bytes.fromhex(o)
    return int.from_bytes(o, 'big')


def double_sha256(o: Octets) -> bytes:
    """Return SHA256(SHA256()) of an octet sequence."""

    if isinstance(o, str):
        o = bytes.fromhex(o)

    return sha256(sha256(o).digest()).digest()


# def point_from_octets(ec: Curve, o: Octets) -> Point:
#     """Return a tuple (Px, Py) that belongs to the curve.
#
#     Return a tuple (Px, Py) that belongs to the curve according to
#     SEC 1 v.2, section 2.3.4.
#     """
#
#     if isinstance(o, str):
#         o = bytes.fromhex(o)
#
#     bsize = len(o) # bytes
#     if bsize == 1 and o[0] == 0x00:     # infinity point
#         return Point()
#
#     if bsize == ec.psize+1:             # compressed point
#         if o[0] not in (0x02, 0x03):
#             m = f"{ec.psize+1} bytes, but not a compressed point"
#             raise ValueError(m)
#         Px = int.from_bytes(o[1:], 'big')
#         try:
#             Py = ec.y_odd(Px, o[0] % 2)  # also check Px validity
#             return Point(Px, Py)
#         except:
#             raise ValueError("point not on curve")
#     else:                               # uncompressed point
#         if bsize != 2*ec.psize+1:
#             m = f"wrong byte-size ({bsize}) for a point: it "
#             m += f"should have be {ec.psize+1} or {2*ec.psize+1}"
#             raise ValueError(m)
#         if o[0] != 0x04:
#             raise ValueError("not an uncompressed point")
#         Px = int.from_bytes(o[1:ec.psize+1], 'big')
#         P = Point(Px, int.from_bytes(o[ec.psize+1:], 'big'))
#         if ec.is_on_curve(P):
#             return P
#         else:
#             raise ValueError("point not on curve")
