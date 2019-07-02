import discord
import urllib.request
from PIL import Image
import os


resolution = 20
client = discord.Client()
processing = False

@client.event
async def on_message(message):
    global processing, resolution

    if message.author == client.user:
        return


    # Change ! to whatever prefix you want the bot to respond to
    if message.content.startswith('!'):
        command = message.content[1:]

        if command :
            type = command.split()[0]

            if type == "help" :
                await message.channel.send(
                """
                **Use reactify to create images out of Discord reactions! Do !reactify with your image attached to begin the process!**
                **!reactify** - reactifies the attached image
                **!res [new resolution]** - changes the resolution of !reactify (call with no arguments for more details)
                """)


            elif type == "res" :
                if len(command.split()) > 1 :
                    new_res = command.split()[1]
                    try :
                        new_res = int(new_res)
                    except ValueError :
                        await message.channel.send("**Please enter a number to change the resolution (!res [new resolution])**")
                    else :
                        if new_res > 20 or new_res < 1 :
                            await message.channel.send("**Please enter a number between 1 and 20**")

                        else :
                            resolution = new_res
                            await message.channel.send("**Resolution successfully changed to " + str(resolution) + "!**")


                else :
                    await message.channel.send("**The 'resolution' of a reactified image is limited by the maximum number of reactions that can be on a single message (20). If you wish to change the resolution, note that your image will be smaller and more inaccurate. You can do this by doing !res [new resolution].**")


            elif type == "reactify" :
                if processing :
                    await message.channel.send("**Reactify is currently prcoessing an image, please wait until it is finished!")

                elif message.attachments :
                    processing = True

                    url = message.attachments[0].url
                    img_name = message.attachments[0].filename

                    path = "./image/" + img_name

                    # Download the image onto server
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(url, path)

                    image = Image.open(path)

                    width, height = image.size
                    rgb_im = image.convert('RGB')


                    emoji_server = await client.create_guild("Emoji Storage")
                    emojis_created = 0


                    # Split into boxes
                    # Each square is scaleX width and scaleY height

                    scaleX = int(width / resolution)
                    scaleY = int(height / resolution)

                    for row in range(resolution) :
                        msg = await message.channel.send(row)

                        for column in range(resolution) :
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
                            custom_color.save('custom.png')

                            if emojis_created >= 50 :
                                await emoji_server.delete()
                                emoji_server = await client.create_guild("Emoji Storage")

                            with open("custom.png", 'rb') as custom:
                                c = await emoji_server.create_custom_emoji(name="custom" + str(column), image=custom.read())
                                emojis_created += 1
                                await msg.add_reaction(c)


                            os.remove("./custom.png")

                            #await message.channel.send(str(aR) + " " + str(aG) + " " + str(aB))

                    os.remove(path)
                    processing = False



                else :
                    await message.channel.send("Please attach an image to your message!")


            else :
                await message.channel.send("Command not found, try $help!")



TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
