import nextcord
from nextcord.ext import commands

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="lock", description="Lock")
    async def lock(self, interaction: nextcord.Interaction):
        pass
    @lock.subcommand(name="channel", description="Lock a channel for everyone")
    async def channel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        """
        Lock a channel.

        Parameters
        ----------
        channel:
            Provide a channel to lock (Optional)
        """
        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message(f"<#{channel.id}> has been successfully locked.")
        
    @lock.subcommand(name="role", description="Lock a channel for a role")
    async def role(self, interaction: nextcord.Interaction, role: nextcord.Role, channel: nextcord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.set_permissions(role, send_messages=False)
        await interaction.response.send_message(f"<#{channel.id}> has been successfully locked for {role.mention}.")


def setup(bot):
    bot.add_cog(Lock(bot))