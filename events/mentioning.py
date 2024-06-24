import nextcord
from nextcord.ext import commands
from main import embed_color, RESET, GREEN

class OnMention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id in message.raw_mentions and message.author != self.bot.user:
            await message.channel.send("Hello! Please use `/help` to get the full list of commands")

def setup(bot):
    bot.add_cog(OnMention(bot))