from figma import Figma
from attr_extractor import Extractor
import sys

cache = "content.json"
headers = ""
fileId = ""

if __name__ == '__main__':
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
            headers = {"X-Figma-Token": arg.split('=')[1]}
        elif "--file" in arg:
            fileId = arg.split('=')[1]

    if len(sys.argv) > 1:
        print("Reload file using arg...")
        # Reload data from figma source if needed
        figma = Figma(headers, fileId, cache)
        figma.get_file()

    ext = Extractor(cache)
    ext.write_attr()
