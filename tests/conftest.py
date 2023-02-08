import pytest
from nornir import InitNornir
from nornir.core.filter import F
import sys
from pytest_tools import nornir_set_creds

def pytest_addoption(parser):
    params = sys.argv[1:]
    group = parser.getgroup("Test", "My test option")
    group.addoption(
        "--device_target",
        help="device_target", metavar="device_target", dest='device_target', default=None)

@pytest.fixture(scope="session", autouse=True)
def pytestnr(request):
    device_target = request.config.getoption("--device_target")
    pytestnr = InitNornir(config_file="./inventory/config.yaml")
    nornir_set_creds(pytestnr)
    pytestnr = pytestnr.filter(F(groups__contains=f"{device_target}"))
    yield pytestnr
    pytestnr.close_connections()
