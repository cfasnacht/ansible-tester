#!/bin/bash

DISTRO=ubuntu
DOCKER_CONTAINER_NAME="test-ansible-container-$DISTRO"
DOCKER_REPOSITORY="local-ansible-test:$DISTRO"

docker build -t $DOCKER_REPOSITORY docker/$DISTRO
docker run -ti --privileged --name $DOCKER_CONTAINER_NAME -d -p 5022:22 $DOCKER_REPOSITORY
ansible-playbook -i inventories/localdocker plays/site.yml --diff -vvv
docker stop $DOCKER_CONTAINER_NAME
docker rm $DOCKER_CONTAINER_NAME
