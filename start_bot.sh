#!/bin/bash -e

python3 schedule.py &
python3 telegram_bot_functionality.py &
