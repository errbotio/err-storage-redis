# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import logging
from jsonpickle import encode, decode
from typing import Any

from errbot.storage.base import StorageBase, StoragePluginBase
from errbot.utils import compat_str
import redis

log = logging.getLogger('errbot.storage.redis')

SERVER = 'server'
PORT = 'port'
DB = 'db'
PASSWORD = 'password'

GLOBAL_PREFIX = 'errbot'


class RedisStorage(StorageBase):

    def _make_nskey(self, key):
        return ':'.join((GLOBAL_PREFIX, self.ns, compat_str(key)))

    def __init__(self, redis, namespace):
        self.redis = redis
        self.ns = namespace
        self._all_keys = self._make_nskey('*')

    def get(self, key: str) -> Any:
        unique_key = self._make_nskey(key)
        log.debug('Get key: %s' % unique_key)
        result = self.redis.get(unique_key)
        if result is None:
            raise KeyError("%s doesn't exists." % (unique_key))
        return decode(result.decode())

    def remove(self, key: str):
        unique_key = self._make_nskey(key)
        log.debug("Removing value at '%s'", unique_key)
        result = self.redis.delete(unique_key)
        if not result:
            raise KeyError('%s does not exist' % (unique_key))

    def set(self, key: str, value: Any) -> None:
        unique_key = self._make_nskey(key)
        log.debug("Setting value '%s' at '%s'", encode(value), unique_key)
        self.redis.set(unique_key, encode(value))

    def len(self):
        return len(self.keys())

    def keys(self):

        keys = self.redis.keys(pattern=self._all_keys)
        base_namespace = ':'.join((GLOBAL_PREFIX, self.ns))
        filtered_keys = []

        for key in keys:
            key = compat_str(key)
            filtered_keys.append(key.lstrip(base_namespace))

        log.debug('Keys: %s' % filtered_keys)
        return filtered_keys

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
