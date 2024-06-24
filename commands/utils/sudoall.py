import nextcord
from nextcord.ext import commands, application_checks

class SudoAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="sudoall", description="Make every user say whatever you want")
    @application_checks.has_permissions(administrator=True)
    async def sudoall(self, interaction: nextcord.Interaction, message):
        for member in interaction.guild.members:
            webhook = await interaction.channel.create_webhook(name=member.display_name, avatar=member.avatar)
            await webhook.send(content=message)
            await webhook.delete()
        
        await interaction.response.send_message("Done.", ephemeral=True)

def setup(bot):
    bot.add_cog(SudoAll(bot))