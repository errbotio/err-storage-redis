# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import logging
from jsonpickle import encode, decode
from typing import Any

from errbot.storage.base import StorageBase, StoragePluginBase
import redis

log = logging.getLogger('errbot.storage.redis')

SERVER = 'server'
PORT = 'port'
DB = 'db'
PASSWORD = 'password'


class RedisStorage(StorageBase):

    def __init__(self, redis, namespace):
        self.redis = redis
        self.ns = namespace

    def get(self, key: str) -> Any:
        result = self.redis.get('{0}.{1}'.format(self.ns, key))
        if result is None:
            raise KeyError("%s.%s doesn't exists." % (self.ns, key))
        return decode(result)

    def remove(self, key: str):
        self.redis.delete('%s.%s'.format(self.ns, key))

    def set(self, key: str, value: Any) -> None:
        log.debug("Setting value '%s.%s' at %s" %
                  (self.ns, key, encode(value)))
        self.redis.set('{0}.{1}'.format(self.ns, key), encode(value))

    def len(self):
        return len(self.keys())

    def keys(self):
        return self.keys(pattern='{0}.*'.format(self.ns))

    def close(self) -> None:
        pass


class RedisPlugin(StoragePluginBase):

    def __init__(self, bot_config):
        super().__init__(bot_config)
        if not all(k in self._storage_config for k in (SERVER, PORT, DB, PASSWORD)):
            raise Exception('You need to specify: {0}, {1}, {2}, {3} in "STORAGE_CONFIG"'.format(
                SERVER, PORT, DB, PASSWORD)
            )

    def open(self, namespace: str) -> StorageBase:
        config = self._storage_config

        connection = redis.StrictRedis(
            host=config[SERVER],
            port=config[PORT],
            db=config[DB],
            password=config[PASSWORD]
        )

        return RedisStorage(connection, namespace)
