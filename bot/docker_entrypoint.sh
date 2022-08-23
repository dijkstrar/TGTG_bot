#!/bin/bash

set -e

exec python3 configure_db.py &
exec python3 schedule.py &
exec python3 telegram_bot_functionality.py &

echo "Succesful startup! :)"
