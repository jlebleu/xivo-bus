# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

import pika


class Config(object):

    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 5672
    DEFAULT_VIRTUAL_HOST = 'xivo'

    def __init__(self,
                 host=DEFAULT_HOST,
                 port=DEFAULT_PORT,
                 virtual_host=DEFAULT_VIRTUAL_HOST):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host

    def to_connection_params(self):
        return pika.ConnectionParameters(host=self.host,
                                         port=self.port,
                                         virtual_host=self.virtual_host)


default_config = Config()