import configparser
import os
from pathlib import Path


class ConfigException(Exception):
    pass


class Config:

    _data = None
    _file = "/etc/noia-agent/config.ini"
    config_file = Path(_file)
    if not config_file.is_file():
        print(f"Config file was not found in {_file}")
        raise ConfigException(f"Config file was not found in {_file}")

    def __init__(self):
        self._data = configparser.ConfigParser()
        self._data.read([self._file])
        for subject in self._data:
            for param in self._data[subject]:
                os.environ[param.upper()] = self._data[subject][param]

    def get(self, subject, param):
        return self._data[subject][param]
