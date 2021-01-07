# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
from figma import Figma
from extractor import Extractor
import sys


ids = {'ids': '1283%3A4922,1220%3A6129,1220%3A6404,1220%3A6687,1220%3A6939'}
cache_path = './content.json'
headers = ''
fileId = ''


if __name__ == '__main__':
    # Parse CLI argument
    for arg in sys.argv[1:]:
        if arg == "--help":
            print(
                """
runner --file='[FILE ID]' --token='[TOKEN]' [OPTIONS]... [FRAME IDS]...(optional)
OPTIONS:
--help      Display this message.
--file      The ID of the Figma file to fetch and render. The default is 'FIGMA_FILE_ID' at environment variable.
--token     The Access Token for your account. The default is 'FIGMA_TOKEN' at environment variable.          
                """)
            sys.exit()
        elif "--token" in arg:
            headers = arg.split('=')[1]
        elif "--file" in arg:
            fileId = arg.split('=')[1]

    if len(sys.argv) > 1:
        # Reload data from figma source if needed
        figma = Figma(headers, cache_path)
        figma.get_file(fileId, ids)

    ext = Extractor(cache_path)
    res = ext.extract()

    print('-> finished extracting {} attributes'.format(len(res)))

