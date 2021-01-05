import json
import re
from progress.bar import Bar

from ordered_set import OrderedSet

out_path = "attr.txt"


class Extractor:

    def __init__(self, content_path):
        # Content data from a local json file (Figma format)
        self._data = {}
        # List of all (filtered) attributes found
        self._res = OrderedSet()
        # Content json file path
        self._content_path = content_path

    def _get_data(self):
        """
        Load data from json file
        """
        with open(self._content_path, 'r') as json_file:
            self._data = json.load(json_file)

    def _find_attr(self, d):
        for k, v in d.items():
            try:
                if k == "name" and re.match("CN_*", v):
                    # _id = [v for k, v in d.items() if k == 'id']
                    _type = [v for k, v in d.items() if k == 'type']
                    self._res.add((v, _type[0]))
                if isinstance(v, list):
                    for item in v:
                        self._find_attr(item)
            except AttributeError:
                pass

    def write_attr(self):
        self._get_data()
        self._find_attr(self._data)
        print(self._res)
        with open(out_path, 'w') as of:
            bar = Bar('Processing', max=len(self._res))
            for _tup in self._res:
                s = "{},{}\n".format(_tup[0], _tup[1])
                of.write(s)
                bar.next()
            bar.finish()
