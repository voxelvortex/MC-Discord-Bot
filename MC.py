import urllib.request
import json
from pythonping import ping


class Server:
    ip = ""
    port = ""

    def __init__(self, ip, port="25565"):
        self.port = port
        self.ip = ip

    def get_json_data(self):
        request = urllib.request.urlopen("https://mcapi.us/server/status?ip={0}&port={1}".format(self.ip, self.port))
        response = request.read().decode("utf-8")
        data = json.loads(response)
        return data

    def get_ping(self):
        return ping(self.ip, count=10, verbose=False)
