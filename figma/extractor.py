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

    def _extract(self, d):
        for k, v in d.items():
            try:
                if k == "name" and re.match('[A-Z]+_[A-Z]+_*', v):
                    _id = [v for k, v in d.items() if k == 'id']
                    _content = [v for k, v in d.items() if k == 'characters']
                    attr = v.split('|')
                    self._res[attr[0]] = attr[1] + '|' + " ".join(_content) \
                                         + '|' + " ".join(_id) \
                        if len(attr) > 1 else ''
                if isinstance(v, list):
                    for item in v:
                        self._extract(item)
            except AttributeError:
                # print('{},{}'.format(k, v))
                pass

    def _load_cache(self):
        d = {}
        try:
            with open(self._out_path, 'r') as cache:
                for line in cache:
                    (k, v) = line.split('|', 1)
                    d[k] = v
        except FileNotFoundError or ValueError:
            pass
        return d

    def _show_diff(self):
        removed = set(self._load_cache()) - set(self._res)
        added = set(self._res) - set(self._load_cache())
        for rem in removed:
            prRed('- ' + rem)
        for ad in added:
            prGreen('+ ' + ad)

    def extract(self):
        self._extract(self._data)
        # show changes
        self._show_diff()

        try:
            with open(self._out_path, 'w') as of:
                for k, v in self._res.items():
                    s = "{}|{}\n".format(k, v)
                    of.write(s)
        except OSError as e:
            print(e)
        finally:
            of.close()

        return self._res
