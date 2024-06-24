import nextcord
from nextcord.ext import commands
import requests

class ChuckNorrisJoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="chucknorris", description="Get a random Chuck Norris joke")
    async def chuck_norris_joke(self, interaction: nextcord.Interaction):
        response = requests.get("https://api.chucknorris.io/jokes/random")
        data = response.json()
        joke = data["value"]
        await interaction.response.send_message(joke)

def setup(bot):
    bot.add_cog(ChuckNorrisJoke(bot))