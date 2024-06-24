import nextcord
from nextcord.ext import commands
import aiosqlite
from datetime import datetime, timedelta
from main import embed_color

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}
        
    async def send_log_message(self, guild, content, _type: str = None):
        async with aiosqlite.connect("server.db") as db:
            async with db.execute("SELECT * FROM logging_enabled WHERE guild_id = ?", (guild.id,)) as cursor:
                existing_entry = await cursor.fetchone()
                if existing_entry and existing_entry[1]:
                    category = nextcord.utils.get(guild.categories, name="Logging")
                    if category:
                        if _type and _type in ["moderation", "server-log"]:
                            log_channel = nextcord.utils.get(category.text_channels, name=_type)
                            if log_channel:
                                await log_channel.send(embed=content)
                                    
    async def common_embed(self, message, description):
        message_url = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        embed = nextcord.Embed(
            description=description,
            color=embed_color
        )
        embed.add_field(name="Message :", value=f"{message.content}\n\n[Jump to message]({message_url})")
        embed.add_field(name="Channel :", value=f"<#{message.channel.id}>", inline=False)
        embed.add_field(name="Author :", value=f"{message.author.name} ({message.author.id})", inline=False)
        embed.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        if message.author.avatar.url:
            embed.set_thumbnail(url=message.author.avatar.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text=message.author.guild.name, icon_url=self.bot.user.avatar.url)
        return embed
        
    ## General Logging ##

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if "discord.gg" in message.content:
            description = "A message containing an invite has been detected"
        elif "https://" in message.content or "http://" in message.content:
            description = "A message containing a link has been detected"
        else:
            return

        embed = await self.common_embed(message, description)
        await self.send_log_message(message.guild, embed)
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        embed = await self.common_embed(message, "A message has been deleted")
        await self.send_log_message(message.guild, embed, "server-log")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            embed = await self.common_embed(message, "A user joined voice channel")
            await self.send_log_message(message.guild, embed, "server-log")
        if before.channel:
            embed = await self.common_embed(message, "User left voice channel")
            await self.send_log_message(message.guild, embed, "server-log")
            
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        embed = nextcord.Embed(
            description="Server invite created by user",
            color=embed_color
        )
        embed.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=invite.inviter.avatar.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text=invite.guild.name, icon_url=self.bot.user.avatar.url)
        await self.send_log_message(invite.guild, embed, "server-log")
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        embed = None

        if before.display_name != after.display_name:
            embed = nextcord.Embed(
                description=f"User: {after.name}\nDisplay Name changed from `{before.display_name}` to `{after.display_name}`",
                color=embed_color
            )

        elif before.avatar != after.avatar:
            embed = nextcord.Embed(
                description=f"User profile edit\nUser: {after.name}\nAvatar changed",
                color=embed_color
            )

        elif before.nick != after.nick:
            embed = nextcord.Embed(
                description=f"User profile edit\nUser: {after.name}\nNickname changed from `{before.nick}` to `{after.nick}`",
                color=embed_color
            )

        elif before.roles != after.roles:
            added_roles = [role.name for role in after.roles if role not in before.roles]
            removed_roles = [role.name for role in before.roles if role not in after.roles]

            if added_roles:
                added_roles_str = ', '.join(added_roles)
                embed = nextcord.Embed(
                    description=f"User profile edit\nUser: {after.name}\nRoles added: {added_roles_str}",
                    color=embed_color
                )

            if removed_roles:
                removed_roles_str = ', '.join(removed_roles)
                embed = nextcord.Embed(
                    description=f"User profile edit\nUser: {after.name}\nRoles removed: {removed_roles_str}",
                    color=embed_color
                )

        if embed:
            embed.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
            embed.set_thumbnail(url=after.avatar.url)
            embed.timestamp = datetime.now()
            embed.set_footer(text=after.guild.name, icon_url=self.bot.user.avatar.url)
            await self.send_log_message(after.guild, embed, "server-log")
                
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.guild.id in self.cooldowns:
            if datetime.now() < self.cooldowns[after.guild.id]:
                return 
        self.cooldowns[after.guild.id] = datetime.now() + timedelta(seconds=5)

        if after.author.bot or before.author == self.bot.user:
            return

        message_url = f"https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}"
        embed = nextcord.Embed(
            description="A message has been edited",
            color=embed_color
        )
        embed.add_field(name="Message :", value=f"Before:\n`{before.content}`\n\nAfter:\n`{after.content}`\n[Jump to message]({message_url})")
        embed.add_field(name="Channel :", value=f"<#{after.channel.id}>", inline=False)
        embed.add_field(name="Author :", value=f"{after.author.name} ({after.author.id})", inline=False)
        embed.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=after.author.avatar.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text=after.guild.name, icon_url=self.bot.user.avatar.url)
        await self.send_log_message(after.guild, embed, "server-log")
        
    ##############################################################################################

    ## Moderation ##
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        embed = nextcord.Embed(
            description=f"{member.name} has been banned from the server",
            color=embed_color
        )
        embed.set_author(name="Member Banned", icon_url=member.avatar.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text=guild.name, icon_url=self.bot.user.avatar.url)
        await self.send_log_message(guild, embed, "moderation")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        embed = nextcord.Embed(
            description=f"{member.name} has been unbanned from the server",
            color=embed_color
        )
        embed.set_author(name="Member Unbanned", icon_url=member.avatar.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text=guild.name, icon_url=self.bot.user.avatar.url)
        await self.send_log_message(guild, embed, "moderation")
def setup(bot):
    bot.add_cog(Logger(bot))