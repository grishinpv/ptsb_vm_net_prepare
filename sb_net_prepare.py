#!/usr/bin/python3
import glob
import json
import ipaddress
import re
import os


# build PBR rules
## --------------------------------

path = "/mnt/images/*/subimage-*.json"
shift = "        "
rule_template = shift + "- from: {0}\n" + shift + "  table: 200\n"

rules = ""

for filename in glob.glob(path):
     with open(filename, "r") as f:
             conf = json.load(f)
             if "tunnel-network" in conf.keys():
                  ip = ipaddress.ip_address(conf["tunnel-network"].split("/")[0]) + 2
             rules += rule_template.format(ip)

if len(rules) == 0:
     raise "No rules found"


# update config
# --------------------------------

netpaln_config_template = "/etc/netplan/01-netcfg.yaml_template"
netpaln_config = "/etc/netplan/01-netcfg.yaml"

with open(netpaln_config_template, "r") as f:
     content = f.read()
     content_new = content.replace("{{ rules }}", rules)

with open(netpaln_config, "w") as f:
     f.write(content_new)


# apply config
# --------------------------------

os.system("netplan apply")


