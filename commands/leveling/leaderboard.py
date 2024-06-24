import nextcord
from nextcord.ext import commands
import aiosqlite
from main import embed_color
from datetime import datetime

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="leaderboard", description="Shows you the top 10 users")
    async def leaderboard(self, interaction: nextcord.Interaction):
        limit = 10
        order_by = "level"
        emoji = ""
        number = 0
        guild_id = interaction.guild.id

        if await self.is_leveling_enabled(guild_id):
            async with aiosqlite.connect("leveling.db") as db:
                async with db.execute(f'SELECT user_id, {order_by} FROM levels WHERE guild_id = ? ORDER BY {order_by} DESC LIMIT ?', (guild_id, limit)) as cursor:
                    leaderboard = await cursor.fetchall()

            if leaderboard:
                user_ids = [row[0] for row in leaderboard]
                users = await self.fetch_users_in_bulk(user_ids)

                embed = nextcord.Embed(
                    title=f"Leaderboard",
                    description=f"Top 10 users in {interaction.guild.name}",
                    color=embed_color
                )
                embed.timestamp = datetime.now()
                embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
                for row, user in zip(leaderboard, users):
                    if row[1] <= 0:
                        break
                    else:
                        number += 1
                        emoji = ":first_place: " if number == 1 else ":second_place: " if number == 2 else ":third_place: " if number == 3 else ""
                        if number <= 3:
                            embed.add_field(name=f"{emoji} • {user.name}", value=f"{row[1]} lvl", inline= False)
                        else:
                            embed.add_field(name=f"{number} • {user.name}", value=f"{row[1]} lvl", inline= False)

                embed.set_thumbnail(url="https://i.imgur.com/hdtXYbj.png" if not interaction.guild.icon else interaction.guild.icon.url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(content="No data found for the leaderboard.")
        else:
            await interaction.response.send_message(content="Leveling is not enabled in this server.\nUse `/toggle_leveling` if you are the server administrator.")

    async def fetch_users_in_bulk(self, user_ids):
        users = []
        for user_id in user_ids:
            user = await self.bot.fetch_user(user_id)
            users.append(user)
        return users

    async def is_leveling_enabled(self, guild_id):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute('SELECT enabled FROM leveling_enabled WHERE guild_id = ?', (guild_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else True

def setup(bot):
    bot.add_cog(Leaderboard(bot))