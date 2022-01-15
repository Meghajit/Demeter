#!/bin/bash

flask run --port=5000 --host=0.0.0.0 &
P1=$!
httpd-foreground &
P2=$!
wait $P1 $P2