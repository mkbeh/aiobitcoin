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

**Working with bip32:**
::

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


