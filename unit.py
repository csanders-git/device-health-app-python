import datetime
import requests
import time


proxyDict = {
              "http"  : "http://localhost:8080",
              "https" : "https://localhost:8080"
            }

def test_alive_get() -> None:
    headers = {
        "Host": "127.0.0.1:53106",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "X-Xsrftoken": "e25880ac600d45a593fcc633a4b271fe",
        "Origin": "https://api-c162f2e2.duosecurity.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }
    timestamp = int(datetime.datetime.now().timestamp()*1000)
    resp = requests.get(
        f"http://127.0.0.1:53106/alive?_={timestamp}", headers=headers, proxies=proxyDict
    )
    assert resp.status_code == 204
    assert resp.text == ''
    assert 'Access-Control-Allow-Methods' in resp.headers
    assert resp.headers['Access-Control-Allow-Methods'] == 'GET, OPTIONS'

def test_alive_options() -> None:
    headers = {
        "Host": "127.0.0.1:53106",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "X-Xsrftoken": "e25880ac600d45a593fcc633a4b271fe",
        "Origin": "https://api-c162f2e2.duosecurity.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }
    timestamp = int(datetime.datetime.now().timestamp()*1000)
    resp = requests.options(f"http://127.0.0.1:53106/alive?_={timestamp}", headers=headers, proxies=proxyDict)

    expected_headers = [
        'Access-Control-Allow-Methods',
        'Content-Type',
        'Access-Control-Allow-Origin',
        'Transfer-Encoding',
        'Date',
        'Access-Control-Allow-Headers',
        'Connection'
    ]
    assert resp.status_code == 204
    assert resp.text == ''
    for header in expected_headers:
        if header not in resp.headers:
            raise AssertionError()


def test_index_get() -> None:
    headers = {
        "Host": "127.0.0.1:53106",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "X-Xsrftoken": "e25880ac600d45a593fcc633a4b271fe",
        "Origin": "https://api-c162f2e2.duosecurity.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }
    resp = requests.get(f"http://127.0.0.1:53106/", headers=headers, proxies=proxyDict)
    assert resp.status_code == 404
    assert resp.text == 'Cannot GET /'
