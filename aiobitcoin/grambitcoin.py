# -*- coding: utf-8 -*-
import logging
import aiohttp
import ujson

from asyncio.futures import TimeoutError
from aiohttp.client_exceptions import ContentTypeError, InvalidURL, ServerDisconnectedError

from . import bitcointools
from .bitcoinerrors import InvalidPrivateKeyEncoding, PrivateKeyForThisAddressAlreadyInWallet, InvalidAddress, \
    NoConnectionToTheDaemon


class GramBitcoin:
    def __init__(self, url):
        self._url = url
        self._session = aiohttp.ClientSession(read_timeout=20, json_serialize=ujson.dumps)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    async def _call_method(self, method, *args):
        headers = {
            'Content-Type': 'application/json',
        }
        data = {'jsonrpc': '1.0', 'method': f'{method}', 'params': args}

        try:
            response = await self._session.post(url=self._url, headers=headers, data=ujson.dumps(data))

            return await response.json()
        except (ContentTypeError, InvalidURL, ServerDisconnectedError, TimeoutError):
            await self.close_session()
            logging.critical('No connection to the daemon.')
            raise NoConnectionToTheDaemon

    async def close_session(self):
        await self._session.close()

    async def get_blockchain_info(self) -> dict:
        """
        Provides information about the current state of the block chain.
        :return: full blockchain information.
        """
        return (
            await self._call_method('getblockchaininfo')
        )['result']

    async def import_address(self, addr: str, rescan: bool = False) -> None or PrivateKeyForThisAddressAlreadyInWallet:
        """
        Adds an address or script (in hex) that can be watched as if it were in your wallet but cannot be used to spend.
        :param addr: bitcoin address
        :param rescan: activate rescanning blockchain after importing
        :return: boolean value
        """
        error = (
            await self._call_method('importaddress', addr, '', rescan)
        )['error']

        if error is not None and error['code'] == -4:
            raise PrivateKeyForThisAddressAlreadyInWallet

    async def import_priv_key(self, wif: str) -> None or InvalidPrivateKeyEncoding:
        """
        Adds a private key (as returned by dumpprivkey) to your wallet.
        :param wif: bitcoin private key
        :return: boolean value
        """
        error = (
            await self._call_method('importprivkey', wif, "", False)
        )['error']

        if error is not None and error['code'] == -5:
            raise InvalidPrivateKeyEncoding

    async def validate_address(self, addr: str) -> bool:
        """
        Return information about the given bitcoin address.
        :param addr: bitcoin address
        :return: boolean value
        """
        return (
            await self._call_method('validateaddress', addr)
        )['result']['isvalid']

    async def rescan_blockchain(self, days_ago: int, full_rescan: bool = False) -> bool:
        """
        Rescan the local blockchain for wallet related transactions.
        :param days_ago: how many days the blockchain rescanning will pass
        :param full_rescan: blockchain rescanning will start from block 1
        :return: boolean value
        """
        blocks_ago = await bitcointools.calc_blocks_by_days(days_ago)
        total_blocks = (
            await self.get_blockchain_info()
        )['blocks']
        block_height = 1 if full_rescan else total_blocks - blocks_ago

        error = (
            await self._call_method('rescanblockchain', block_height)
        )['error']

        return True if not error else False

    async def get_balance(self) -> float:
        """
        Returns the total available balance.
        :return: total balance
        """
        return (
            await self._call_method('getbalance')
        )['result']

    async def send_to_address(self, addr: str, amount: int or float) -> None or InvalidAddress:
        """
        Send an amount to a given address.
        :param addr: Bitcoin address
        :param amount: amount to send
        :return: tx hash
        """
        error = (
            await self._call_method('sendtoaddress', addr, amount)
        )['error']

        if error is not None and error['code'] == -5:
            raise InvalidAddress

    async def list_transactions(self,
                                count: int = 100,
                                include_watchonly: bool = True,
                                to_list: bool = True) -> list or not list:
        """
        Returns up to 'count' most recent transactions.
        :param count: The number of transactions to return
        :param include_watchonly: Include transactions to watch-only addresses
        :param to_list: will return list or genexpr
        :return: list of transactions
        """
        list_txs = (
            await self._call_method('listtransactions', '*', count, 0, include_watchonly)
        )['result']

        if to_list:
            return list_txs

        return (tx for tx in list_txs)
