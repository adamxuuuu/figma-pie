# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/2/24 11:06 AM
# @Author    :AdamXu
import json
from pathlib import Path
import csv
import random
import tkinter as tk
from tkinter import filedialog


class Utils:

    @staticmethod
    def unpackDict(d: dict, res: dict):
        for k, v in d.items():
            if type(v) == dict:
                Utils.unpackDict(v, res)
            # elif type(v) == list(dict):
            #     [Utils.unpackDict(i, res) for i in v if type(i) == dict]
            else:
                res[k] = v

    @staticmethod
    def convert2Dict() -> dict:
        res = {}
        _dict = {}

        tk.Tk().withdraw()
        file2read = Path(filedialog.askopenfilename())

        if file2read.name.endswith('.json'):
            _dict = json.loads(file2read.read_text())
        elif file2read.name.endswith('.csv'):
            with open(file2read, 'r') as file:
                csv_file = csv.DictReader(file)
                _dict = dict(random.choice(list(csv_file)))
        else:
            raise RuntimeError('File type not supported of {}'.format(file2read.name.split('.')[1]))
        Utils.unpackDict(_dict, res)
        return res


if __name__ == '__main__':
    util = Utils()

    # parse a json file
    data = Utils.convert2Dict()
    [print(k + ':' + str(v)) for k, v in data.items()]
