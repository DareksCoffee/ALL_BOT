import nextcord
import random
import sqlite3
import aiosqlite
from nextcord.ext import commands
from main import embed_color, ThrowError
from cooldown import Cooldown

class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = Cooldown()

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

    async def update_balance(self, user_id, guild_id, amount):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "UPDATE users SET balance = ? WHERE user_id = ? AND guild_id = ?",
                (amount, user_id, guild_id)
            )
            await db.commit()

    async def update_bank(self, user_id, guild_id, amount):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "UPDATE users SET bank = ? WHERE user_id = ? AND guild_id = ?",
                (amount, user_id, guild_id)
            )
            await db.commit()

    @nextcord.slash_command(name="withdraw", description="Withdraw your coins")
    async def withdraw(self, interaction: nextcord.Interaction, amount: int):
        user_id = interaction.user.id
        guild_id = interaction.guild.id

        if amount <= 0:
            await ThrowError(interaction=interaction, error="The amount must be greater than 0.", error_type="Negative")
            return

        bank = await self.get_bank(user_id, guild_id)
        if bank < amount:
            await ThrowError(interaction=interaction, error="You don't have enough money in your bank.", error_type="Negative")
            return

        balance = await self.get_balance(user_id, guild_id)
        await self.update_balance(user_id, guild_id, balance + amount)
        await self.update_bank(user_id, guild_id, bank - amount)
        embed = nextcord.Embed(
            title="Success",
            description=f"You have successfully withdrawn {amount} :coin: from your bank",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Withdraw(bot))