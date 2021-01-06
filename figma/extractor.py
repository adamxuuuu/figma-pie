# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
import json
import re
import sys

from ordered_set import OrderedSet


class Extractor:

    def __init__(self, data_path):
        self._out_path = '../attr.txt'
        self._res = OrderedSet()

        try:
            with open(data_path, 'r') as json_file:
                self._data = json.load(json_file)
        except FileNotFoundError:
            print('Local cache not found, please run script with argument --file')
            print('System exiting...')
            sys.exit()

    def _extract(self, d):
        for k, v in d.items():
            try:
                if k == "name" and re.match("CN_*", v):
                    # _id = [v for k, v in d.items() if k == 'id']
                    _type = [v for k, v in d.items() if k == 'type']
                    self._res.add((v, _type[0]))
                if isinstance(v, list):
                    for item in v:
                        self._extract(item)
            except AttributeError:
                # print('{},{}'.format(k, v))
                pass

    def extract(self):
        self._extract(self._data)
        try:
            with open(self._out_path, 'w') as of:
                for _tup in self._res:
                    s = "{},{}\n".format(_tup[0], _tup[1])
                    of.write(s)
        except OSError as e:
            print(e)
        finally:
            of.close()
