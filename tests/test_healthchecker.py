import pytest
import urllib.request
from healthyurl import check_health


def test_check_health_valid_url(mocker):
    # Mock a valid response
    mocker.patch("urllib.request.urlopen", return_value=True)
    check_health("http://example.com", quiet=False)  # no error


def test_check_health_without_scheme(mocker):
    # Mock a valid response without the http:// scheme
    urlopen = mocker.patch("urllib.request.urlopen", return_value=True)
    check_health("example.com", quiet=False)
    urlopen.assert_called_once_with("http://example.com")


@pytest.mark.parametrize("quiet", [False, True])
def test_check_health_invalid_url(mocker, quiet):
    # Mock an error response
    mock_error = urllib.error.URLError("Connection refused")
    mocker.patch("urllib.request.urlopen", side_effect=mock_error)

    with pytest.raises(SystemExit) as exc_info:
        check_health("http://invalid-url.com", quiet=quiet)

    assert exc_info.value.code == 1


@pytest.mark.parametrize("quiet", [False, True])
def test_check_health_invalid_url_without_scheme(mocker, quiet):
    # Mock an error response without http:// scheme
    mock_error = urllib.error.URLError("Connection refused")
    mocker.patch("urllib.request.urlopen", side_effect=mock_error)

    with pytest.raises(SystemExit) as exc_info:
        check_health("invalid-url.com", quiet=quiet)

    assert exc_info.value.code == 1
