import nextcord
import random
from nextcord.ext import commands
from main import embed_color, default_footer

class PPSize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ppsize", description="pp size go crazy")
    async def ppsize(self, interaction: nextcord.Interaction, member: nextcord.Member=None):
        """
        How long is the member's PP!

        Parameters
        ----------
        member:
            Enter the guild member.
        """
        if member is None:
            member = interaction.user
        
        random_num = random.randint(1, 18)
        pp_size = "8" + "=" * random_num + "D"
        inches = random_num / 2.0  
        formatted_inches = "{:.1f}".format(inches)
        embed = nextcord.Embed(
            title=f"PP size of {member.name}",
            description=f"{pp_size} | {formatted_inches} inches",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(PPSize(bot))