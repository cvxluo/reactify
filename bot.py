import discord

EMOJI_SERVER_ID = 594361190272991234

client = discord.Client()

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('!'):
        command = message.content[1:]

        if command :
            type = command.split()[0]

            if type == "hello" :
                await message.channel.send("Hello World!")


            elif type == "test" :
                emoji_server = client.get_guild(EMOJI_SERVER_ID)
                emojis = emoji_server.emojis

                emoji = "<:" + str(emojis[0].name) + ":" + str(emojis[0].id) + ">"
                await message.channel.send(emoji)

            elif type == "reactify" :
                if message.attachments :
                    url = message.attachments

                    print(url)

                else :
                    await message.channel.send("Please attach an image to your message!")


            else :
                await message.channel.send("Command not found, try $help for a list of commands!")



TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
