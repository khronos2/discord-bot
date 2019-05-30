import discord
from discord.utils import get
import random
import time

#Pre-login vars
client = discord.Client()
game = discord.Activity(type=discord.ActivityType.watching, name="How to Become Self-Aware")

#login and status set.
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=game)

#vars for dice roll
min = 1
max = 100
dice_roll = random.randint(min, max)


def flip():
    min = 1
    max = 2
    roll_result = random.randint(min, max)
    if roll_result == 1:
        flip.heads += 1
        return "Heads"
    else:
        flip.tails += 1
        return "Tails"

flip.heads = 0
flip.tails = 0

#help system
help_messages = """
```
Welcome to help menu for this bot!

The following functions are available:
/help or help: This menu
/hello: Well... the bot says hello!
/roll: Rolls dice for a random int between 1-100.
/addrole: Adds a user to a specified role. An example of this: /addrole Username Rolename
/coin: Flip a coin!
/cc: Coin Counter! Displays Heads/Tails occurences. 
```
"""

#messaging system
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/hello'):
        await message.channel.send('Why, hello there!')

    if message.content.startswith('help'):
        await message.channel.send(help_messages)
    
    if message.content.startswith('/help'):
        await message.channel.send(help_messages)

    if message.content.startswith('/coin'):
        await message.channel.send(flip())

    if message.content.startswith('/cc'):
        await message.channel.send("Heads: " + str(flip.heads))
        await message.channel.send("Tails: " + str(flip.tails))

    if message.content.startswith('/roll'):
        await message.channel.send('Rolling the dice...')
        time.sleep(2)
        await message.channel.send(dice_roll)

    if message.content.startswith('/addrole'):
        role_list = ["Bad_Bot", "Dumb_Bot", "Crazy_Bot"]
        entered_role = message.content[9:]
        role = discord.utils.get(message.guild.roles, name=entered_role)
        member = message.author
        roles = [
        # Role IDs
        #"581579864620924931",
        #"582957201258184715",
        #"582972597902245909",
        ]
        for r in message.author.roles:
            if r.id in roles:
                # If a role in the user's list of roles matches one of those we're checking
                await message.channel.send("You already have that role!")
                return
        if role is None or role.name not in role_list:
            await message.channel.send( "That role does not exist!")
            return
        elif role in message.author.roles:
            # If they already have the role
            await message.channel.send("You already have this role.")
        else:
            try:
                await member.add_roles(role)
                await message.channel.send("Successfully added role {0}".format(role.name))
            except discord.Forbidden:
                await message.channel.send("Invalid permissions")

#client.run(TOKEN_HERE)