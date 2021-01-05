import requests
import json
import sys
import os

ids = {"ids": "1220%3A5791,1220%3A6129,1220%3A6404,1220%3A6687,1220%3A6939"}
cred_path = "local/credential.json"


class Figma:

    def __init__(self, headers, file_id, cache):
        self._headers = headers
        self._file_id = file_id
        self._cache = cache

        # Try find info in file
        self._load_info()

    def get_file(self):
        resp = self._get_file(ids)
        try:
            content = resp.json()
            print("Writing results to cache")
            with open(self._cache, 'w') as of:
                json.dump(content["document"], of)
        except IOError or json.decoder.JSONDecodeError:
            print("IOError when writing to file {}".format(self._cache))
            sys.exit()
        finally:
            of.close()

        # Save header and file id to a json file if write success
        info = {"FIGMA-HEADER": self._headers, "FIGMA-FILE-ID": self._file_id}
        with open(cred_path, 'w') as of:
            json.dump(info, of)

    def _get_file(self, params):
        """
        Get figma file with specified parameters

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
        :return: A standard response
        """
        try:
            url = "https://api.figma.com/v1/files/" + self._file_id
            if params:
                url += "?"
                for k, v in params.items():
                    url += k + '=' + v + '&'

            print("Connecting to figma {}.".format(url))

            resp = requests.get(url, headers=self._headers)

            code = resp.status_code
            print("status code: ", code)
            if code == 404:
                print("Requested resource was not found on {}".format(code, url))

            return resp
        except ConnectionError:
            print("Connection abort...")
            sys.exit()

    def _load_info(self):
        if not os.path.isfile(self._cache):
            return
        if self._headers == "" or self._file_id == "":
            with open("local/credential.json", 'r') as json_file:
                info = json.load(json_file)
            if self._headers == "":
                self._headers = info["FIGMA-HEADER"]
            if self._file_id == "":
                self._file_id = info["FIGMA-FILE-ID"]