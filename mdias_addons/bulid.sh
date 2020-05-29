#!/usr/bin/env bash

docker pull registry.cn-hangzhou.aliyuncs.com/odoomaster/super_odoo12_docker:v1
if [ "$1" "==" "dev" ]
then
  echo "docker dev bulid";
  docker build  -t mdias -f DockerfileDev .
else

  docker login -u wallini@funenc -p lyp3192594 registry.cn-hangzhou.aliyuncs.com
  if [ "$1" "==" "test" ]
  then
      echo "start test compile";
      docker build -t registry.cn-hangzhou.aliyuncs.com/odoomaster/mdias6 -f DockerfileDev .
      docker push registry.cn-hangzhou.aliyuncs.com/odoomaster/mdias6
  elif [ "$1" "==" "socket" ]
  then
      echo "docker socketio bulid";
      docker build -t registry.cn-hangzhou.aliyuncs.com/odoomaster/funenc-socket-io  -f DockerfileIO --no-cache .
      docker push registry.cn-hangzhou.aliyuncs.com/odoomaster/funenc-socket-io

  else
       echo "docker production bulid";
       if [ "$1" "==" "mdias1" ]
       then
            docker build -t registry.cn-hangzhou.aliyuncs.com/odoomaster/mdias  --no-cache .
            docker push registry.cn-hangzhou.aliyuncs.com/odoomaster/mdias
       else
            docker build -t registry.cn-hangzhou.aliyuncs.com/odoomaster/mdias2  --no-cache .
            docker push registry.cn-hangzhou.aliyuncs.com/odoomaster/mdias2
       fi
  fi
fi