import nextcord
import random
from nextcord.ext import commands
from main import embed_color

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="random", description="Randomness")
    async def random(self, interaction: nextcord.Interaction):
        pass

    @random.subcommand(name="number", description="Generate a random number")
    async def random_number(self, interaction: nextcord.Interaction, max: int):
        """
        Generate a random number.

        Parameters
        ----------
        max:
            Maximum number.
        """
        number = random.randint(0, max)
        embed = nextcord.Embed(
            description=f"**Random number:** {number}",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

    @random.subcommand(name="float", description="Generate a random float")
    async def random_float(self, interaction: nextcord.Interaction, x: float, y: float):
        """
        Generate a random float.

        Parameters
        ----------
        x:
            Minimum float number.
        y:
            Maximum float number.
        """
        if x >= y:
            await interaction.response.send_message("The first number must be smaller than the second number.")
            return

        random_float = random.uniform(x, y)
        embed = nextcord.Embed(
            description=f"**Random float:** {random_float}",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Random(bot))
