# TGTG_bot
This repository lists all relevant code in order to host your own TGTG_bot. Registration is performed by using a user's email. Every 60 seconds the bot checks their favourite offers. If a new offer is available, the user is immediately notified!

The bot itself runs in a docker container, but communication is performed by means of a telegram bot.
Setting up a Telegram bot is thus required!

When setting up a Telegram bot, the following commands must be registered:
``` 
/up # users can check if the bot is still checking their offers on demand.
/register # users can register with their email to get offers
/deregister # users can deregister, meaning they won't get notifications.
```

#### Try it out
```bash
# Get repo
git clone https://github.com/shipping-docker/dockerized-app.git
cd TGTG_bot
```

```bash
#create an .env file
sudo touch .env
sudo nano .env

#enter your key:
TELEGRAM_TOKEN=...
```

Finally you can compose the docker container
```bash
docker-compose up -d
```