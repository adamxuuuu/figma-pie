# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
from figma import Figma
from extractor import Extractor
from drive import updateSheet
import sys

# 1220%3A5791,1304%3A5141,1304%3A5475,1304%3A5751,1304%3A5997,1309%3A3,1607%3A8781,1608%3A11,1583%3A44,1598%3A8650
NODE_IDS = {'ids': '1220%3A5791,1304%3A5141,1304%3A5475,1304%3A5751,1304%3A5997,1309%3A3,1607%3A8781,1608%3A11,'
                   '1583%3A44,1598%3A8650'}
CACHE = 'content.json'


def main():
    headers = ''
    file_id = ''
    update = False
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
            file_id = arg.split('=')[1]
        elif "--update" in arg:
            update = True

    if file_id:
        # Reload data from figma source if file_id are provided
        api = Figma(headers, CACHE)

        # Get the files and store to cache if specified
        api.get_file(file_id, NODE_IDS)

    res = Extractor(CACHE).extract()

    print('-> finished extracting {} attributes'.format(len(res)))

    if update:
        updateSheet()


if __name__ == '__main__':
    main()
