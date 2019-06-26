Examples
--------

**Basic usage:**
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

**Basic usage with context manager:**
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

**Another way to usage:**
::

    import asyncio
    from aiobitcoin.grambitcoin import GramBitcoin
    from aiobitcoin.blockchain import Blockchain


    async def baz():
        # Create gram objects.
        gram = GramBitcoin(session_required=True)

        # Get some single info.
        blockchain = Blockchain(url='http://alice:bob@127.0.0.1:18332', gram=gram)
        result = await blockchain.get_block_count()
        print(result)

        # Close sessions.
        await gram.close_session()

**How to call methods asynchronously:**
::

    async def multi(obj):
        result = await obj.get_block_count()
        print(result)


    async def baz():
        # Create Network objects with sessions.
        objs = [Blockchain(url='http://alice:bob@127.0.0.1:18332') for _ in range(100)]

        # Call methods asynchronously
        await asyncio.gather(
            *(multi(obj) for obj in objs)
        )

        # Close sessions
        [await obj.close_session() for obj in objs]

**Another example of how to call methods asynchronously:**

This method is less productive than the previous
one by about 25%, but more elegant :)
::

    import asyncio
    from aiobitcoin.blockchain import Blockchain


    async def multi(obj):
        result = await obj.get_block_count()
        print(result)


    async def baz():
        async with Blockchain(url='http://alice:bob@127.0.0.1:18332') as blockchain:
            await asyncio.gather(
                *(multi(blockchain) for _ in range(100))
            )

**Another way to get some info:**
::

    import asyncio
    from aiobitcoin.grambitcoin import GramBitcoin
    from aiobitcoin.blockchain import Blockchain


    async def baz():
        # Create gram object with `session_required=True`.
        gram = GramBitcoin(url='http://alice:bob@127.0.0.1:18332', session_required=True)

        # Pass the `gram` object to the `Blockchain` class constructor.
        blockchain = Blockchain(gram=gram)

        # Get info.
        result = await blockchain.get_block_count()
        print(result)

        # Close session.
        await gram.close_session()

**How convenient to get various information using
the `GramBitcoin`:**
::

    import asyncio
    from aiobitcoin.grambitcoin import GramBitcoin
    from aiobitcoin.blockchain import Blockchain
    from aiobitcoin.network import Network


    async def baz():
        # Create gram object with `session_required=True`.
        gram = GramBitcoin(url='http://alice:bob@127.0.0.1:18332', session_required=True)

        # Pass the `gram` object to the `Blockchain` class constructor.
        blockchain = Blockchain(gram=gram)
        network = Network(gram=gram)

        # Get info.
        result = await blockchain.get_block_count()
        print(result)

        # Get another info.
        another_result = await network.get_peer_info(to_list=True)
        print(another_result)

        # Close session.
        await gram.close_session()


**Get single data and then get multi data
asynchronously using `GramBitcoin`**
::

    import asyncio
    from aiobitcoin.grambitcoin import GramBitcoin
    from aiobitcoin.blockchain import Blockchain
    from aiobitcoin.network import Network
    from aiobitcoin.bitcoinerrors import NoConnectionToTheDaemon


    async def multi(obj):
        result = await obj.get_peer_info()
        print(result)


    async def baz():
        # Create grams objects.
        grams = [GramBitcoin(url='http://alice:bob@127.0.0.1:18332', session_required=True)
                 for _ in range(10)]

        # Try to get some single info.
        try:
            blockchain = Blockchain(gram=grams[0])
            result = await blockchain.get_block_count()
            print(result)
        except NoConnectionToTheDaemon:
            pass

        # Get another info asynchronously.
        objs = [Network(gram=gram) for gram in grams]
        await asyncio.gather(
            *(multi(obj) for obj in objs)
        )

        # Close sessions.
        [await gram.close_session() for gram in grams]
