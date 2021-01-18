# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
from figma import Figma
from extractor import Extractor
import sys

# 1220%3A5791,1304%3A5141,1304%3A5475,1304%3A5751,1304%3A5997,1309%3A3
ids = {'ids': '1220%3A5791,1304%3A5141,1304%3A5475,1304%3A5751,1304%3A5997,1309%3A3'}
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

    if fileId:
        # Reload data from figma source if header and fileId are provided
        api = Figma(headers, cache_path)
        file = api.get_file(fileId, ids)

    ext = Extractor(cache_path)
    res = ext.extract()

    print('-> finished extracting {} attributes'.format(len(res)))
