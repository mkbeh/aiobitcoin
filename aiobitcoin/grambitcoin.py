# -*- coding: utf-8 -*-
import logging
import aiohttp
import ujson

from asyncio.futures import TimeoutError
from aiohttp.client_exceptions import ContentTypeError, InvalidURL, ServerDisconnectedError

from .bitcoinerrors import *


class GramBitcoin:
    def __init__(self, url=None, read_timeout=20, session_required=False):
        self.url = url
        self._session_required = session_required
        self.session = None
        self.read_timeout = read_timeout

        self._check_session_required()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    def _check_session_required(self):
        if self._session_required:
            self.session = aiohttp.ClientSession(read_timeout=self.read_timeout, json_serialize=ujson.dumps)

    def check_gram(self, gram):
        if not gram:
            return aiohttp.ClientSession(read_timeout=self.read_timeout, json_serialize=ujson.dumps)
        else:
            return gram.session

    @staticmethod
    def check_url(url, gram):
        if not url:
            return gram.url

        return url

    async def call_method(self, method, *args):
        headers = {'Content-Type': 'application/json'}
        data = {'jsonrpc': '1.0', 'method': f'{method}', 'params': args}

        try:
            response = await self.session.post(url=self.url, headers=headers, data=ujson.dumps(data))
        except (ContentTypeError, InvalidURL, ServerDisconnectedError, TimeoutError):
            await self.close_session()
            logging.critical('No connection to the daemon.')
            raise NoConnectionToTheDaemon
        else:
            return await response.json()

    async def close_session(self):
        await self.session.close()
