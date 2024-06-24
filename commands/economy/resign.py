import nextcord
import sqlite3
import aiosqlite
from nextcord.ext import commands, application_checks
import random
from main import embed_color, ThrowError

class Resign(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def has_job(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            async with db.execute("SELECT job FROM users WHERE user_id = ? AND guild_id = ?", (user_id, guild_id)) as cursor:
                existing_job = await cursor.fetchone()
                return existing_job[0] is not None if existing_job else False

    async def resign_job(self, user_id, guild_id):
        if await self.has_job(user_id, guild_id):
            async with aiosqlite.connect("economy.db") as db:
                await db.execute(
                    "INSERT INTO users (user_id, guild_id, job) VALUES (?, ?, ?) ON CONFLICT(user_id, guild_id) DO UPDATE SET job = job + ?",
                    (user_id, guild_id, None, None,)
                )
                await db.commit()       

    @nextcord.slash_command(name="resign", description="Resign on your current job.")
    async def resign(self, interaction: nextcord.Interaction):
        middle_finger = """
....................../´¯/) 
....................,/¯../ 
.................../..../ 
............./´¯/'...'/´¯¯`·¸ 
........../'/.../..../......./¨¯\ 
........('(...´...´.... ¯~/'...') 
.........\.................'...../ 
..........''...\.......... _.·´ 
............\..............( 
..............\.............\...
                        """
        if await self.has_job(interaction.user.id, interaction.guild.id):
            await self.resign_job(interaction.user.id, interaction.guild.id)

            embed = nextcord.Embed(
                title="You have resigned",
                description=f"You've sent this to your boss E-mail and got fired as a result\n```\n{middle_finger}\nfuck u lol im out\n```\nUse `/joblist` to get the list of all available jobs.",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed)
        else:
            await ThrowError(interaction=interaction, error="You do not have a job.", error_type="Economy")

def setup(bot):
    bot.add_cog(Resign(bot))