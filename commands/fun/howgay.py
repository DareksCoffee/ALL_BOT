import nextcord
import random
from nextcord.ext import commands
from main import embed_color

class HowGay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="howgay", description="How gay is a user!")
    async def howgay(self, interaction: nextcord.Interaction, user: nextcord.Member):
        """
        How gay is a member!

        Parameters
        ----------
        user:
            Enter the guild member.
        """
        percentage = random.randint(0, 100) 
        isgay = " is not" if percentage < 20 else " is mildly" if percentage <= 50 else " is"

        embed = nextcord.Embed(
            title=f"How gay is {user.name}",
            description=f"**Gay Percentage**: {percentage}%\n{user.name}{isgay} gay",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(HowGay(bot))