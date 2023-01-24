import discord
import asyncio
import json
from requests import get
from keep_alive import keep_alive
from discord import role
from discord import activity
from discord import mentions
from discord import client
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
import urllib
import os
import random
from discord.ext.commands import bot

TOKEN = os.environ.get('TOKEN')
keep_alive()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=">>", status=discord.Status.online, intents=intents)
bot.remove_command('help')

async def ch_pr():
  await bot.wait_until_ready()

  statuses = ["with hedgehogs | >>help", f"on {len(bot.guilds)} servers! | >>help", f"with {len(bot.users)} users! | >>help", "Numix Programmed me! | >>help"]

  while not bot.is_closed():

    status = random.choice(statuses)

    await bot.change_presence(activity=discord.Game(name=status))

    await asyncio.sleep(5)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is Online")

@bot.event
async def on_member_join(member):
  guild = bot.get_guild(885885805569138778)
  channel = guild.get_channel(885886913213521950)
  await channel.send(f'Welcome to the server {member.mention} !')
  await member.send(f'Welcome to the {guild.name} server, {member.name}!')

@bot.command()
async def nomick(ctx):
  await ctx.send("https://media.discordapp.net/attachments/885885806269562953/931934051055583292/unknown.png")

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help Panel!", description="All avaible commands with the bot.", color=0x42ff8b)
    embed.add_field(name="Server Info", value="Type ``>>serverData`` to get the Server Info.", inline=False)
    embed.add_field(name="User Info", value="Type ``>>data`` to get your own information or, if you want to get another user information, type ``>>data @user``.", inline=False)
    embed.add_field(name="Ping", value="Type ``>>ping`` to get the latency of the message from the bot.", inline=False)
    embed.add_field(name="Random Number generator", value="Type ``>>randomNumber`` to get a random number.", inline=False)
    embed.add_field(name="Avatar", value="Type ``>>getAvatar`` to get your avatar, if you want to get another user avatar, type ``>>getAvatar @user``.", inline=False),
    embed.add_field(name="Meme", value="Type ``>>meme`` to get a meme post!", inline=False)
    embed.add_field(name="Snipe", value="Type ``>>snipe`` to see the recent deleted message in the chat!", inline=False)
    embed.add_field(name="8ball", value="Type ``>>8ball`` to ask a question for the bot...", inline=False)
    embed.add_field(name="lockdown", value="Type ``>>lockdown`` to lock a channel from the server", inline=False)
    embed.add_field(name="unlock", value="Type ``>>unlock`` to unlock the main locked channel", inline=False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Help request by - {ctx.author}')
    await ctx.reply(embed=embed, mention_author=False)

snipe_message_author = {}
snipe_message_content = {}

@bot.event
async def on_message_delete(message):
  snipe_message_author[message.channel.id] = message.author
  snipe_message_content[message.channel.id] = message.content

  await asyncio.sleep(60)

  del snipe_message_author[message.channel.id]
  del snipe_message_content[message.channel.id]

@bot.command()
async def snipe(ctx):
  channel = ctx.channel
  try:
    embed = discord.Embed(
      color = discord.Color.green()
    )
    embed.set_author(name=f"Last deleted message in {ctx.channel.name}")
    embed.add_field(name="Author: ", value=snipe_message_author[channel.id])
    embed.add_field(name="Message: ", value=snipe_message_content[channel.id])
    embed.set_footer(icon_url = ctx.author.avatar_url, text=f"Snipe request by - {ctx.author}")
    await ctx.reply(embed = embed, mention_author=False)
  except:
    await ctx.reply("There are no recent deleted messages!", mention_author=False)

@bot.command()
async def meme(ctx):
  memeApi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')

  memeData = json.load(memeApi)

  memeUrl = memeData['url']
  memeName = memeData['title']
  memePoster = memeData['author']
  memeSub = memeData['subreddit']
  memeLink = memeData['postLink']

  embed = discord.Embed(title=memeName)
  embed.set_image(url=memeUrl)
  embed.set_footer(text=f"Meme by: {memePoster} | Subreddit: {memeSub} | Post: {memeLink}")
  await ctx.send(embed=embed)

@bot.command()
async def randomNumber(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.reply("Type a number", mention_author=False)
    msg1 = await bot.wait_for("message", check=check)
    await ctx.send("Type a second, larger number", mention_author=False)
    msg2 = await bot.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"You got {value}!")
    else:
        await ctx.send("Please, make sure that the first number is smaller than the second number.")

@bot.command()
async def ping(ctx):
    await ctx.reply(f'My ping is {round(bot.latency * 1000)}ms!', mention_author=False)

@bot.command(name="data")
async def data(ctx,user:discord.Member=None):

    if user==None:
        user=ctx.author

    rlist = []
    for role in user.roles:
        rlist.append(role.mention)

    b = ", ".join(rlist)

    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
  icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)

    embed.add_field(name='Created at:',value=user.created_at,inline=False)
    embed.add_field(name='Joined at:',value=user.joined_at,inline=False)


    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)

    await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def getAvatar(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author
  
  memberAvatar = member.avatar_url
  embed = discord.Embed(title = f"{member.name}'s Avatar, download here", url = memberAvatar)
  embed.set_image(url = memberAvatar)

  await ctx.reply(embed = embed, mention_author=False)

@bot.command()
async def serverData(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.green()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=False)
  embed.add_field(name="Server ID", value=id, inline=False)
  embed.add_field(name="Region", value=region, inline=False)
  embed.add_field(name="Member Count", value=memberCount, inline=False)
  embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y  %H:%M:%S'), inline=False) 

  await ctx.reply(embed=embed, mention_author=False)

@bot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
  responses  = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Maybe."]
  await ctx.reply(f':8ball: Answer: {random.choice(responses)}', mention_author=False)

@commands.has_permissions(administrator = True)
@bot.command("delete")
async def sell(ctx, amount : int):
  await ctx.channel.purge(limit=amount+1)
  embed=discord.Embed(description=f"Succefully deleted {amount} message(s) in {ctx.channel}!", color=discord.Colour.green())
  await ctx.send(embed=embed, delete_after=5)

@bot.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
  await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
  embed=discord.Embed(description=f"{ctx.channel} is in lockdown...", color=discord.Colour.red())
  await ctx.send(embed=embed, delete_after=10)

@bot.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
  await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
  embed=discord.Embed(description=f"Succefully unlocked {ctx.channel}!", color=discord.Colour.green())
  await ctx.send(embed=embed, delete_after=10)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Unknown command, if you are having troubles, check ``>>help``", mention_author=False)

bot.loop.create_task(ch_pr()) 
bot.run(TOKEN)