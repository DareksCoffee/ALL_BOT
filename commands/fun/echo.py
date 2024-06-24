import nextcord
from nextcord.ext import commands

class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="echo", description="Make the bot say whatever you want")
    async def echo(self, interaction: nextcord.Interaction, *, message):
        """
        Make the bot say your message!

        Parameters
        ----------
        message:
            Provide your message.
        """
        await interaction.response.send_message(message)

def setup(bot):
    bot.add_cog(Echo(bot))