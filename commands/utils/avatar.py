import nextcord
from nextcord.ext import commands
from main import embed_color

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="avatar", description="Receive user avatar")
    async def avatar(self, interaction: nextcord.Interaction):
        user = interaction.user       
        embed = nextcord.Embed(
            title=f"Your avatar",
            color=embed_color
        )
        embed.set_image(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Avatar(bot))