import discord

client = discord.Client()


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$'):
        command = message.content[1:]

        if command :
            type = command.split()[0]

            if type == "hello" :
                await message.channel.send("Hello World!")

            else :
                await message.channel.send("Command not found, try $help for a list of commands!")



TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
