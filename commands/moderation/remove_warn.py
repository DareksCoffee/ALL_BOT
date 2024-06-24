import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color
import sqlite3
import aiosqlite

class RemoveWarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def remove_warning(self, warning_id):
        async with aiosqlite.connect("warnings.db") as db:
            await db.execute("DELETE FROM warnings WHERE warning_id = ?", (warning_id,))
            await db.commit()
    @nextcord.slash_command(name="remove_warn", description="remove a user warn")
    @application_checks.has_permissions(kick_members=True)
    async def remove(self, interaction: nextcord.Interaction, warning_id: str):
        """
        Remove a user warn.

        Parameters
        ----------
        warning_id:
            The ID of the warn
        """
        eembed = nextcord.Embed(
            description="A member warning has been removed",
            color=embed_color
        )

        embed.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text=interaction.guild.name, icon_url=self.bot.user.avatar.url)

        await logger.send_log_message(interaction.guild, embed, "moderation")
        await self.remove_warning(warning_id)
        embed = nextcord.Embed(
            title="Success!",
            description="The warn has been successfully removed.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(RemoveWarn(bot))