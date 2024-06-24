import nextcord
from nextcord.ext import commands
from main import embed_color, ThrowError
import requests

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="meme", description="Get a random meme")
    async def meme(self, interaction: nextcord.Interaction):
        try:
            response = requests.get('https://meme-api.com/gimme/2')
            data = response.json()
            
            if 'memes' in data:
                memes = data['memes']
                for meme in memes:
                    meme_url = meme['url']
                    embed = nextcord.Embed(title="Fresh Meme", color=embed_color)
                    embed.set_image(url=meme_url)
                    await interaction.response.send_message(embed=embed)
            else:
                await ThrowError(interaction=interaction, error="Cannot find a meme, please try again!", error_type="Out of memes!")
        except Exception as e:
            print(e)
            await ThrowError(interaction=interaction, error="Cannot find a meme, please try again!", error_type="Out of memes!")

def setup(bot):
    bot.add_cog(Meme(bot))
