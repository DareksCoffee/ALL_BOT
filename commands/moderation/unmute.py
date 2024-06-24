import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color, default_footer, ThrowError
import asyncio

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="unmute", description="Unmute a user.")
    @application_checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: nextcord.Interaction, user: nextcord.Member, notify: bool = False):
        """
        Mute a guild member.

        Parameters
        ----------
        user:
            Enter the guild member.
        reason:
            Provide a reason (Optional)
        notify:
            Notify the guild member (False by default)
        """
        muted = "The user " if not user.bot else "The bot "
        embed = nextcord.Embed(
            title=f"Unmuted",
            description=f"{muted}{user.name} has been successfully unmuted.\n**Username**: {user.name}\n**User ID**: {user.id}",
            color=embed_color
        )
        muted_role = nextcord.utils.get(interaction.guild.roles, name="Muted")

        if muted_role not in user.roles:
            await ThrowError(interaction=interaction, error=f"{user.name} is not muted.")
            return

        await user.remove_roles(muted_role, reason=reason)    
        ## Logger #####################################

        logger = Logger(self.bot)
        logging = nextcord.Embed(
            description=f"A member has been unmuted",
            color=embed_color
        )
        logging.add_field(name="User", value= f"{user.name} ({user.id})", inline=False)
        logging.add_field(name="Moderator", value= f"{interaction.user.name} ({interaction.user.id})", inline=False)

        logging.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        logging.set_thumbnail(url=user.avatar.url)
        logging.timestamp = datetime.now()
        logging.set_footer(text=interaction.guild.name, icon_url=self.bot.user.avatar.url)

        await logger.send_log_message(interaction.guild, logging, "moderation")
        ################################################

        await interaction.response.send_message(embed=embed)
        if notify:
            embed = nextcord.Embed(
                title=f"Unmuted",
                description=f"You have been unmuted in {interaction.guild.name}",
                color=embed_color
            )
            await user.send(embed=embed)

def setup(bot):
    bot.add_cog(Unmute(bot))