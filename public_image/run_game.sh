#!/bin/bash

set -u
set -e

python get_bot_names.py
chmod +x command.sh
./command.sh
cp ./replay.* bots/