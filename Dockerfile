FROM python:3-alpine

WORKDIR tgtg
COPY requirements.txt ./
RUN apk add --no-cache tzdata && cp -r -f /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN ["chmod", "a+x", "bot/docker_entrypoint.sh"]
RUN ["chmod", "a+x", "bot/configure_db.py"]
RUN ["chmod", "a+x", "bot/schedule.py"]
RUN ["chmod", "a+x", "bot/telegram_bot_functionality.py"]
RUN ["chmod", "a+x", "bot/TGTG_framework.py"]

RUN ["python3", "bot/configure_db.py"]
CMD  ["sh","bot/docker_entrypoint.sh"]
