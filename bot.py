import discord
from discord.ext import tasks, commands
from config import TOKEN


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        game = discord.Game('logs mode...')
        await client.change_presence(status=discord.Status.idle, activity=game)

    client.run(TOKEN)
