import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import pandas as pd
import h2o
from urllib.parse import urlparse, parse_qs
from Utils import Utils
from AlgorithmicModel import AlogrithmicModel

host_name = ""
port = 3000

class ServerConfiguration():
    def start_server(self):
        server = HTTPServer((host_name, port), MyServer)
        print(time.asctime(), "Server Starts - %s:%s" % (host_name, port))
        h2o.init()
        h2o.connect()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
        print(time.asctime(), "Server Ends - %s:%s" % (host_name, port))

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)

        data = json.loads(post_body.decode())

        df = Utils.load_df_from_json(data)
        prob = AlogrithmicModel.evaluate_instance(df)

        self.send_response(200)
        self.end_headers()
        json_string = json.dumps({"score": prob})
        self.wfile.write(bytes(json_string, "utf-8"))
        return

ServerConfiguration().start_server()