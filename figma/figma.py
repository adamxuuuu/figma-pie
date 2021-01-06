# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      :2021/1/6 3:21 PM
# @Author    :AdamXu
import sys

import requests
import json
import os


class Figma:

    def __init__(self, token, cache):
        self._api_uri = 'https://api.figma.com/v1/'
        self._token_path = "../token.json"
        self._api_token = token
        self._cache = cache

        self._load_info()

    def _api_request(self, endpoint, method='get', payload=None):
        method = method.lower()

        if payload is None:
            payload = ''

        header = {'X-Figma-Token': '{0}'.format(self._api_token), 'Content-Type': 'application/json'}

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
                with open(self._token_path, 'w') as of:
                    json.dump(info, of)
                of.close()
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

        data = self._api_request('files/{0}{1}'.format(file_key, optional_param), method='get')

        if use_cache:
            self._to_cache(data)
        return data

    def _to_cache(self, data):
        try:
            print("Writing content to cache...")
            with open(self._cache, 'w') as of:
                json.dump(data["document"], of)
        except OSError or json.decoder.JSONDecodeError as e:
            print("Error when writing to file {}, {}".format(self._cache, e))
        finally:
            of.close()

    def _load_info(self):
        if not os.path.isfile(self._cache):
            return
        if self._api_token == '':
            try:
                with open(self._token_path, 'r') as json_file:
                    info = json.load(json_file)
                    self._api_token = info["FIGMA-TOKEN"]
            except FileNotFoundError:
                print('local token file not found, please run with argument --token')
                print('System exiting...')
                sys.exit()
