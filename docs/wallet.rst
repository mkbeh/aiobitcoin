Wallet
------

* **get_balance()**
    *Returns the total available balance.*

    **Parameters:** absent

    **Returns:** Total balance

    **Return type:** float

* **import_address(addr, rescan=False)**
    *Adds an address or script (in hex) that can be watched
    as if it were in your wallet but cannot be used to spend.*

    **Parameters:**

    * **addr** (str) - Bitcoin address
    * **rescan** (bool) - Activates rescanning blockchain after importing. By default is *False*.

    **Returns:**       True or False.

    **Return type:**    boolean

    **Raises:** aiobitcoin.bitcoinerrors.PrivateKeyForThisAddressAlreadyInWallet -
    if WIF for this address was already imported into the wallet

* **import_priv_key(wif)**
    *Adds a private key (as returned by dumpprivkey) to
    your wallet.*

    **Parameters:**

    * **wif** (str) - Bitcoin private key in WIF format

    **Returns:**       None

    **Return type:**    NoneType

    **Raises** aiobitcoin.bitcoinerrors.InvalidPrivateKeyEncoding -
    if private key not in WIF format.

* **list_transactions(count=100, include_watchonly=True, to_list=True)**
    *Returns up to 'count' most recent transactions.*

    **Parameters:**

    * **count** (int) - The number of transactions to return
    * **include_watchonly** (bool) - Include transactions to watch-only addresses
    * **to_list** (bool) - Will return list or genexpr

    **Returns:** List or genexpr of txs.

    **Return type:** list or genexpr

* **rescan_blockchain(days_ago, full_rescan=False)**
    *Rescan the local blockchain for wallet related transactions.*

    **Parameters:**

    * **days_ago** (int) - How many days the blockchain rescanning will pass
    * **full_rescan** (bool) - Blockchain rescanning will start from block 1

    **Returns:** True or False

    **Return type:**    boolean

* **send_to_address(addr, amount)**
    *Send an amount to a given address.*

    **Parameters:**

    * **addr** (str) - Bitcoin address to send
    * **amount** (int or float) - amount to send

    **Returns:** Hash of tx

    **Return type:** str

    **Raises** aiobitcoin.bitcoinerrors.InvalidAddress -
    if address to send is incorrect.
