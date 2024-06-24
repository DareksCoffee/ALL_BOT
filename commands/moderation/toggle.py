import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color
import sqlite3
import aiosqlite
from datetime import datetime

class Toggle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(name="toggle", description="Toggle stuff")
    @application_checks.has_permissions(administrator=True)
    async def toggle(self, interaction: nextcord.Interaction):
        pass

    @toggle.subcommand(name="logging", description="Toggle logging")
    @application_checks.has_permissions(administrator=True)
    async def logging(self, interaction: nextcord.Interaction, action: bool):
        guild = interaction.guild
        async with aiosqlite.connect("server.db") as db:
            async with db.execute("SELECT * FROM logging_enabled WHERE guild_id = ?", (interaction.guild.id,)) as cursor:
                existing_entry = await cursor.fetchone()
                if existing_entry:
                    await db.execute("UPDATE logging_enabled SET enabled = ? WHERE guild_id = ?", (action, interaction.guild.id))
                else:
                    await db.execute("INSERT INTO logging_enabled (guild_id, enabled) VALUES (?, ?)", (interaction.guild.id, action))
                
                await db.commit()
            
            logging_category = nextcord.utils.get(guild.categories, name="Logging")
            if not logging_category:
                overwrites = {
                    guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
                }
                logging_category = await guild.create_category("Logging", overwrites=overwrites)

            moderation_channel = nextcord.utils.get(guild.channels, name="moderation")
            if not moderation_channel:
                moderation_channel = await logging_category.create_text_channel("moderation")
                embed = nextcord.Embed(
                    title = "Enabled",
                    description= "Moderation Logging has been successfully enabled and will start logging mod-related stuff.",
                    color=embed_color
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.timestamp = datetime.now()
                embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
                await moderation_channel.send(embed=embed)
            server_log_channel = nextcord.utils.get(guild.channels, name="server-log")
            if not server_log_channel:
                server_log_channel = await logging_category.create_text_channel("server-log")
                embed = nextcord.Embed(
                    title = "Enabled",
                    description= "Server Logging has been successfully enabled and will start logging server-related stuff.",
                    color=embed_color
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.timestamp = datetime.now()
                embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
                await server_log_channel.send(embed=embed)

            status = "enabled" if action else "disabled"
            await interaction.response.send_message(f"Logging is now {status} for this server.")
    @toggle.subcommand(name="leveling", description = "Toggle leveling system")
    @application_checks.has_permissions(administrator=True)
    async def toggle_leveling(self, interaction: nextcord.Interaction, action: bool):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute('SELECT enabled FROM leveling_enabled WHERE guild_id = ?', (interaction.guild.id,)) as cursor:
                result = await cursor.fetchone()
                if result:
                    await cursor.execute('UPDATE leveling_enabled SET enabled = ? WHERE guild_id = ?', (action, interaction.guild.id))
                else:
                    await cursor.execute('INSERT INTO leveling_enabled (guild_id, enabled) VALUES (?, ?)', (interaction.guild.id, action))
                await db.commit()
                
                status = "enabled" if action else "disabled"
                await interaction.response.send_message(f"Leveling system is now {status} for this server.")
def setup(bot):
    bot.add_cog(Toggle(bot))