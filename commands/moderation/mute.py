import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color, default_footer, ThrowError, load_language
from datetime import datetime
from events.logger import Logger
import asyncio

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def load_guild_language(self, guild_id):
        self.guild_language_data[guild_id] = await load_language(guild_id)

    @nextcord.slash_command(name="mute", description="Mute a user.")
    @application_checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: nextcord.Interaction, user: nextcord.Member, duration: str = None, reason="No reason provided.", notify: bool = False):
        """
        Mute a guild member.

        Parameters
        ----------
        user:
            Enter a guild member.
        duration:
            Enter a duration in seconds (Optional)
        reason:
            Provide a reason (Optional)
        notify:
            Notify the member of the mute
        """

        if user == interaction.user:
            await ThrowError(interaction=interaction, error="You cannot mute yourself.")
            return
        elif user == self.bot.user:
            await ThrowError(interaction=interaction, error="You cannot mute me via my command.")
            return
        elif not interaction.guild.me.top_role > user.top_role:
            await ThrowError(interaction=interaction, error="I cannot mute this user due to role hierarchy.")
            return

        muted = "The user" if not user.bot else "The bot"
        embed = nextcord.Embed(
            title="Muted",
            description=f"{muted} \"{user.name}\" has been successfully muted.",
            color=embed_color
        )
        new_duration = duration if duration else "Indefinite."
        embed.add_field(name="Informations", value=f"**User ID**: {user.id}\n**Reason**: {reason}\n**Duration**: {new_duration}")
        muted_role = nextcord.utils.get(interaction.guild.roles, name="muted")

        ## Logger #####################################

        logger = Logger(self.bot)
        logging = nextcord.Embed(
            description=f"A member has been muted",
            color=embed_color
        )
        logging.add_field(name="User", value= f"{user.name} ({user.id})", inline=False)
        logging.add_field(name="Moderator", value= f"{interaction.user.name} ({interaction.user.id})", inline=False)
        logging.add_field(name="Reason", value= reason, inline=False)

        if duration:
            logging.add_field(name="Duration", value= f"{duration}", inline=False)

        logging.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        logging.set_thumbnail(url=user.avatar.url)
        logging.timestamp = datetime.now()
        logging.set_footer(text=interaction.guild.name, icon_url=self.bot.user.avatar.url)

        await logger.send_log_message(interaction.guild, logging, "moderation")
        ################################################
        if not muted_role:
            muted_role = await interaction.guild.create_role(name="muted")
        for channel in interaction.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
        await interaction.response.send_message(embed=embed)
        await user.add_roles(muted_role, reason=reason)
        if duration:
            await asyncio.sleep(parse_duration(duration))
            await user.remove_roles(muted_role, reason="Mute expired.")

        if notify:
            embed = nextcord.Embed(
                title="Muted",
                description=f"You have been muted in {interaction.guild.name} for the following reason:\n ```\n{reason}\n```",
                color=embed_color
            )
            await user.send(embed=embed)

def parse_duration(duration_str):
    total_seconds = 0
    multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400} 
    
    components = []
    current_number = ""
    for char in duration_str:
        if char.isdigit():
            current_number += char
        elif char in multipliers:
            if current_number:
                components.append((int(current_number), char))
                current_number = ""
        else:
            raise ValueError(f"Invalid duration string: {duration_str}")

    if current_number:
        raise ValueError(f"Invalid duration string: {duration_str}")

    for number, unit in components:
        total_seconds += number * multipliers[unit]

    return total_seconds

def setup(bot):
    bot.add_cog(Mute(bot))