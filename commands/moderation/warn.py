import nextcord
from nextcord.ext import commands, application_checks
from events.logger import Logger
from main import embed_color
from datetime import datetime
import sqlite3
import aiosqlite
import random
import string

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def add_warning(self, warning_id, guild_id, user_id, moderator_id, reason):
        async with aiosqlite.connect("warnings.db") as db:
            await db.execute(
                "INSERT INTO warnings (warning_id, guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (warning_id, guild_id, user_id, moderator_id, reason)
            )
            await db.commit()

    @nextcord.slash_command(name="warn", description="warn a user")
    @application_checks.has_permissions(kick_members=True)
    async def warn(self, interaction: nextcord.Interaction, user: nextcord.Member, reason="No reason provided.", notify: bool = False):
        """
        Warn a guild member.

        Parameters
        ----------
        user:
            Enter the guild member.
        reason:
            Provide a reason (Optional)
        """
        characters = string.ascii_letters + string.digits
        warning_id = ''.join(random.choice(characters) for i in range(8))
        logger = Logger(self.bot)

        embed = nextcord.Embed(
            description="A member has been warned",
            color=embed_color
        )
        embed.add_field(name="User", value= f"{user.name} ({user.id})", inline=False)
        embed.add_field(name="Moderator", value= f"{interaction.user.name} ({interaction.user.id})", inline=False)
        embed.add_field(name="Reason", value= reason, inline=False)

        embed.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=user.avatar.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text=interaction.guild.name, icon_url=self.bot.user.avatar.url)

        await logger.send_log_message(interaction.guild, embed, "moderation")

        embed = nextcord.Embed(
            title=f"Success",
            description=f"{user.name} has been successfully warned\n**Reason**: {reason}",
            color=embed_color
        )
        embed.set_footer(text=f"User ID : {user.id}")
        await self.add_warning(warning_id, interaction.guild.id, user.id, interaction.user.id, reason)
        await interaction.response.send_message(embed=embed)
        if notify:
            warned = nextcord.Embed(
                title="You have been warned!",
                description=f"Reason: {reason}",
                color=embed_color
            )
            await user.send(embed=warned)

def setup(bot):
    bot.add_cog(Warn(bot))