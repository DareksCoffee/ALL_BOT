import nextcord
from nextcord.ext import commands
from main import embed_color, RESET, GREEN

class Ad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command(self, interaction: nextcord.Interaction):
        print("command")

def setup(bot):
    bot.add_cog(Ad(bot))