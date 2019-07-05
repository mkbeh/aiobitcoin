# aiobitcoin

![](https://img.shields.io/pypi/v/aiobitcoin.svg?style=flat)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/aiobitcoin/badge/?version=latest)](http://aiobitcoin.readthedocs.io/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/issues/)

This is a library that provides methods for working 
with Bitcoin/forks daemon JSON-RPC.

Also there are tools for working with bip32 hierarchical 
deterministic wallets in this library . These tools were taken 
from three different libraries such as 
[bitcoinlib](https://github.com/1200wd/bitcoinlib), 
[btclib](https://github.com/fametrano/btclib) and
[pycoin](https://github.com/richardkiss/pycoin) ,
because I had problems while importing keys and addresses 
to the Bitcoin Core when working with each of them separately.

[Examples](https://aiobitcoin.readthedocs.io/en/latest/examples.html)

[Documentation](https://aiobitcoin.readthedocs.io/en/latest/)

`NOTE #0: this lib works successful with Bitcoin Core 0.17.1 , 
other wallet versions not tested.`

`NOTE #1: At the moment, not all available methods are 
implemented in the library , only the most common.`

**Donate me if you like it :)**
```bash
Bitshares account -> mkbehforever007
bitcoin -> bc1qqkr72aemz59aawxf74gytrwuw4m9mj20t7e7df
ethereum -> 0xB3e5b643cFB9e2565a3456eC7c7A73491A32e31F
```

## Supports
* **Basic methods for asynchronous work with Bitcoin/forks
JSON-RPC**
* **Mnemonic key generation**
* **BIP32 hierarchical deterministic wallets**

## Installation
```bash
pip3 install aiobitcoin
```

## Quickstart
**Simple usage:**

    import asyncio
    from aiobitcoin.blockchain import Blockchain


    async def foo():
        blockchain = Blockchain(url='http://alice:bob@127.0.0.1:18332')
        difficulty = await blockchain.get_difficulty()
        block_count = await blockchain.get_block_count()
        print(difficulty)
        print(block_count)
        await blockchain.close_session()

    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(foo())

**or use the same with context manager:**

    import asyncio
    from aiobitcoin.blockchain import Blockchain


    async def foo():
        async with Blockchain(url='http://alice:bob@127.0.0.1:18332') as blockchain:
            difficulty = await blockchain.get_difficulty()
            block_count = await blockchain.get_block_count()
            print(difficulty)
            print(block_count)


    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(foo())
    

**Working with bip32**

`All keys can be imported without problems to Bitcoin Core.`

```python
    from aiobitcoin.tools import bip32
    from aiobitcoin.tools.bip32 import MAINNET_PRV, TESTNET_PRV
    from aiobitcoin.tools.key.Key import Key
    from aiobitcoin.mnemonic import Mnemonic

    # -- Generate mnemonic phrase --
    ceed = Mnemonic().generate(encoding=False)

    # ... Output: rebel swear tomorrow burger cave giraffe ...

    # -- Generate master keys from ceed for BTC mainnet and testnet --
    testnet_mxpriv = bip32.xmprv_from_seed(ceed, TESTNET_PRV)
    # ... Output: tprv8ZgxMBicQKsPe6tqMpq6qyzFoFSr3cgh...

    mainnet_mxpriv = bip32.xmprv_from_seed(ceed, MAINNET_PRV)
    # ... Output: xprv9s21ZrQH143K4Q9MazKYy5Kuck31yFeT...

    # -- Generate master public keys from master private key --
    testnet_mxpub = bip32.xpub_from_xprv(testnet_mxpriv)
    mainnet_mxpub = bip32.xpub_from_xprv(mainnet_mxpriv)

    # ... Output: tpubD6NzVbkrYhZ4X5ghC8mzzsGuMQCxEmnh5Y...
    # ... Output: xpub661MyMwAqRbcFHVqjwnunwwY2H7JFPHdXv...

    # -- Transform master private key to WIF format and getting address of master key --
    key = Key.from_text(mainnet_mxpriv)

    wif = key.wif()
    # ... Output: L4PEssMfRgHvmpyEGxHJkFVcNWeQvZiySNMAa...

    addr = key.address()
    # ... Output: 1BGLari4SCxGXoJib27C8pAL6Ef3pFqswD

    # -- Create sub key by custom derive path --
    subkey = key.subkey_for_path('1/0/{}'.format(11))

    addr = subkey.address(use_uncompressed=False)
    wif = subkey.wif()
```

## Roadmap
* Add all available methods to work with Bitcoin/forks JSON-RPC
* Rewrite to async `Key` tool
* Add DASH, LTC supporting
