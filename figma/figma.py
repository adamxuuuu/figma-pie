# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
import sys
from pathlib import Path
import requests
import json

HOME = Path(__file__).parents[1]


class Figma:

    def __init__(self, token, cache):
        self._api_uri = 'https://api.figma.com/v1/'
        self._token_path = HOME / 'secret/token.json'
        self._api_token = token
        self._cache = cache

    def get_file(self, file_key, params=None):
        """
        Get figma file with specified parameters

        :param file_key: unique file id
        :param params:
        version [String]: A specific version ID to get. Omitting this will get the current version of the file
        ids: Comma separated list of nodes that you care about in the document. If specified, only a subset of the
            document will be returned corresponding to the nodes listed, their children, and everything between the root
            node and the listed nodes
        depth [Number]: Positive integer representing how deep into the document tree to traverse. For example, setting
            this to 1 returns only Pages, setting it to 2 returns Pages and all top level objects on each page.
            Not setting this parameter returns all nodes
        geometry [String]: Set to "paths" to export vector data
        plugin_data [String]: A comma separated list of plugin IDs and/or the string "shared". Any data present in the
            document written by those plugins will be included in the result in the `pluginData` and `sharedPluginData`
            properties.
        :return: A standard response.text
        """
        optional_param = ''
        if params:
            optional_param += '?'
            for k, v in params.items():
                optional_param += k + '=' + v + '&'

        endpoint = 'files/{0}{1}'.format(file_key, optional_param)
        print('-> Connecting to figma api endpoint {}'.format(self._api_uri + endpoint))
        data, code = self.__request(endpoint, method='get')

        if data is None:
            print('-> Server responded with code {}, abort!'.format(code))
            sys.exit()

        # Store to cache
        self.__cache(data)

        return data

    def __request(self, endpoint, method='get', payload=None):
        method = method.lower()

        if payload is None:
            payload = ''

        header = self.__header()

        try:
            resp = self.__response(header, endpoint, method, payload)
            # Check response status
            code = resp.status_code
            if code == 200:
                # Save token to a json file if connection is OK
                self._token_path.write_text(json.dumps({"FIGMA-TOKEN": self._api_token}))
                return json.loads(resp.text), code
            else:
                return None, code
        except (Exception, requests.HTTPError, requests.exceptions.SSLError) as e:
            print('Error occurred attempting to make an api request. {0}'.format(e))
            sys.exit()

    def __cache(self, data: dict, key='document'):
        _d = data[key]
        try:
            print('-> Writing content to cache')
            (HOME / self._cache).write_text(json.dumps(_d))
        except OSError or json.decoder.JSONDecodeError as e:
            print('-> Warning! fail writing to cache {}, {}'.format(self._cache, e))

    def __header(self) -> dict[str: str]:
        if self._api_token == '':
            try:
                info = json.loads(self._token_path.read_text())
                self._api_token = info['FIGMA-TOKEN']
            except FileNotFoundError:
                print('-> Token not found, please run with argument --token')
                sys.exit()

        return {'X-Figma-Token': '{0}'.format(self._api_token),
                'Content-Type': 'application/json'}

    def __response(self, header, endpoint, method='get', payload=None) -> requests.Response:
        url = '{0}{1}'.format(self._api_uri, endpoint)
        if method == 'head':
            response = requests.head(url, headers=header)
        elif method == 'delete':
            response = requests.delete(url, headers=header)
        elif method == 'get':
            response = requests.get(url, headers=header, data=payload)
        elif method == 'options':
            response = requests.options(url, headers=header)
        elif method == 'post':
            response = requests.post(url, headers=header, data=payload)
        elif method == 'put':
            response = requests.put(url, headers=header, data=payload)
        else:
            print('invalid api method {}'.format(method))
            sys.exit()
        return response
