# aiobitcoin

![](https://img.shields.io/pypi/v/aiobitcoin.svg?style=flat)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

[![Documentation Status](https://readthedocs.org/projects/aiobitcoin/badge/?version=latest)](http://aiobitcoin.readthedocs.io/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/issues/)
[![HitCount](http://hits.dwyl.com/mkbeh/aiobitcoin.svg)](http://hits.dwyl.com/mkbeh/aiobitcoin)

This is a simple library that provides methods for working 
with Bitcoin daemon JSON-RPC.

`NOTE: this lib works successful with Bitcoin Core 0.17.1`

## Quickstart
### Create gram object and get blockchain info and balance:

```python
import asyncio
from aiobitcoin.grambitcoin import GramBitcoin


async def foo():
    gram = GramBitcoin(url='<your_daemon_url_with_rpcuser_and_rpcwd>')
    info = await gram.get_blockchain_info()
    balance = await gram.get_balance()
    print(info)
    print(balance)

    await gram.close_session()


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(foo())
```

### or use the same with context manager:

```python
import asyncio
from aiobitcoin.grambitcoin import GramBitcoin


async def foo():
    async with GramBitcoin(url='<your_daemon_url_with_rpcuser_and_rpcwd>') as gram:
        info = await gram.get_blockchain_info()
        balance = await gram.get_balance()
        print(info)
        print(balance)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(foo())
```
