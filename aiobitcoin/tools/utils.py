# -*- coding: utf-8 -*-

# Copyright (C) 2017-2019 The btclib developers 2019 mkbeh
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""Assorted conversion utilities.

Most conversions from SEC 1 v.2 2.3 are included.

https://www.secg.org/sec1-v2.pdf
"""

from typing import Union
from hashlib import sha256
from .curve import Curve, Point


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


def octets_from_point(ec: Curve, Q: Point, compressed: bool) -> bytes:
    """Return a point as compressed/uncompressed octet sequence.

    Return a point as compressed (0x02, 0x03) or uncompressed (0x04)
    octet sequence, according to SEC 1 v.2, section 2.3.3.
    """

    # check that Q is a point and that is on curve
    ec.require_on_curve(Q)

    if Q[1] == 0:  # infinity point in affine coordinates
        return b'\x00'

    bPx = Q[0].to_bytes(ec.psize, byteorder='big')
    if compressed:
        return (b'\x03' if (Q[1] & 1) else b'\x02') + bPx

    return b'\x04' + bPx + Q[1].to_bytes(ec.psize, byteorder='big')
