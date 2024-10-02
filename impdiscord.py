import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Configuration des intents (permissions) nécessaires
intents = discord.Intents.default()
intents.guilds = True  # Pour pouvoir gérer les serveurs (guilds)

# Création du bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Événement déclenché lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt et connecté !")

# Lancement du bot
bot.run(TOKEN)
