import nextcord
from nextcord.ext import commands
from main import embed_color, ThrowError
import requests

class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="cat", description="Shows a cute cat picture.")
    async def cat(self, interaction: nextcord.Interaction):
        response = requests.get("https://api.thecatapi.com/v1/images/search")

        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                cat_url = data[0].get("url")

                embed = nextcord.Embed(
                    title="Cute cat picture",
                    color=embed_color
                )
                embed.set_image(url=cat_url)
                await interaction.response.send_message(embed=embed)
            else:
                await ThrowError(interaction=interaction, error="I couldn't find any silly cat pictures!", error_type="Cat Overload")
        else:
            await ThrowError(interaction=interaction, error="I couldn't find any silly cat pictures!", error_type="Cat Overload")

def setup(bot):
    bot.add_cog(Cat(bot))
