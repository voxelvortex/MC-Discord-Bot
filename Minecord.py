import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='mc.')
extensions = ["MCCommands"]


@bot.event
async def on_ready():
    print("Ready!")

    # say bot is playing minecraft
    game = discord.Game("Minecraft")
    await bot.change_presence(activity=game)

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
