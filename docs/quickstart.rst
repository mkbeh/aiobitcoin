Quickstart
----------

**Create `Blockchain` object and get some info:**
::

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

::

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
