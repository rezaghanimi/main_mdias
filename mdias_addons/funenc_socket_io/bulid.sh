#!/usr/bin/env bash

docker pull registry.cn-hangzhou.aliyuncs.com/odoomaster/super_odoo12_docker:v1
echo "docker socket-io bulid";
docker build -t registry.cn-hangzhou.aliyuncs.com/odoomaster/funenc-socket-io  -f DockerfileIO --no-cache .
docker push registry.cn-hangzhou.aliyuncs.com/odoomaster/funenc-socket-io
curl 'https://cs.console.aliyun.com/hook/trigger?token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVzdGVySWQiOiJjOWJkYTMxNDc5YzY0NGI2NGI1YzIwNDY0YTU5MmYxNTQiLCJpZCI6IjUwODc1In0.b66-CKfotj6CYtHsI0m2EAhg4pqv1R1OoAs32EryQYVtPLq2dyl0gJxE-oeHcSeXb4p4JihU8W3Wal-KfRWAH8katS8FXgIoFHKbDoe6YuSnh_lPwwOIUSM9anXYKtfoGhywbaKXeqgAvJBk8cIt0ErA3_JqBlTN_tBeRBySHFQ'
