import json
import re
from progress.bar import Bar


class Extractor:

    def __init__(self, content_path):
        # Content data from a local json file (Figma format)
        self._data = {}
        # List of all (filtered) attributes found
        self._res = []
        # Content json file path
        self._content_path = content_path

    def _get_data(self):
        """
        Load data from json file
        """
        with open(self._content_path, 'r') as json_file:
            self._data = json.load(json_file)

    def _find_attr(self, d):
        attr_id = [v for k, v in d.items() if k == 'id']
        for k, v in d.items():
            try:
                if k == "name" and re.match("CN_*", v):
                    self._res.append((v, attr_id))
                if isinstance(v, list):
                    for item in v:
                        self._find_attr(item)
            except AttributeError:
                pass

    def write_attr(self):
        self._get_data()
        self._find_attr(self._data)
        with open("attr.txt", 'w') as of:
            bar = Bar('Processing', max=len(self._res))
            for _name, _id in self._res:
                s = "%s|%s\n" % (_name, _id[0])
                of.write(s)
                bar.next()
            bar.finish()
