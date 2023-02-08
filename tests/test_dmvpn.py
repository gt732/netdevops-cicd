from nornir_scrapli.tasks import send_command
import pytest
from nornir import InitNornir
from nornir.core.filter import F
import sys


def check_dmvpn_tunnel_state(task):
    result = task.run(task=send_command, command='show dmvpn')
    task.host["dmvpn_facts"] = result.scrapli_response.textfsm_parse_output()
    

def get_dev_names():
    params = sys.argv[1:]
    for i, param in enumerate(params):
        if param == "--device_target":
            device_target = params[i + 1]
            break
    else:
        device_target = "dev"
    nr = InitNornir(config_file="./inventory/config.yaml")
    filtered = nr.filter(F(groups__contains=f"{device_target}"))
    devices = filtered.inventory.hosts.keys()
    nr.close_connections()
    return devices


class TestDmvpn:
  
  
  @pytest.fixture(scope="class", autouse=True)
  def setup_teardown(self, pytestnr):
    pytestnr.run(task=check_dmvpn_tunnel_state)
    yield
    for host in pytestnr.inventory.hosts.values():
      host.data.pop("dmvpn_facts")
      
      
  @pytest.mark.parametrize(
        'device_name', get_dev_names()
        )
  
  
  def test_dmvpn(self, pytestnr, device_name):
    my_list = []
    nr_host = pytestnr.inventory.hosts[device_name]
    dmvpn_facts =  nr_host["dmvpn_facts"]
    for i in dmvpn_facts:
      tunnel_state = i['state']
      my_list.append(tunnel_state)
      for state in my_list:
        assert state == 'UP'
        print(f"\nDevice: {device_name} passed the test")