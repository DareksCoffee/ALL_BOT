import nextcord
from nextcord.ext import commands
import requests

class DadJoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="dadjoke", description="Get a random dad joke")
    async def dad_joke(self, interaction: nextcord.Interaction):
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        data = response.json()
        joke = data["joke"]
        await interaction.response.send_message(joke)

def setup(bot):
    bot.add_cog(DadJoke(bot))