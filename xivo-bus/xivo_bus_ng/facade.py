# -*- coding: utf-8 -*-

from xivo_bus_ng import client
from xivo_bus_ng import connection

_conn = connection.Connection()
_client = client.Client(_conn)


def connect():
    # XXX maybe connect should be explicit AND implicit
    _conn.connect()


def declare(entity):
    _client.declare(entity)


def publish(message):
    _client.publish(message)
