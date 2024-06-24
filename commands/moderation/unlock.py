import nextcord
from nextcord.ext import commands

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="unlock", description="Unlock a channel.")
    async def unlock(self, interaction: nextcord.Interaction):
        pass

    @unlock.subcommand(name="channel", description="unlock a channel for everyone")
    async def channel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        """
        Unlock a channel to everyone.

        Parameters
        ----------
        channel:
            Enter the channel to unlock (Optional).
        """

        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message(f"<#{channel.id}> has been successfully unlocked.")

    @unlock.subcommand(name="role", description="unlock a channel for a role")
    async def role(self, interaction: nextcord.Interaction, role: nextcord.Role, channel: nextcord.TextChannel = None):
        """
        Unlock a channel for a role.

        Parameters
        ----------
        role:
            Enter the role.
        channel:
            Enter the channel to unlock (Optional)
        """

        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message(f"<#{channel.id}> has been successfully unlocked for {role.name}.")

def setup(bot):
    bot.add_cog(Unlock(bot))