import json
import os


class JsonReader:
    res = {}

    def __init__(self, root_path):
        self.path = root_path
        self.json_files = [pos_json for pos_json in os.listdir(root_path) if pos_json.endswith('.json')]
        print('Following json files are being imported...', self.json_files)

    def unpack_dict(self, d):
        for k, v in d.items():
            if type(v) == dict:
                self.unpack_dict(v)
            else:
                self.res[k] = v

    def run(self):
        for index, jf in enumerate(self.json_files):
            with open(os.path.join(self.path, jf), "r") as j:
                j_dict = json.load(j)
                self.unpack_dict(j_dict)


if __name__ == '__main__':
    jr = JsonReader('drive/')
    jr.run()
    print(jr.res)
