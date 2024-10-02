import discord
from discord.ext import commands
import asyncio

# Ton token ici
TOKEN = 'OTgyMzg4MDk1MjM0MjQ0NjI4.GRpwb9.F474xaAVJX4vRSH2-8w9rVa_le7GgvaUlwCr7I'

# Intents nécessaires
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Ajout de cette ligne pour lire le contenu des messages


# Création du bot
bot = commands.Bot(command_prefix='!', intents=intents)

# ID du canal spécifique où tu veux spammer (remplace-le par l'ID de ton canal)
REVOLUTION_CHANNEL_ID = 770397242300694569  # Remplace par l'ID du canal "révolution"

# Variable pour contrôler le spam
spamming = False

# Commande qui spamme des messages dans le canal "révolution"
@bot.command()
async def revolution(ctx):
    global spamming
    # Récupère le canal où on va spammer
    channel = bot.get_channel(REVOLUTION_CHANNEL_ID)
    
    if channel is None:
        await ctx.send("Le canal 'révolution' n'a pas été trouvé.")
        return
    
    # Liste de messages avec des emojis
    messages = [
        "🔥 Vive la révolution ! 🔥",
        "💥 C'est l'heure du changement ! 💥",
        "⚔️ La liberté ou la mort ! ⚔️",
        "💣 Révolution en cours... 💣",
        "🛡️ Prenez les armes ! 🛡️",
        "🚩 Nous ne nous rendrons jamais ! 🚩"
    ]
    
    # Définir la variable spamming à True pour démarrer la boucle
    spamming = True
    await ctx.send("La révolution commence maintenant ! 🚩")
    
    # Boucle infinie pour spammer tant que spamming est True
    while spamming:
        for message in messages:
            await channel.send(message)
            await asyncio.sleep(1)  # Attendre 1 seconde entre chaque message

# Commande pour arrêter le spam
@bot.command()
async def stop(ctx):
    global spamming
    # Définir la variable spamming à False pour arrêter la boucle
    spamming = False
    await ctx.send("Le spam de la révolution a été arrêté !")

# Lancement du bot
bot.run(TOKEN)
