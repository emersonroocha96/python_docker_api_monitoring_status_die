#!/bin/sh
for i in `seq 5`; do docker run -d nginx; done; docker stop `docker ps -q`
