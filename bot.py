import discord
import asyncio
import urllib.request
from PIL import Image
import os


resolution = 20
client = discord.Client()
processing = False

cleaner_mode = False
image_channel = None


@client.event
async def on_message(message):
    global processing, resolution, cleaner_mode, image_channel
    channel = message.channel

    if channel == image_channel and cleaner_mode and message.author != client.user and processing :
        await message.delete()

    if message.author == client.user:
        return


    # Change ! to whatever prefix you want the bot to respond to
    if message.content.startswith('!'):
        command = message.content[1:]

        if command :
            type = command.split()[0]

            if type == "help" :
                await channel.send(
                """
                **Use reactify to create images out of Discord reactions! Do !reactify with your image attached to begin the process!**
                **!reactify** - reactifies the attached image
                **!res [new resolution]** - changes the resolution of !reactify (call with no arguments for more details)
                **!cleaner** - enable/disable cleaner mode (call with no arguments for more details)
                **!cancel** - cancels reactify process on an image
                """)


            elif type == "res" :
                if len(command.split()) > 1 :
                    new_res = command.split()[1]
                    try :
                        new_res = int(new_res)
                    except ValueError :
                        await channel.send("**Please enter a number to change the resolution (!res [new resolution])**")
                    else :
                        if new_res > 20 or new_res < 1 :
                            await channel.send("**Please enter a number between 1 and 20**")

                        else :
                            resolution = new_res
                            await channel.send("**Resolution successfully changed to " + str(resolution) + "!**")


                else :
                    await channel.send("**The 'resolution' of a reactified image is limited by the maximum number of reactions that can be on a single message (20). If you wish to change the resolution, note that your image will be smaller and more inaccurate. You can do this by doing !res [new resolution].**")


            elif type == "cleaner" :
                await channel.send("**Cleaner mode will delete any messages that might split up a reactifying image - note it also disables canceling**")
                msg = await channel.send("**Enable cleaner mode?**")

                await msg.add_reaction('\U0001f44d')
                await msg.add_reaction('\U0001f44e')

                await asyncio.sleep(1)


                def check (reaction, user) :
                    return reaction.message.id == msg.id

                try :
                    reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)

                except asyncio.TimeoutError :
                    await channel.send("**Timed out :(**")

                else :
                    if reaction.emoji == '\U0001f44d' :
                        cleaner_mode = True
                        await channel.send("**Cleaner mode activated!**")

                    else :
                        cleaner_mode = False
                        await channel.send("**Cleaner mode deactivated!**")


            elif type == "cancel" :
                if processing :
                    await channel.send("**Canceling...**")
                    processing = False

                else :
                    await channel.send("**No image being processed!")




            elif type == "reactify" :
                if processing :
                    await channel.send("**Reactify is currently prcoessing an image, please wait until it is finished!**")

                elif message.attachments or len(command.split()) > 1:
                    image_channel = channel
                    processing = True

                    url = None
                    img_name = None

                    if (message.attachments) :
                        url = message.attachments[0].url
                        img_name = message.attachments[0].filename

                    else :
                        url = str(command.split()[1])
                        img_name = "image.png"



                    path = "./image/" + img_name

                    # Download the image onto the server
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)

                    try :
                        urllib.request.urlretrieve(url, path)

                    except ValueError :
                        await channel.send("**Please enter a valid URL!**")
                        image_channel = None
                        processing = False
                        return


                    image = Image.open(path)

                    width, height = image.size
                    rgb_im = image.convert('RGB')


                    emoji_server = await client.create_guild("Emoji Storage")
                    emojis_created = 0


                    # Split into boxes
                    # Each square is scaleX width and scaleY height

                    aspect_ratio = width / height

                    scaleX = int(width / resolution)
                    scaleY = int(aspect_ratio * scaleX)

                    for row in range(int(height / scaleY)) :
                        msg = await channel.send(row)

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
                            # We have to create a custom emoji and upload it to the server

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


                        # If process is canceled
                        if not processing :
                            os.remove(path)
                            await emoji_server.delete()
                            return


                    os.remove(path)
                    await emoji_server.delete()
                    processing = False



                else :
                    await channel.send("**Please attach an image to your message!**")


            else :
                await channel.send("**Command not found, try !help!**")



TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
