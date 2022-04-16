#!/bin/bash

python get_bot_names.py
chmod +x command.sh
./command.sh
cp bots/replay.* ./