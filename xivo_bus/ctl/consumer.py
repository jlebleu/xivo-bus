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

import logging
import pika
from pika.exceptions import AMQPConnectionError

from xivo_bus.ctl.marshaler import Marshaler

logger = logging.getLogger(__name__)


class BusConsumer(object):

    def __init__(self):
        self._marshaler = Marshaler()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def add_binding(self, callback, queue_name, exchange, key):
        self.callback = callback
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, exclusive=False, durable=True)
        self.channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=key)

    def on_message(self, channel, method, header, body):
        body = self._marshaler.unmarshal_message(body)
        logger.debug('Received new event : %s', body)
        self.callback(body)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        logger.info('Running...')
        try:
            self.channel.basic_consume(self.on_message, self.queue_name)
            self.channel.start_consuming()
        except AMQPConnectionError:
            raise BusConnectionError()

    def stop(self):
        if self.connection.is_open:
            self.channel.stop_consuming()
            self.connection.close()


class BusConnectionError(Exception):
    pass
