import nextcord
import sqlite3
import aiosqlite
from nextcord.ext import commands, application_checks
import random
from main import embed_color

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_balance(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            async with db.execute("SELECT balance FROM users WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0

    async def get_bank(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            async with db.execute("SELECT bank FROM users WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0

    async def get_bank_limit(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            async with db.execute("SELECT bank_limit FROM users WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 1000               
    async def get_job(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            cursor = await db.execute(
                "SELECT job FROM users WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id)
            )
            row = await cursor.fetchone()
            return row[0] if row else None

    @nextcord.slash_command(name="balance", description="View your balance")
    async def balance(self, interaction: nextcord.Interaction, user: nextcord.Member = None):
        if user == None:
            user = interaction.user
        user_balance = await self.get_balance(user.id, interaction.guild.id)

        bank_money = await self.get_bank(user.id, interaction.guild.id)
        bank_limit = await self.get_bank_limit(user.id, interaction.guild.id)

        job = await self.get_job(user.id, interaction.guild.id)
        embed = nextcord.Embed(
            title=f"{user.display_name}'s Balance",
            description=f"Here is the balance of {user.global_name}.",
            color=embed_color
        )
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="In-come", value=f"100-500 :coin:/minute")
        embed.add_field(name="Global Money", value=f"{user_balance} :coin:", inline = False)
        embed.add_field(name="Bank Money", value=f"{bank_money}/{bank_limit} :coin:", inline=False)
        if job:
            embed.add_field(name="Job", value=f"{job}")
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Balance(bot))