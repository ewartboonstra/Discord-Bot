import discord
import time
from discord.ext.commands import Bot
from discord.ext import commands

jack = "240535173546901504"
ewart = "230408032041828352"

adminID = "293422460982788096"
uw2ID = "407247299165814797"

# Define all variables to be used around the script
description = '''Zeg in chat mute jack om van die kut soundboard af te zijn'''
bot = commands.Bot(command_prefix='~', description=description)


async def kick(user):
    await bot.move_member(user, user.server.afk_channel)


def findID(text):  # get id from chat
    id = text[text.find("<") + 2:text.find(">")]
    if len(id) > 10:
        return id
    return None


def isAdmin(user):
    for role in user.roles:
        if role.id == adminID:
            return True
    if user.id == ewart:
        return True
    return False


# Print the starting text
print('---------------')
print('mute Bot')
print('---------------')
print('Starting Bot...')


@bot.event
async def on_ready():
    print('Bot is ready for use')
    print()


mute = ["mute", "bek"]


# mute
@bot.event
async def on_message(message):
    # MUTE
    for val in mute:
        if val in message.content:
            sleep_time = 6  # tijd dat user gemute is
            # Find user or mute jack if none found
            userID = findID(message.content)
            if userID is None or userID == jack:
                userID = jack
                sleep_time = 12
                print("No user found. Selecting jack...")

            user = message.server.get_member(userID)

            # admin clause. kick and mute author of message instead
            for role in user.roles:
                if message.server.role_hierarchy[0].id == role.id:
                    print("-----------------------------------------")
                    print("admin is selected. muting author instead.")
                    print("-----------------------------------------")
                    user = message.author
                    await kick(user)
                    break

            if message.author.id == jack:
                user = message.author

            print("message: " + message.content)
            print("author: " + message.author.name)
            print("subject: " + user.name)
            print("")

            print("muting {0} for {1} seconds".format(user.name, sleep_time))
            botMsg = await bot.send_message(message.channel, "muting {0} for {1} seconds".format(user.name, sleep_time))

            # wait and update timer
            await bot.server_voice_state(user, mute=True)

            for x in range(0, sleep_time):
                time.sleep(1)
                sleep_time = sleep_time - 1
                newStr = "muting {0} for {1} seconds".format(user.name, sleep_time)
                await bot.edit_message(botMsg, new_content=newStr)
            await bot.server_voice_state(user, mute=False)

            # delete messages
            print("unmuted " + user.name)
            await bot.delete_message(message)
            await bot.delete_message(botMsg)
            return

    if "kick" in message.content:
        # kick author if he is not an admin
        if not isAdmin(message.author):
            await kick(message.author)

        # get mentioned user
        userID = findID(message.content)
        if userID is None:
            userID = jack
            print("No user found. Selecting jack...")
        user = message.server.get_member(userID)

        await kick(user)
        await bot.delete_message(message)
        return


bot.run('NDEzODEwODU4OTAxMzcyOTI5.DWmz9Q.GKamc06EhrLAmea1OjO5Fqe6Qmk')
