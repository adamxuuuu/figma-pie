# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
import json
import re
import sys


def prRed(skk): print("\033[91m {}\033[00m".format(skk))
def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


class Extractor:

    def __init__(self, data_path):
        self._out_path = './attributes.txt'
        self._res = dict()

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
                    _id = [v for k, v in d.items() if k == 'id']
                    # _type = [v for k, v in d.items() if k == 'type']
                    attr = v.split('|')
                    self._res[attr[0]] = attr[1] if len(attr) > 1 else ''
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
                    (k, v) = line.split(',')
                    d[k] = v
        except FileNotFoundError:
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
                    s = "{},{}\n".format(k, v)
                    of.write(s)
        except OSError as e:
            print(e)
        finally:
            of.close()

        return self._res
