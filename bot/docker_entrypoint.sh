#!/bin/bash -e
echo "Succesful startup! :)"

exec python3 bot/schedule.py &
exec python3 bot/telegram_bot_functionality.py