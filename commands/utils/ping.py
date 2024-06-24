import nextcord
from nextcord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping",description="get the bot latency")
    async def ping(self, interaction: nextcord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong!\n{latency}ms')

def setup(bot):
    bot.add_cog(Ping(bot))