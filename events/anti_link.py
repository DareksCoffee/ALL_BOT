import nextcord
from nextcord.ext import commands
import aiosqlite

class AntiLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
        self.links = ["http", "www.", "discord.gg"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        async with aiosqlite.connect("server_security.db") as db:
            cursor = await db.execute("SELECT * FROM anti_link WHERE server_id = ?", (message.guild.id,))
            data = await cursor.fetchone()

            if data:
                for link in self.links:
                    if link in message.content:
                        await message.delete()
                        user = message.author
                        await user.send("You cannot send links.")

def setup(bot):
    bot.add_cog(AntiLink(bot))