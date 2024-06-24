import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color, default_footer, ThrowError, load_language

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_language_data = {}

    async def load_guild_language(self, guild_id):
        self.guild_language_data[guild_id] = await load_language(guild_id)

    @nextcord.slash_command(name="ban")
    @application_checks.has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
        """
        Bans a guild member.

        Parameters
        ----------
        user:
            Enter a guild member.
        reason:
            Provide a reason (Optional)
        """
        
        if user == interaction.user:
            await ThrowError(interaction=interaction, error="You cannot ban yourself.")
        elif user == self.bot.user:
            await ThrowError(interaction=interaction, error="You cannot ban me via my command.")
        elif not interaction.guild.me.top_role > user.top_role:
            await ThrowError(interaction=interaction, error="I cannot ban this user due to role hierarchy.")
        
        banned = "The user" if not user.bot else "The bot"
        embed = nextcord.Embed(
            title="Banned",
            description=f"{banned} {user.name} has been successfully banned.",
            color=embed_color
        )
        embed.add_field(name="Informations", value=f"**User ID**: {user.id}\n**Reason**: {reason}")
        await user.ban(reason=reason)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Ban(bot))