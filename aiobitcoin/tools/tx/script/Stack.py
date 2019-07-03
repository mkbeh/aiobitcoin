"""
VM Stack data structure
"""

from . import errno
from . import ScriptError


class Stack(list):
    def pop(self, *args, **kwargs):
        try:
            return super(Stack, self).pop(*args, **kwargs)
        except IndexError:
            raise ScriptError("pop from empty stack", errno.INVALID_STACK_OPERATION)

    def __getitem__(self, *args, **kwargs):
        try:
            return super(Stack, self).__getitem__(*args, **kwargs)
        except IndexError:
            raise ScriptError("getitem out of range", errno.INVALID_STACK_OPERATION)
