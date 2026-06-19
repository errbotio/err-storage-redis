## Redis storage plugin for errbot


### About
[Errbot](http://errbot.io) is a python chatbot, this storage plugin allows you to use it with Redis databases as a persistent storage.

### Installation

1. Install [redis library](https://pypi.python.org/pypi/redis)
2. Then you need to add this section to your config.py:

 ```python
 BOT_EXTRA_STORAGE_PLUGINS_DIR='/path/to/err-storage'
 STORAGE = 'Redis'
 STORAGE_CONFIG = {
     'host': 'localhost',
     'port': 6379,
     'db': 0,
     'password': 'xyz123',
 }
 ```

`STORAGE_CONFIG` will send any option specified as an argument to `redis.StrictRedis`.

3. Start your bot in text mode: `errbot -T` to give it a shot.

### Running Tests

To run the automated test suite:

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the dependencies and testing requirements:
   ```bash
   pip install -r requirements.txt errbot pytest tox fakeredis
   ```
3. Run the tests using `pytest` directly:
   ```bash
   pytest
   ```
   Or run both tests and style checks using `tox`:
   ```bash
   tox
   ```
