import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="unban", description="unban a user")
    @application_checks.has_permissions(ban_members=True)
    async def unban(self, interaction: nextcord.Interaction, user: nextcord.Member, notify: bool = None):
        """
        Unban a guild member.

        Parameters
        ----------
        user:
            Enter the guild member.
        notify:
            Notify the guild member (False by default)
        """
        embed = nextcord.Embed(
            title=f"Success",
            description=f"{user.name} has been successfully unbanned",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)
        await interaction.guild.unban(user)
        if notify:
            embed = nextcord.Embed(
                title="Unbanned",
                description=f"You have been unbanned in {interaction.guild.name}",
                color=embed_color
            )
            embed.set_thumbnail(url=interaction.guild.icon.url)
            await user.send(embed=embed)

def setup(bot):
    bot.add_cog(Unban(bot))