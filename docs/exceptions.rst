Exceptions
----------

**class aiobitcoin.bitcoinerrors.BitcoinErrors()**
    Bases: Exception

    This class is the base for all subsequent classes.

* **class aiobitcoin.bitcoinerrors.NoConnectionToTheDaemon()**
    Bases: aiobitcoin.bitcoinerrors.BitcoinErrors

    No connection to the Bitcoin daemon.

* **class aiobitcoin.bitcoinerrors.InvalidPrivateKeyEncoding()**
    Bases: aiobitcoin.bitcoinerrors.BitcoinErrors

    The invalid private key encoding (not WIF format).

* **class aiobitcoin.bitcoinerrors.PrivateKeyForThisAddressAlreadyInWallet()**
    Bases: aiobitcoin.bitcoinerrors.BitcoinErrors

    The private key for current Bitcoin address is already in wallet.

* **class aiobitcoin.bitcoinerrors.InvalidAddress()**
    Bases: aiobitcoin.bitcoinerrors.BitcoinErrors

    The invalid Bitcoin address.

* **class aiobitcoin.bitcoinerrors.InvalidAddress()**
    Bases: aiobitcoin.bitcoinerrors.BitcoinErrors

    The invalid Bitcoin address.
