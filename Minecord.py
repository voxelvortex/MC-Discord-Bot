import discord
from discord.ext import commands
import json
import datetime

bot = commands.Bot(command_prefix='mc.')
extensions = ["MCCommands"]


@bot.event
async def on_ready():
    print("Ready!")

    # say bot is playing minecraft
    game = discord.Game("Minecraft")
    await bot.change_presence(activity=game)


@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Unfortunately, an error occured...", colour=discord.Colour(0xd0021b),
                          description="```python\n{0}```".format(error), timestamp=datetime.datetime.
                          utcfromtimestamp(1555552142))

    await ctx.send(embed=embed)

if __name__ == "__main__":
    # define bot secrets
    secrets = json.loads("{}")
    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    # load extensions
    for extension in extensions:
        bot.load_extension(extension)

    # start bot using token from secrets
    bot.run(secrets["token"], reconnect=True)
