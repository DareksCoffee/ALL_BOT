import nextcord
import random
import sqlite3
import aiosqlite
from nextcord.ext import commands
from main import embed_color, ThrowError
from cooldown import Cooldown

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = Cooldown()

    async def update_balance(self, user_id, guild_id, amount):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?) ON CONFLICT(user_id, guild_id) DO UPDATE SET balance = balance + ?",
                (user_id, guild_id, amount, amount,)
            )
            await db.commit()

    @nextcord.slash_command(name="beg", description="Earn a couple dollars by begging!")
    async def beg(self, interaction: nextcord.Interaction):
        remaining_time = await self.cooldown.check_cooldown(interaction.user.id, interaction.guild.id)
        if remaining_time:
            await ThrowError(interaction=interaction, error=f"You are tired! Wait {remaining_time:.2f} seconds to beg again.", error_type="Cooldown")
            return
        earnings = random.randint(20, 250)
        await self.update_balance(interaction.user.id, interaction.guild.id, earnings)
        embed = nextcord.Embed(
            description=f"A generous person gave you {earnings}$ :coin:",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)
        await self.cooldown.start_cooldown(60, interaction.user.id, interaction.guild.id)

def setup(bot):
    bot.add_cog(Beg(bot))