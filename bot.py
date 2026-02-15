import discord
from discord.ext import tasks, commands
from discord import app_commands
from config import TOKEN
from api import find_report, find_fight


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='/', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        game = discord.Game('logs mode...')
        await client.change_presence(status=discord.Status.idle, activity=game)
        try:
            synced = await client.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as err:
            print(err)

    @client.tree.command(name='say', description='repeats back to you')
    @app_commands.describe(speak='the thing')
    async def repeat(ctx: discord.Interaction, speak: str):
        await ctx.response.send_message(f'{speak}', ephemeral=True)

    @client.tree.command(name='compare', description='compares logs')
    @app_commands.describe(log_id='the log ID')
    async def compare(ctx: discord.Interaction, log_id: str):
        report = find_report(log_id)
        # left off here with tying in api implementation
        # need to have drop down choice between fights in report
        # need to have drop down choice for players in fight
        # then comparable with future data
        await ctx.response.send_message(report, ephemeral=True)

    client.run(TOKEN)
