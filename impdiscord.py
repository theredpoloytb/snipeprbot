import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive

# Chargement du token depuis le fichier .env
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Intents nécessaires
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Création du bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Commande ping
@bot.command()
async def ping(ctx):
    """Répond avec Pong et la latence en millisecondes"""
    latency = round(bot.latency * 1000)  # Latence du bot en millisecondes
    await ctx.send(f'Pong! Latence : {latency}ms')

# Commande say
@bot.command()
async def say(ctx, *, message):
    """Répète le message fourni par l'utilisateur"""
    await ctx.send(message)

# Commande userinfo
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    """Affiche les informations d'un utilisateur"""
    if member is None:
        member = ctx.author  # Si aucun utilisateur n'est mentionné, prend l'auteur de la commande
    embed = discord.Embed(title=f"Info de {member.display_name}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Nom", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=member.status, inline=True)
    embed.add_field(name="Compte créé le", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="A rejoint le serveur le", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    
    await ctx.send(embed=embed)

# Commande poll
@bot.command()
async def poll(ctx, *, question):
    """Crée un sondage avec deux réactions (👍 et 👎)"""
    embed = discord.Embed(title="Sondage", description=question, color=discord.Color.green())
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')

# Commande clear (réservée aux admins)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Supprime un nombre spécifié de messages dans le salon (réservé aux admins)"""
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages ont été supprimés.', delete_after=5)

# Gérer les erreurs si l'utilisateur n'a pas les permissions requises
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas la permission de supprimer des messages.")

# Commande kick (réservée aux admins)
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Expulse un membre du serveur (réservé aux admins)"""
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} a été expulsé(e) du serveur. Raison: {reason}')

# Commande ban (réservée aux admins)
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bannit un membre du serveur (réservé aux admins)"""
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} a été banni(e) du serveur. Raison: {reason}')

# Commande help personnalisée
@bot.command()
async def help(ctx):
    """Affiche toutes les commandes disponibles"""
    embed = discord.Embed(title="Commandes disponibles", color=discord.Color.blue())
    
    for command in bot.commands:
        # Si la commande est utilisable par l'utilisateur, on l'ajoute à l'aide
        if await command.can_run(ctx):
            embed.add_field(name=f"!{command.name}", value=command.help, inline=False)

    await ctx.send(embed=embed)

# Lancement du bot
keep_alive()
bot.run(TOKEN)
