
# Reactify

Reactify reactifies images - this Discord bot converts a given image into a series of messages with reactions attached to them, recreating the image!


## Usage

Invite the bot [here](https://discordapp.com/api/oauth2/authorize?client_id=593314917499535363&permissions=1074080832&scope=bot)

If you want to host it on your own, clone the repo, make your pipenv, and pip install -r requirements.txt, insert your token, and enjoy!

Make sure you have a fresh(ish) server for the emoji creation, and put that as the EMOJI_SERVER_ID - otherwise, the rate limit for emojis will prevent the image from being created

## How It Works

The bot first breaks up the image into chunks, reads the average RGB value of the chunk, then creates a custom emoji in a server to represent that chunk. Then, the bot reacts to its message with that custom emote, and this process then repeats until the full image is "rendered" as reactions.

Example of this process working:
![](example.png)

This process tends to work the best with extremely pixel size images - otherwise, Discord limits prevent more emojis from being added.



## Contributing

This was written quickly and badly - I'll be open to any pulls, if there is any interest.

Created by Vex#9042

:)
