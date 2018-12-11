#!/usr/bin/python3

import argparse
from argparse import RawTextHelpFormatter
import subprocess

parser = argparse.ArgumentParser(
        description="Simplistic Ansible Docker playbook tester / runner \n\
With no options the ansible playbook is ran, the container stopped and removed\n\
the default play location is play/site.yml",
        formatter_class=RawTextHelpFormatter)
parser.add_argument("-d", "--diff", help="enable ansible --diff",
                    action="store_true")
parser.add_argument("-e", "--enter", help="only run Ansible play no clean up, used for debugging",
                    action="store_true")
parser.add_argument("-x", "--cleanup", help="stop and remove the test container",
                    action="store_true")
parser.add_argument("-p", "--play", help="specify non default play, default: play/site.yml")
parser.add_argument("-v", "--verbose", help="ansible verbose mode, multiple allowed: -vvv",
                   action="count")
args = parser.parse_args()

distro = "ubuntu"
container_name = "test-ansible-container-" + distro
docker_repo = "local-ansible-test:" + distro

if not args.cleanup:
    subprocess.call(["docker", "build", "-t", docker_repo,  "docker/" + distro])
    subprocess.call(["docker", "run", "-ti", "--privileged",  "--name", container_name, "-d", "-p", "5022:22", docker_repo])
    if args.play:
        play = args.play
    else:
        play = "plays/site.yml"
    ansible_cmd = ["ansible-playbook", "-i", "inventories/localdocker", play]
    if args.verbose:
        verbose = "-" + "v" * args.verbose
        ansible_cmd.append(verbose)
        print("verbose " + verbose)
    print("cmd" + str(ansible_cmd))

    subprocess.call(ansible_cmd)

if not args.enter:
    subprocess.call(["docker", "stop", container_name])
    subprocess.call(["docker", "rm",  container_name])
