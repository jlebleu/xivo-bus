# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from xivo_bus.ctl.amqp_transport_client import AMQPTransportClient
from xivo_bus.ctl.marshaler import Marshaler


class BusProducer(object):
    """
    The methods on this class are thread safe except for the following:

    * close
    * connect

    """

    def __init__(self):
        self._transport = None
        self._marshaler = Marshaler()

    def close(self):
        if not self.connected:
            return

        self._transport.close()
        self._transport = None

    def connect(self):
        if self.connected:
            raise Exception('already connected')

        self._transport = self._new_transport()

    @property
    def connected(self):
        return self._transport is not None

    def _new_transport(self):
        return AMQPTransportClient.create_and_connect()

    def declare_exchange(self, name, exchange_type, durable):
        self._transport.exchange_declare(name, exchange_type, durable)

    def publish_event(self, exchange, routing_key, event):
        body = self._marshaler.marshal_command(event)
        self._transport.send(exchange, routing_key, body)
