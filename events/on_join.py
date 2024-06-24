import nextcord
from nextcord.ext import commands
from main import embed_color
import asyncio

class OnJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        last_server = len(self.bot.guilds)
        channel = None
        for text_channel in guild.text_channels:
            if not text_channel.permissions_for(guild.me).send_messages:
                continue
            if text_channel.type == nextcord.ChannelType.text:
                channel = text_channel
                break

        if channel:
            embed = nextcord.Embed(
                title="",
                description="Hello!\n\nI am ALL, a fully customizable security bot designed to enhance the security and engagement of your server through a variety of features, including entertaining commands and a robust leveling system.\n\n",
                color=embed_color
            )
            embed.add_field(
                name="Leveling",
                value="Leveling is enabled by default. If you wish to disable this feature, simply utilize `/toggle_leveling`.\n\n"
                      "You can designate a reward role upon leveling up by using `/reward add_role <role> <level>`. Please note that my role must be higher in hierarchy than the reward role in order for it to function properly.\n"
                      "Additionally, if you desire a custom leveling up message, use `/reward message <message>`. For detailed instructions and syntax to enhance your leveling up message, refer to `/reward info`.\n"
            )
            embed.add_field(
                name="Logging",
                value="By default, logging is disabled. To activate this feature, use `/enable_logging`. Upon activation, a dedicated category will be created, comprising two channels: one for moderation and another for comprehensive logging of server activities."
            )
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(OnJoin(bot))