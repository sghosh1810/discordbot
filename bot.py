import discord
import youtube_dl
import json
import os
import random
from discord import user
from discord import client
from discord.ext import commands
from discord.ext.commands import errors
from ctypes.util import find_library
from discord import opus
from itertools import cycle
import nacl
import asyncio
from PIL import Image, ImageDraw, ImageFont

players = {}


newUserMessage = """ Welcome to MaMa Gang :grin:
Please read the rules and enjoy your stay.
Read rules by typing !mg rules in commands channel.
"""


bot = commands.Bot(command_prefix='!mg ')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='!mg list'))
    print("Bot online. Client ID: " + str(bot.user.id))


@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await member.send(newUserMessage)
    role = discord.utils.get(member.guild.roles, name="MINI MAMA")
    print(role)
    await member.add_roles(member, role)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    with open('users.json', 'r') as f:
        users = json.load(f)
        if(message.author != bot.user):
            await update_data(users, message.author)
            await add_experience(users, message.author, 5)
            await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(":ping_pong: Pong")
    print("Pong")


@bot.command(pass_context=True)
async def hello(ctx):
    response = ['Hey there', 'Hi there', 'Yo ho', 'Taijobuka', 'Meh,', 'Hello']
    emoji = [':eyes:', ':ok_hand:', ':yum:', ':sunglasses:', ':robot:']
    str_authName = str(ctx.message.author)
    printName = str_authName.split('#', 1)[0]
    await ctx.send(random.choice(response)+" {} ".format(printName)+random.choice(emoji))


@bot.command(pass_context=True)
async def about(ctx):
    embed = discord.Embed(title="Version: 3.0.1".format(),
                          description="Made by Duxorhell", color=0x00ff00)
    await ctx.send(embed=embed)
    print("Called about fn")


@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name),
                          description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)
    print("Called info fn  for user:{}.".format(user.name))


@info.error
async def clear_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Invlaid Username")


@bot.command(pass_context=True)
async def stalk(ctx, message, user: discord.Member):
    try:
        print(str(ctx.message.author)+" sent "+str(user.name)+" "+str(message))
        await user.send(str(message))
    except Exception as e:
        await ctx.send("Invalid username. Make sure youre using @username")


@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.guild.name),
                          description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="SERVER INFO XD")
    embed.add_field(name="Name", value=ctx.guild.name, inline=True)
    embed.add_field(name="ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.guild.members), inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)
    print("Called serverinfo fn")


@bot.command(pass_context=True)
async def list(ctx):
    embed = discord.Embed(title="List of Commands", description="-_______-", color=0x00ff00)
    embed.add_field(name="-", value='!mg ping = pong', inline=False)
    embed.add_field(name="-", value='!mg about = Gives Bot info', inline=False)
    embed.add_field(name="-", value='!mg info @username = Gives info about the user', inline=False)
    embed.add_field(name="-", value='!mg serverinfo = Gives server info dude!', inline=False)
    embed.add_field(name="-", value='!mg hello = Try karle be khud', inline=False)
    embed.add_field(
        name="-", value='!mg play <youtube url> = Plays the audio from youtube url', inline=False)
    embed.add_field(name="_", value='!mg gen "Your  text" = Generates image with text', inline=False)
    embed.add_field(
        name="_", value='!mg stalk "Your text" @username = Sends "your text" to @username', inline=False)
    embed.add_field(name="_", value="!mg meme = Sends meme", inline=False)
    await ctx.send(embed=embed)
    print("Called list fn")


@bot.command(pass_context=True)
@commands.has_role("GOD MAMA")
async def kick(ctx, user: discord.Member):
    await ctx.send(":boot: Cya, {}. Ya loser!".format(user.name))
    await ctx.kick(user)


@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    if voice_client:
        await voice_client.disconnect()
        print("Bot left the voice channel")
    else:
        print("Bot was not in channel")


@bot.command(pass_context=True)
async def play(ctx, url):
    opus_path = find_library('opus')
    discord.opus.load_opus(opus_path)
    if not opus.is_loaded():
        print('Opus was not loaded')
    else:
        channel = ctx.message.author.voice.voice_channel
        await bot.join_voice_channel(channel)
        server = ctx.message.server
        voice_client = bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()


@bot.command(pass_context=True)
async def meme(ctx):
    await ctx.send_file(ctx.message.channel, 'sarcastic-meme-5.jpg')


async def update_data(users, user):
    if user.id not in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1


async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp


async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await ctx.send(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end


@bot.command(pass_context=True)
async def gen(ctx, message):
    image = Image.open('background.jpg')
    max_length, max_bredth = 2550, 1440
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('HelveticaNeueMedium.ttf', size=100)
    w, h = draw.textsize(message)
    color = 'rgb(255,255,255)'
    draw.text(((max_length-w)/2, (max_bredth-h)/2), message, fill=color, font=font)
    image.save('opt.png', optimize=True, quality=10)
    await ctx.channel.send(file=discord.File('opt.png'))


async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You dont have that permission mate!")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No such command found!")
    raise error

bot.run("TOKEN")
