import datetime
from unittest import mock
from typing import Dict

import pytest
from flask.testing import FlaskClient

import main


@pytest.fixture
def client() -> FlaskClient:
    with main.app.test_client() as client:
        yield client


def ztest_main(config_file_mock: Dict[str, str]) -> None:
    main.get_configuration_args = mock.MagicMock()
    main.get_configuration_args.return_value = config_file_mock
    main.load_config_file = mock.MagicMock()
    main.main()
    assert main.get_configuration_args.called
    assert main.load_config_file.called


def test_alive(client) -> None:
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
    timestamp = datetime.datetime.now().timestamp()
    res = client.get(f"/alive?_={timestamp}", headers=headers)
    assert res.status_code == 204
