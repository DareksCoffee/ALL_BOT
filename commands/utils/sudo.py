import nextcord
from nextcord.ext import commands

class Sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="sudo", description="Make a user say whatever you want")
    async def sudo(self, interaction: nextcord.Interaction, user: nextcord.Member, message):
        """
        Sudo a message (Make a member say your message)

        Parameters
        ----------
        user:
            Enter the guild member.
        message:
            Provide a message.
        """
        webhook = await interaction.channel.create_webhook(name=user.display_name, avatar=user.avatar)
        
        await webhook.send(content=message)
        await interaction.response.send_message("Done.", ephemeral=True)
        await webhook.delete()

def setup(bot):
    bot.add_cog(Sudo(bot))
