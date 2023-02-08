from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure
from nornir.core.filter import F
from tools import nornir_set_creds
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "--dry_run", dest="dry", action="store_true", help="Will not run on devices"
)
parser.add_argument(
    "--no_dry_run", dest="dry", action="store_false", help="Will run on devices"
)
parser.add_argument(
    "--device_target", help="Enter either prod or dev will run on dev or prod devices"
)
parser.set_defaults(dry=True)
args = parser.parse_args()


nr = InitNornir(config_file="./inventory/config.yaml", core={"raise_on_error": True})

nornir_set_creds(nr)

device_target = parser.parse_args().device_target

filter = nr.filter(F(groups__contains=f"{device_target}"))


def load_vars(task):

    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    group_data = task.run(task=load_yaml, file="./group_vars/all.yaml")
    task.host["group_facts"] = group_data.result
    filter.run(task=generate_dmvpn)

def generate_dmvpn(task):
    dmvpn_template = task.run(
      task=template_file,
      name="Buildling DMVPN Configuration",
      template="dmvpn.j2",
      path="./templates",
  )
    task.host["dmvpn"] = dmvpn_template.result
    filter.run(task=generate_bgp)
    
def generate_bgp(task):
    bgp_template = task.run(
        task=template_file,
        name="Buildling BGP Configuration",
        template="bgp.j2",
        path="./templates",
    )
    task.host["bgp"] = bgp_template.result
    

def config_dmvpn(task):
    dmvpn_output = task.host["dmvpn"]
    task.run(task=napalm_configure, configuration=dmvpn_output, dry_run=args.dry)



def config_bgp(task):
    bgp_output = task.host["bgp"]
    task.run(task=napalm_configure, configuration=bgp_output, dry_run=args.dry)
    
def main():
          
  filter.run(task=load_vars)
  
  config_dmvpn_results = filter.run(task=config_dmvpn)
  
  config_bgp_results = filter.run(task=config_bgp)
  
  print_result(config_dmvpn_results)
  
  print_result(config_bgp_results)
    


if __name__ == "__main__":
  main()
