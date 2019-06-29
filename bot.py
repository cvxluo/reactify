import discord
import urllib.request
from PIL import Image
import os


EMOJI_SERVER_ID = 594419428628627456
RESOLUTION = 20

client = discord.Client()

@client.event
async def on_message(message):

    if message.author == client.user:
        return


    if message.content.startswith('!'):
        command = message.content[1:]

        if command :
            type = command.split()[0]

            if type == "help" :
                await message.channel.send("Use reactify to create images out of Discord reactions! Do !reactify with your image attached to begin the process!")


            elif type == "reactify" :
                if message.attachments :
                    url = message.attachments[0].url
                    img_name = message.attachments[0].filename

                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(url, "./images/" + img_name)

                    path = "./images/" + img_name
                    image = Image.open(path)

                    width, height = image.size
                    rgb_im = image.convert('RGB')


                    emoji_server = client.get_guild(EMOJI_SERVER_ID)

                    # Split into boxes
                    # Each square is scaleX width and scaleY height

                    scaleX = int(width / RESOLUTION)
                    scaleY = int(height / RESOLUTION)

                    for row in range(RESOLUTION) :
                        msg = await message.channel.send(row)

                        for column in range(RESOLUTION) :
                            # row, column is x, y of box

                            aR, aG, aB = 0, 0, 0

                            for x in range(scaleX) :
                                for y in range(scaleY) :
                                    r, g, b = rgb_im.getpixel((x + column * scaleX, y + row * scaleY))

                                    aR += (r ** 2)
                                    aG += (g ** 2)
                                    aB += (b ** 2)

                            aR /= (scaleX * scaleY)
                            aG /= (scaleX * scaleY)
                            aB /= (scaleX * scaleY)

                            aR = int(aR ** 0.5)
                            aG = int(aG ** 0.5)
                            aB = int(aB ** 0.5)


                            # Now we have the RGB value of the square
                            # We have to create a custom emoji

                            custom_color = Image.new('RGB', (128, 128), color = (aR, aG, aB))

                            with open("custom.png", 'rb') as custom:
                                c = await emoji_server.create_custom_emoji(name="custom" + str(column), image=custom.read())
                                await msg.add_reaction(c)
                                await c.delete()

                            os.remove("./custom.png")

                            #await message.channel.send(str(aR) + " " + str(aG) + " " + str(aB))

                    os.remove(path)



                else :
                    await message.channel.send("Please attach an image to your message!")


            else :
                await message.channel.send("Command not found, try $help!")



TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
