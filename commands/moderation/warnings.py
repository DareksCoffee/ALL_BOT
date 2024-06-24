import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color, ThrowError
import sqlite3
import aiosqlite

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_warnings(self, guild_id, user_id):
        async with aiosqlite.connect("warnings.db") as db:
            async with db.execute(
                "SELECT warning_id, moderator_id, reason FROM warnings WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id)
            ) as cursor:
                return await cursor.fetchall()
    async def get_warn_by_ID(self, guild_id, user_id, warning_id):
        async with aiosqlite.connect("warnings.db") as db:
            async with db.execute(
                "SELECT moderator_id, reason FROM warnings WHERE guild_id = ? AND user_id = ? AND warning_id = ?",
                (guild_id, user_id, warning_id)
            ) as cursor:
                return await cursor.fetchone()

    @nextcord.slash_command(name="warnings", description="View user's warning history")
    @application_checks.has_permissions(kick_members=True)
    async def warnings(self, interaction: nextcord.Interaction, user: nextcord.Member):
        pass
    @warnings.subcommand(name="history", description="View user's warning history")
    async def history(self, interaction: nextcord.Interaction, user: nextcord.Member):
        """
        Receive the warning history of the guild member.

        Parameters
        ----------
        user:
            Enter the guild member.
        """
        warnings = await self.get_warnings(interaction.guild.id, user.id)
        if not warnings:
            await interaction.send("This user has no warnings.")
            return
        embed = nextcord.Embed(
            title=f"Warning History for {user.display_name}",
            color=embed_color
            )
        for warning_id, moderator_id, reason in warnings:
            moderator = interaction.guild.get_member(moderator_id)
            embed.add_field(name=f"Warning ID: {warning_id}", value=f"Moderator: {moderator.display_name}\nReason: {reason}", inline=False)

        await interaction.response.send_message(embed=embed)
    @warnings.subcommand(name="check", description="Check specific warning")
    async def check(self, interaction: nextcord.Interaction, user: nextcord.Member, warning_id: str):
        """
        Check a specific warning for a user.

        Parameters
        ----------
        user:
            Enter the guild member.
        warning_id:
            Enter the warning ID of the guild member.
        """
        warning = await self.get_warn_by_ID(interaction.guild.id, user.id, warning_id)
        if not warning:
            await interaction.send("Warning not found.")
            return
        moderator_id, reason = warning
        moderator = interaction.guild.get_member(moderator_id)
        embed = nextcord.Embed(
            title=f"Warning Details",
            color=embed_color
        )
        embed.add_field(name="Warning ID", value=warning_id, inline=False)
        embed.add_field(name="User", value=user.display_name, inline=False)
        embed.add_field(name="Moderator", value=moderator.display_name, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)

        await interaction.send(embed=embed)
def setup(bot):
    bot.add_cog(Warnings(bot))