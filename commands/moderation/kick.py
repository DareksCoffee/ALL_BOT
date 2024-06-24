import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color, default_footer, ThrowError, load_language

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="kick", description="Kick a user.")
    @application_checks.has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, user: nextcord.Member, reason= "No reason provided."):
        """
        Kick a guild member.

        Parameters
        ----------
        user:
            Enter a guild member.
        reason:
            Provide a reason (Optional)
        """
        guild_language_data = await load_language(interaction.guild_id)

        if user == interaction.user:
            await ThrowError(interaction=interaction, error="You cannot kick yourself.")
        elif user == self.bot.user:
            await ThrowError(interaction=interaction, error="You cannot kick me via my command.")
        elif not interaction.guild.me.top_role > user.top_role:
            await ThrowError(interaction=interaction, error="I cannot kick this user due to role hierarchy.")
        else:
            kicked = "The user" if not user.bot else "The bot"
            embed = nextcord.Embed(
                title="Kicked",
                description=f"{kicked} {user.name} has been successfully kicked.",
                color=embed_color
            )
            embed.add_field(name="Informations", value=f"**User ID**: {user.id}\n**Reason**: {reason}")
            await interaction.response.send_message(embed=embed)
            await user.kick(reason=reason)

def setup(bot):
    bot.add_cog(Kick(bot))