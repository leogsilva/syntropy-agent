import configparser
import os


class Config:

    _data = None
    _file = "/etc/noia-agent/config.ini"

    def __init__(self):
        self._data = configparser.ConfigParser()
        self._data.read([self._file])
        for subject in self._data:
            for param in self._data[subject]:
                os.environ[param.upper()] = self._data[subject][param]

    def get(self, subject, param):
        return self._data[subject][param]
