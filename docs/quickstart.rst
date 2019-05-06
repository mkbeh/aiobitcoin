Quickstart
----------

Create gram object and get blockchain info:
"""""""""""""""""""""""""""""""""""""""""""""""
::

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

or use the same with context manager:
"""""""""""""""""""""""""""""""""""""""""
::

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
