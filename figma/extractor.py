# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
import json
import re
import sys
from pathlib import Path

HOME = Path(__file__).parents[1]


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


class Extractor:

    def __init__(self, cache_path):
        self._out_path = HOME / 'attributes.txt'
        self._res = dict()
        self._data_path = HOME / cache_path

        if self._data_path.exists():
            self._data = json.loads(self._data_path.read_text())
        else:
            print('-> Local cache not found, please run script with argument --file')
            sys.exit()

    def extract(self):
        self.__extract(self._data)
        # show changes
        self.__diff()
        self._out_path.write_text(''.join(["{}|{}\n".format(k, v) for k, v in self._res.items()]))

        return self._res

    def __extract(self, d):
        for k, v in d.items():
            try:
                if k == "name" and re.match('[A-Z]+_[A-Z]+_*', v):
                    _id = [v for k, v in d.items() if k == 'id']
                    _content = [v for k, v in d.items() if k == 'characters']
                    attr = v.split('|')
                    self._res[attr[0]] = attr[1] + '|' + " ".join(_content) + '|' + " ".join(_id) \
                        if len(attr) > 1 else ''
                # Recursion
                if isinstance(v, list):
                    for item in v:
                        self.__extract(item)
            except AttributeError:
                # print('{},{}'.format(k, v))
                pass

    def __load(self):
        d = {}
        try:
            with open(self._out_path, 'r') as cache:
                for line in cache:
                    (k, v) = line.split('|', 1)
                    d[k] = v
        except FileNotFoundError or ValueError:
            pass
        return d

    def __diff(self):
        removed = set(self.__load()) - set(self._res)
        added = set(self._res) - set(self.__load())
        for rem in removed:
            prRed('- ' + rem)
        for ad in added:
            prGreen('+ ' + ad)
