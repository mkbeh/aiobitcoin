# -*- coding: utf-8 -*-

#    BitcoinLib - Python Cryptocurrency Library
#    CONFIG - Configuration settings
#    © 2019 March - 1200 Web Development <http://1200wd.com/>
#    © 2019 July - mkbeh
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys


# General defaults
PY3 = sys.version_info[0] == 3
TYPE_TEXT = str

# Mnemonics
DEFAULT_LANGUAGE = 'english'

# File locations
WORDLIST_DIR = os.path.abspath('aiobitcoin/wordlists')
