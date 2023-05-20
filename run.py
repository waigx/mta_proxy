#!/usr/bin/env python

from http.server import ThreadingHTTPServer
import logging
from libs.station_arrival_service import StationArrivalService


def run(server_class=ThreadingHTTPServer, handler_class=StationArrivalService, port=8090):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
