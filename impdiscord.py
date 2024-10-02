import os
import discord
import re
import asyncio
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

# Mot de passe pour obtenir le rôle admin
PASSWORD = "theredpololpb"

# Fonction pour détecter les messages avec les abréviations de "quoi"
@bot.event
async def on_message(message):
    # Empêche le bot de répondre à ses propres messages
    if message.author == bot.user:
        return

    # Vérifie si le message contient une variation ou abréviation de "quoi"
    if re.search(r'(pk|pq|qwa|koi|quoi|qoi|qouwa|kouwa|kwa|koa|koua|pkoi|pquoi)', message.content, re.IGNORECASE):
        # Répond avec "feur" et plein d'emojis goofy
        await message.channel.send("feur 🤪🤣😂🙃😛")

    # Nécessaire pour que les autres commandes fonctionnent toujours
    await bot.process_commands(message)

# Commande !admin
@bot.command()
async def admin(ctx, member: discord.Member):
    """Attribue un rôle admin camouflé à un utilisateur après vérification du mot de passe via MP"""
    
    # Vérification que l'exécutant de la commande a la permission de gérer les rôles
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("Désolé, tu n'as pas la permission de donner des rôles administrateurs.")
        return
    
    # Demander le mot de passe en MP
    await ctx.author.send("Veuillez entrer le mot de passe pour attribuer le rôle admin à cet utilisateur.")

    def check(msg):
        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

    try:
        # Attendre la réponse en DM
        msg = await bot.wait_for('message', check=check, timeout=60.0)
        
        # Vérification du mot de passe
        if msg.content == PASSWORD:
            # Créer le rôle "admin" camouflé si il n'existe pas
            guild = ctx.guild
            role_name = "Admin camouflé"
            role = discord.utils.get(guild.roles, name=role_name)
            
            if not role:
                role = await guild.create_role(name=role_name, color=discord.Color(0x2C2F33), hoist=False, mentionable=False)
                await ctx.send(f"Rôle {role_name} créé avec succès.")

            # Attribution du rôle à l'utilisateur
            await member.add_roles(role)
            await ctx.send(f"Le rôle {role_name} a été attribué à {member.mention}.")
            await member.send(f"Tu as été attribué(e) au rôle {role_name} sur {guild.name}.")

        else:
            await ctx.author.send("Mot de passe incorrect. Aucune action effectuée.")
    except asyncio.TimeoutError:
        await ctx.author.send("Temps écoulé. Aucune action effectuée.")

# Commandes classiques (comme avant)
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
@bot.command(name="aide")
async def myhelp(ctx):
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
