# TGTG_bot
This repository lists all relevant code in order to host your own TGTG_bot. 


## Usage
`TGTG_bot` observes your favorite TGTG Magic Bags for new available items and notifies you via Telegram. Notifications will be send when Magic Bags become available. This software is provided as is without warranty of any kind. If you have problems, find bugs or have suggestions for improvement feel free to create an issue or contribute to the project.

When the bot is started it will run idle. The bot must be contacted (example: https://t.me/TGTG_checker_bot) and the user must be registered by using `/register`. Similar to loging in to the TGTG app, you have to click on the link send to you by mail. **This won't work on your mobile phone if you have installed the TGTG app, so you have to check your mailbox on PC.** After a successfull login the bot will commence scanning. If you don't receive notifications, you can consider checking the bot with the `/up` command. The bot will check your enrollment, and will display how many favorite stores have offers available!

<p style="text-align:center;"><img src="data/profile_pic.png" width="300" class="center"></p>

## Available Commands
``` 
/up # users can check if the bot is still checking their offers on demand.
/register # users can register with their email to get offers
/deregister # users can deregister, meaning they won't get notifications.
```
Unknown commands or non-commands will be ignored, and the user is notified correspondingly!

## Telegram Requirements
The bot itself runs in a docker container, but communication is performed by means of a telegram bot.
Setting up a Telegram bot is thus required! Please consult https://core.telegram.org/Bots for more information on setting up a bot! When setting up a Telegram bot, the previously listed commands must be registered at the bot!


## Try it out
```bash
# Get repo
git clone https://github.com/dijkstrar/TGTG_bot.git
cd TGTG_bot
```

```bash
#create an .env file
sudo cp env.example .env
sudo nano .env

#enter your key:
TELEGRAM_TOKEN=...
```

Finally you can build and run the docker container
```bash
docker-compose up -d
```

### Troubleshooting RaspberryPi3
In case you encounter request errors (code 443), the DNS configuration inside your docker container must be altered.
One way to do this, would be by inspecting docker's DNS configuration

```
cat /etc/docker/daemon.json
```
Change the fields accordingly:

```
{
    "dns": ["DNS_1", "DNS_2"]
}
```
Docker restart is required:
```
sudo systemctl restart docker
```
