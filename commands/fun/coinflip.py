import nextcord
import random
from nextcord.ext import commands
from main import embed_color

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="coinflip", description="Flip a coin!")
    async def coinflip(self, interaction: nextcord.Interaction):
        coin = ["head", "tails"]
        embed = nextcord.Embed(
            title="Coin Flipped!",
            description=f"The coin landed on ||{random.choice(coin)}||",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(CoinFlip(bot))