import discord
from discord import user
from discord import client
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

bot = commands.Bot(command_prefix='!mg ')

@bot.event
async def on_ready():
    print("Mama Gang Bot")
    print("I am: "+ bot.user.name)
    print("Client ID: "+ bot.user.id)


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: Pong")
    print("Pong")


@bot.command(pass_context=True)
async def about(ctx):
    embed = discord.Embed(title="Version: 1.0.1".format(), description="Made by Duxorhell", color=0x00ff00)
    await bot.say(embed=embed)
    print("Called about fn")

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)
    print("Called info fn")

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="SERVER INFO XD")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def list(ctx):
    embed = discord.Embed(title="List of Commands".format(), description="-_______-", color=0x00ff00)
    embed.add_field(name="-", value='!mg ping = pong', inline=False)
    embed.add_field(name="-", value='!mg about = Gives Bot info', inline=False)
    embed.add_field(name="-", value='!mg info @username = Gives info about the user', inline=False)
    embed.add_field(name="-", value='!mg serverinfo = Gives server info dude!', inline=False)
    await bot.say(embed=embed)
    print("Called command fn")


@bot.command(pass_context=True)
@commands.has_role("SATAN MAMA")
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Cya, {}. Ya loser!".format(user.name))
    await bot.kick(user)



bot.run("TOKEN")