import argparse
import json
import os
import datetime
import zoneinfo
import requests
from typing import Dict
from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from urllib.parse import urlparse, parse_qs
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)


@app.route("/", methods=['OPTIONS', 'GET', 'POST'])
def index():
    result = f"Cannot {request.method} /"
    resp = Response(result, status=404)
    return resp


@app.route("/test", methods=['GET'])
def render_test():
    return render_template('test_trigger.html')


# DNS Rebind
@app.route("/alive", methods=['OPTIONS', 'GET'])
def alive_handler() -> Response:
    resp = Response("", status=204)
    if request.method == "GET":
        resp.headers = get_resp_headers(request.headers)
        resp.headers["no-store, must-revalidate"] = "Cache-Control"
    if request.method == "OPTIONS":
        resp.headers = get_resp_headers(request.headers)
    return resp


@app.route("/report", methods=['OPTIONS', 'GET'])
def report_handler() -> Response:
    print(request.url)
    eh_service_url = request.args.get("eh_service_url")
    txid = request.args.get("txid")
    parsed_eh_url = urlparse(eh_service_url)
    parsed_eh_query = parse_qs(parsed_eh_url.query)
    config_args = get_configuration_args()
    config_loc = config_args['config']
    if not os.path.exists(config_loc):
        exit("Unable to load configuration file")
    json_body = json.load(open(config_loc))
    json_body['txid'] = txid
    finished_time = int(datetime.datetime.now().timestamp()*1000)
    assert '_req_trace_group' in parsed_eh_query
    trace_group = parsed_eh_query['_req_trace_group']
    headers = {
        "Host": "2.endpointhealth.duosecurity.com",
        "User-Agent": "Duo Device Health/3.4.0.0 CFNetwork/1125.2 Darwin/20.4.0 (x86_64)",
        "Accept": "*/*",
        "Accept-Language": "en-au",
        "Accept-Encoding": "gzip, deflate"
    }
    url = f"https://2.endpointhealth.duosecurity.com/v1/healthapp/device/health?_req_trace_group={trace_group}?_={finished_time}"
    resp = requests.post(url, json=json_body, headers=headers, verify=False)
    print(str(json_body))
    print(f"status_code={resp.status_code}")
    print(f"text={resp.text}")
    return ""


def get_configuration_args() -> Dict[str, str]:
    default_configuration_file_path = "./config.json"
    description = "An emulation of the Duo Device Health App written in Python"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-c', '--config',
        help='path to the configuration file',
        required=False, nargs='?', type=str,
        const=default_configuration_file_path,
        default=default_configuration_file_path)
    output_args = vars(parser.parse_args())
    return output_args


def get_resp_headers(request_headers) -> Dict[str, str]:
    origin = request_headers.get('Origin', None)
    now = datetime.datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles"))
    formatted_date = now.strftime('%a, %d %b %Y %H:%M:%S %Z')
    headers = {
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Content-Type": "text/plain; charset=utf-8",
        "Connection": "keep-alive",
        "Transfer-Encoding": "chunked",
        "Access-Control-Allow-Headers": "x-xsrftoken",
        "Date": formatted_date,
        "Cache-Control": "no-store, must-revalidate"
    }
    if origin:
        headers["Access-Control-Allow-Origin"] = origin
    return headers


def main() -> None:
    try:
        # Otherwise flask returns 1.0
        WSGIRequestHandler.protocol_version = "HTTP/1.1"
        app.run(host="localhost", port=53106, debug=True)
    except OSError:
        exit("Error: Make sure your Duo Health App is not running.")


if __name__ == "__main__":
    main()
