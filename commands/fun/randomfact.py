import nextcord
from nextcord.ext import commands
import requests

class RandomFact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="randomfact", description="Get a random fact")
    async def random_fact(self, interaction: nextcord.Interaction):
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        data = response.json()
        fact = data["text"]
        await interaction.response.send_message(fact)

def setup(bot):
    bot.add_cog(RandomFact(bot))