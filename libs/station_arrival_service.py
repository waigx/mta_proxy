from http.server import BaseHTTPRequestHandler
from libs.station_arrival import StationArrivals
import logging
import json

class StationArrivalService(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _set_error_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data_raw = self.rfile.read(content_length)
        api_key = None
        routes = None
        stations = None
        directions = None

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data_raw.decode('utf-8'))

        try:
            request = json.loads(post_data_raw.decode('utf-8'))
            api_key = request["api_key"]
            routes = request["route_ids"]
            stations = request["station_ids"]
            directions = request["directions"]
        except Exception as err:
            self._set_error_response(400)
            logging.error("Error Parsing request")
            logging.error(err)
            self.wfile.write("Error Parsing request".encode(encoding='utf_8'))
            return

        try:
            sa = StationArrivals(api_key, routes, stations)
            trains = sa.directional_arrival(directions)
            responseJson = sa.format(trains)
            self._set_response()
            self.wfile.write(json.dumps(responseJson).encode(encoding='utf_8'))
        except Exception as err:
            self._set_error_response(500)
            logging.error("Error Getting Trains Infos")
            logging.error(err)
            self.wfile.write("Error Parsing request".encode(encoding='utf_8'))
            return
