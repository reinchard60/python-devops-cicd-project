import pytest
import requests
from pytest_mock import MockerFixture

from simple_http_checker.checker import check_urls

def test_check_urls_success(mocker: MockerFixture):
    mock_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True
    mock_requests_get.return_value = mock_response

    urls = ["https://www.example.com"]
    results = check_urls(urls)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "200 OK"