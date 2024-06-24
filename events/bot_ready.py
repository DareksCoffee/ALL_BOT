import nextcord
from nextcord.ext import commands
import sqlite3
import aiosqlite
from main import embed_color, RESET, GREEN

class BotReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is ready")
        await self.bot.change_presence(activity=nextcord.Game(name="/help | command list"))

        async with aiosqlite.connect("warnings.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS warnings (
                    warning_id TEXT PRIMARY KEY,
                    guild_id INTEGER,
                    user_id INTEGER,
                    moderator_id INTEGER,
                    reason TEXT
                )
                """
            )
            await db.commit()
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER,
                    guild_id INTEGER,
                    balance INTEGER DEFAULT 150,
                    bank INTEGER DEFAULT 0,
                    bank_limit INTEGER DEFAULT 1000,
                    job TEXT DEFAULT NULL,
                    PRIMARY KEY (user_id, guild_id)
                )
                """
            )
            await db.commit()

        async with aiosqlite.connect("server_security.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS anti_link (
                    server_id INTEGER PRIMARY KEY
                )
                """
            )
            await db.commit()
            
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS anti_raid (
                    server_id INTEGER PRIMARY KEY
                )
                """
            )
            await db.commit()
        async with aiosqlite.connect("leveling.db") as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS levels (
                    guild_id INTEGER,
                    user_id INTEGER,
                    xp INTEGER,
                    level INTEGER,
                    PRIMARY KEY (guild_id, user_id)
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS leveling_enabled (
                    guild_id INTEGER PRIMARY KEY,
                    enabled BOOLEAN
                )
            ''')

            await db.execute("""
                CREATE TABLE IF NOT EXISTS rewards (
                    guild_id INTEGER,
                    role_id INTEGER,
                    required_level INTEGER
                )
                """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS custom (
                    guild_id INTEGER PRIMARY KEY,
                    reward_message TEXT
                )
            """)

            await db.commit()
        async with aiosqlite.connect("server.db") as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS reaction_messages (
                    guild_id INTEGER,
                    message_id INTEGER,
                    role_id INTEGER
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS logging_enabled (
                    guild_id INTEGER PRIMARY KEY, 
                    enabled BOOLEAN
                )

            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS server_language (
                    guild_id INTEGER PRIMARY KEY,
                    language TEXT
                );
            ''')

            await db.commit()

            
def setup(bot):
    bot.add_cog(BotReady(bot))