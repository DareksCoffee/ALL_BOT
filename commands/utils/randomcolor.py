import nextcord
from nextcord.ext import commands
import random
import requests

class RandomColor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="randomcolor", description="Generate a random hex color with preview")
    async def random_color(self, interaction: nextcord.Interaction):
        hex_color = ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
        embed = nextcord.Embed(title="Random Color Preview", color=int(hex_color, 16))
        embed.add_field(name="Hex Color", value=f"#{hex_color}", inline=False)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(RandomColor(bot))