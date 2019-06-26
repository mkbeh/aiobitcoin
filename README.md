# aiobitcoin

![](https://img.shields.io/pypi/v/aiobitcoin.svg?style=flat)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/aiobitcoin/badge/?version=latest)](http://aiobitcoin.readthedocs.io/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/issues/)

This is a simple library that provides methods for working 
with Bitcoin/forks daemon JSON-RPC.

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
