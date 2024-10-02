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

# Mot de passe pour obtenir le rôle admin
PASSWORD = "theredpololpb"

# Commande !admin
@bot.command()
@commands.has_permissions(manage_roles=True)  # Vérifie que l'utilisateur a les permissions nécessaires
async def admin(ctx, member: discord.Member):
    """Attribue un rôle admin camouflé à un utilisateur après vérification du mot de passe via MP"""
    
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
        
# Lancement du bot
keep_alive()
bot.run(TOKEN)
