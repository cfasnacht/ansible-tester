#!/usr/bin/python3

import argparse
from argparse import RawTextHelpFormatter
import subprocess

parser = argparse.ArgumentParser(
        description="Simplistic Ansible Docker playbook tester / runner \nWith no options the ansible playbook is ran, the container stopped and removed",
        formatter_class=RawTextHelpFormatter)
parser.add_argument("-d", "--debug", help="only run Ansible play no clean up, used for debugging",
                    action="store_true")
parser.add_argument("-x", "--cleanup", help="stop and remove the test container",
                    action="store_true")
args = parser.parse_args()

distro = "ubuntu"
container_name = "test-ansible-container-" + distro
docker_repo = "local-ansible-test:" + distro

if not args.cleanup:
  subprocess.call(["docker", "build", "-t", docker_repo,  "docker/" + distro])
  subprocess.call(["docker", "run", "-ti", "--privileged",  "--name", container_name, "-d", "-p", "5022:22", docker_repo])
  subprocess.call(["ansible-playbook", "-i", "inventories/localdocker", "plays/site.yml", "--diff", "-vv"])

if not args.debug:
  subprocess.call(["docker", "stop", container_name])
  subprocess.call(["docker", "rm",  container_name])
