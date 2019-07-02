# -*- coding: utf-8 -*-

"""Elliptic curves.

* SEC 2 v.2 curves
  http://www.secg.org/sec2-v2.pdf
* SEC 2 v.1 curves, removed from SEC 2 v.2 as insecure ones
  http://www.secg.org/SEC2-Ver-1.0.pdf
* Federal Information Processing Standards Publication 186-4
  (NIST) curves
  https://oag.ca.gov/sites/all/files/agweb/pdfs/erds1/fips_pub_07_2013.pdf
* Brainpool standard curves
  https://tools.ietf.org/html/rfc5639
* test curves with very low cardinality

"""

# scroll down at the end of the file for 'relevant' code

from .curve import Curve


# bitcoin curve
__p = 2**256 - 2**32 - 977
__a = 0
__b = 7
__Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
__Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
__n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
__h = 1
secp256k1 = Curve(__p, __a, __b, (__Gx, __Gy), __n, __h, 128, True)
