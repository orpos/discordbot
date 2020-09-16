import discord
import random
from discord.ext import commands
from time import sleep

def is_it_me(ctx):
    return ctx.author.id == 612364426284105728

def is_it_friend(ctx):
    return ctx.author.id == 598211043575201822

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('bot on')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Eu n tenho permissão para esse comando')
# administration
@client.command()
async def status(ctx,atividade,*,statuss):
    await client.change_presence(status=statuss,activity=discord.Game(str(atividade)))

@client.command()
@commands.check(is_it_me)
async def restart(ctx):
    await client.change_presence(status=discord.Status.online,activity=discord.Game('Reiniciando o bot'))
    for a in range(0,5):
        await client.change_presence(status=discord.Status.online,activity=discord.Game(f'Reiniciando o bot em {a}'))
        sleep(1)
    await client.change_presence(status=discord.Status.online,activity=discord.Game(f'Bot reiniciado'))
    exit(0)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, *,number):
    await ctx.channel.purge(limit=int(number))
    await ctx.send('Mensagens limpas com sucesso :D')
    sleep(2)
    await ctx.channel.purge()

@client.command()
async def kick(ctx, member : discord.Member, *, reason= None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason= None):
    await member.ban(reason=reason)
    await ctx.send(f'Usuario @{member.mention}')

@client.command()
async def unban(ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name,user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Usuario @{user.name}#{user.discriminator}')

@client.command()
@commands.check(is_it_friend)
async def say(ctx,*,text):
    await ctx.send(text)

#games :D
@client.command(alliases=['8ball','eightball'])
async def _8ball(ctx, *,question):
    responses = ['It is certain.',
            'It is decidedly so',
            'Without a doubt',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good',
            'Very doubtful']
    await ctx.send(f'Question: {question}\nAnswer: {random.choices(responses)}')

@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Por favor escolha um tanto de mensagens que deseja apagar')

client.run('NzU0NTM2NDg5NjI2NTAxMTYx.X12K3Q.NqL7lWrUuGo8rggWaE0OkrHFeGE')
