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

    def _api_request(self, endpoint, method='get', payload=None):
        method = method.lower()

        if payload is None:
            payload = ''

        header = self._header()

        try:
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
                response = None
            if response.status_code == 200:
                # Save header and file id to a json file if write success
                info = {"FIGMA-TOKEN": self._api_token}
                self._token_path.write_text(json.dumps(info))
                return json.loads(response.text)
            else:
                return None
        except (Exception, requests.HTTPError, requests.exceptions.SSLError) as e:
            print('Error occurred attempting to make an api request. {0}'.format(e))
            return None

    def get_file(self, file_key, params=None, use_cache=True):
        """
        Get figma file with specified parameters

        :param use_cache: if caching the content
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
        data = self._api_request(endpoint, method='get')

        if data is None:
            print('-> Connection failed, abort...')
            sys.exit()

        if use_cache:
            self._toCache(data)

        return data

    def _toCache(self, data, key='document'):
        _d = data[key]
        try:
            print('-> Writing content to cache')
            (HOME / self._cache).write_text(json.dumps(_d))
        except OSError or json.decoder.JSONDecodeError as e:
            print('Error when writing to file {}, {}'.format(self._cache, e))

    def _header(self):
        if not self._token_path.exists():
            return
        if self._api_token == '':
            try:
                data = self._token_path.read_text()
                info = json.loads(data)
                self._api_token = info['FIGMA-TOKEN']
            except FileNotFoundError:
                print('local token file not found, please run with argument --token')
                sys.exit()
        return {'X-Figma-Token': '{0}'.format(self._api_token), 'Content-Type': 'application/json'}
