import discord
from discord.ext import commands
import datetime
from MC import Server
import json


class MCCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("servers.json","r") as file:
            self.servers = json.load(file)

    @commands.command(name="status", aliases=["serverstatus", "server_status", "stat", "serverstat", "server_stat"],
                      pass_conext=True, help="Returns information about a server given its ip and port")
    async def server_status(self, ctx, ip: str, port: int = 25565):
        await ctx.trigger_typing()
        server = Server(ip, port)
        data = server.get_json_data()
        # Create and send an embed
        embed = self.make_embed(data, ip, port)

        await ctx.send(embed=embed)

    @commands.command(name="ip", aliases=["server", "serverip", "server_ip"], pass_context=True,
                      help="Returns a server's ip given a keyword")
    async def ip(self, ctx, *args):
        await ctx.trigger_typing()
        for server in self.servers["list"]:
            for arg in args:
                if arg in server["keywords"]:
                    if ctx.message.channel.id in server["auth_channel_ids"] or\
                            ctx.message.guild.id in server["auth_server_ids"]:

                        obj = Server(server["ip"], server["port"])
                        data = obj.get_json_data()
                        embed = self.make_embed(data, server["ip"], server["port"])
                        await ctx.send(embed=embed)
                        return

        embed = discord.Embed(title="Error: The server you searched for could not be found.",
                              colour=discord.Colour(0xff0000),
                              description=
                              "Please verify you are in a channel with authority to search for the given server")

        await ctx.send(embed=embed)

    @commands.command(name="ping", aliases=["getping", "get_ping", "getserverping", "get_server_ping"],
                      pass_context=True, help="Gets ping of the discord bot to discord, or a given ip")
    async def ping(self, ctx, ip: str="discordapp.com"):
        await ctx.trigger_typing()
        server = Server(ip)
        ping = server.get_ping()

        embed = discord.Embed(title="Pinging {0}".format(ip), colour=discord.Colour(0xf8e71c),
                              description="{0}".format(ping),
                              timestamp=datetime.datetime.utcfromtimestamp(1555527735))

        await ctx.send(embed=embed)

    def make_embed(self, data, ip, port=25565):
        online = "Currently offline"
        color = discord.Colour(0xff0000)
        if data["online"]:
            online = "Currently online"
            color = discord.Colour(0x406d20)

        embed = discord.Embed(title="{0}".format(data["motd"]), colour=color
                              , description="{0}\nVersion: {1} ".format(online, data["server"]["name"]))
        embed.set_author(name="{0}:{1}".format(ip, port))
        embed.set_footer(text="{0}/{1}".format(data["players"]["now"], data["players"]["max"]),
                         icon_url="https://images-na.ssl-images-amazon.com/images/I/512dVKB22QL.png")
        return embed


def setup(bot):
    bot.add_cog(MCCommands(bot))
