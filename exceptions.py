from collections import namedtuple


Error = namedtuple('Error', ('message', ))


class CommandError(Exception):
    pass


class Disconnect(Exception):
    pass
