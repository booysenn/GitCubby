#!/bin/bash

docker stop git-cubby-test > /dev/null 2>&1
docker rm git-cubby-test > /dev/null 2>&1

docker build -t git-cubby-test .
docker run -v /config/git/keys:/keys:ro --env-file test.env \
 --name git-cubby-test  -d -p 2222:22 -p 9980:9980 \
 git-cubby-test 

docker logs -f git-cubby-test