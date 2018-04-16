import time
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


def find_id(text):  # get id from chat
    user_id = text[text.find("<") + 2:text.find(">")]
    if len(user_id) > 10:
        return id
    # Select jack if no id is given
    user_id = jack
    print_with_time("No user found. Selecting jack...")
    return user_id


def is_admin(user):
    for role in user.roles:
        if role.id == adminID:
            return True
    if user.id == ewart:
        return True
    return False


def print_with_time(msg):
    print('{0}: {1}'.format(time.strftime('%X'), msg))


# Print the starting text
print('---------------')
print('Jack bot')
print('---------------')
print_with_time('Starting Jackbot...')


@bot.event
async def on_ready():
    print_with_time('Jackbot is ready')
    print()


mute = ["!mute", "!bek"]

# second word to keep jack quiet
trigger_list = ["bek", "muil", "smoel", "hoofd", "klep", "kleppekop", "kop", "snavel"]


async def mute_with_timer(user, sleep_time, message):
    print_with_time("Muting {0} for {1} seconds".format(user.name, sleep_time))
    bot_msg = await bot.send_message(message.channel, "muting {0} for {1} seconds".format(user.name, sleep_time))

    # wait and update timer
    await bot.server_voice_state(user, mute=True)

    for x in range(0, sleep_time):
        time.sleep(1)
        sleep_time = sleep_time - 1
        new_string = "Muting {0} for {1} seconds".format(user.name, sleep_time)
        await bot.edit_message(bot_msg, new_content=new_string)
    await bot.server_voice_state(user, mute=False)

    # delete messages
    print_with_time("Un-muted " + user.name)
    await bot.delete_message(message)
    await bot.delete_message(bot_msg)


# mute
@bot.event
async def on_message(message):
    # MUTE
    for val in mute:
        if val in message.content:
            sleep_time = 6  # tijd dat user gemute is
            # Find user or mute jack if none found
            user_id = find_id(message.content)
            user = message.server.get_member(user_id)

            # admin clause. kick and mute author of message instead
            for role in user.roles:
                if message.server.role_hierarchy[0].id == role.id:
                    print_with_time("admin is selected. muting author instead.")
                    user = message.author
                    await kick(user)
                    break

            if message.author.id == jack:
                user = message.author
            await mute_with_timer(user, sleep_time, message)
            return

    if "!kick" in message.content:
        # kick author if he is not an admin
        if not is_admin(message.author):
            await kick(message.author)

        # get mentioned user
        user_id = find_id(message.content)
        user = message.server.get_member(user_id)

        await kick(user)
        await bot.delete_message(message)
        return
    if "jack" in message.content.lower():
        for val in trigger_list:
            if val in message.content.lower():
                user = message.server.get_member(jack)
                await mute_with_timer(user, 10, message)
        return
    if "!ping" in message.content:
        print_with_time("ping")
        # You say ping
        pong_msg = await bot.send_message(message.channel, "pong")
        # I say pong
        time.sleep(2)
        await bot.delete_message(message)
        await bot.delete_message(pong_msg)
        print_with_time("pong")
        return


bot.run('NDEzODEwODU4OTAxMzcyOTI5.DWmz9Q.GKamc06EhrLAmea1OjO5Fqe6Qmk')
