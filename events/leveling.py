import nextcord
from nextcord.ext import commands
import aiosqlite
import random
import re

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def is_leveling_enabled(guild_id):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute('SELECT enabled FROM leveling_enabled WHERE guild_id = ?', (guild_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else True       

    def xp_for_level(self, level):
        return 100 * level
        
    def calculate_xp(self, level, m):
        if m.attachments:
            return random.randint(10, 25) if level < 2 else random.randint(20, 55)
        elif len(m.content) > 500:
            return random.randint(50, 75) if level < 2 else random.randint(50, 100)
        else:
            return random.randint(5, 10) if level < 2 else random.randint(10, 50)

    async def get_custom_message(self, guild_id, user, level, isOnChannel, isOnDms, reward):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute('SELECT reward_message FROM custom WHERE guild_id = ?', (guild_id,)) as cursor:
                result = await cursor.fetchone()
                if result:
                    message = result[0]
                    if '{username}' in message:
                        message = message.replace('{username}', user.name)
                    if '{usermention}' in message:
                        message = message.replace('{usermention}', user.mention)
                    if '{user_globalname}' in message:
                        message = message.replace('{user_globalname}', str(user.display_name))
                    if '{level}' in message:
                        message = message.replace('{level}', str(level))
                    if '{reward}' in message:
                        reward_role = await self.get_reward_role(guild_id, level)
                        message = message.replace('{reward}', 'True' if reward_role else 'False')

                    if '{reward_role}' in message:
                        reward_role = await self.get_reward_role(guild_id, level)
                        message = message.replace('{reward_role}', reward_role.name if reward_role else 'None')
                    
                    condition_pattern = re.compile(r'\{if\s+(.*?)\}(.*?)\{else\}(.*?)\{endif\}')
                    matches = re.findall(condition_pattern, message)
                    for match in matches:
                        condition, if_clause, else_clause = match
                        if eval(f"{condition}"):
                            message = message.replace(f'{{if {condition}}}{if_clause}{{else}}{else_clause}{{endif}}', if_clause)
                        else:
                            message = message.replace(f'{{if {condition}}}{if_clause}{{else}}{else_clause}{{endif}}', else_clause)

                    return message
                else:
                    return None



    async def get_reward_role(self, guild_id, level):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute('SELECT role_id FROM rewards WHERE guild_id = ? AND required_level = ?', (guild_id, level)) as cursor:
                result = await cursor.fetchone()
                if result:
                    role_id = result[0]
                    guild = self.bot.get_guild(guild_id)
                    if guild:
                        return guild.get_role(role_id)
                return None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot: 
            guild_id = message.guild.id
            user_id = message.author.id

            isOnChannel = isinstance(message.channel, nextcord.TextChannel)
            isOnDms = isinstance(message.channel, nextcord.DMChannel)
            if await self.is_leveling_enabled(guild_id):
                async with aiosqlite.connect("leveling.db") as db:
                    async with db.execute('SELECT xp, level FROM levels WHERE guild_id = ? AND user_id = ?', (guild_id, user_id)) as cursor:
                        result = await cursor.fetchone()
                        if result:
                            xp, level = result
                            xp += self.calculate_xp(level, message)
                            required_xp = self.xp_for_level(level + 1)
                            if xp >= required_xp:
                                level += 1
                                xp = xp - required_xp
                                reward_role = await self.get_reward_role(guild_id, level)
                                if reward_role:
                                    custom_message = await self.get_custom_message(guild_id, message.author, level, isOnChannel, isOnDms, reward_role)
                                    if custom_message:
                                        await message.channel.send(custom_message)
                                    else:
                                        await message.channel.send(f'Congratulations {message.author.mention}! You have reached level {level} and received {reward_role.name}')

                                    await message.author.add_roles(reward_role)

                                else: 
                                    custom_message = await self.get_custom_message(guild_id, message.author, level, isOnChannel, isOnDms, None)
                                    if custom_message:
                                        await message.channel.send(custom_message)
                                    else:
                                        await message.channel.send(f'Congratulations {message.author.mention}! You have reached level {level}!')

                                await db.execute('UPDATE levels SET xp = ?, level = ? WHERE guild_id = ? AND user_id = ?', (xp, level, guild_id, user_id))
                                await db.commit()
                            else:
                                await db.execute('UPDATE levels SET xp = ? WHERE guild_id = ? AND user_id = ?', (xp, guild_id, user_id))
                                await db.commit()  
                        else:
                            await db.execute('INSERT INTO levels (guild_id, user_id, xp, level) VALUES (?, ?, ?, ?)', (guild_id, user_id, 1, 0))
                            await db.commit() 


def setup(bot):
    bot.add_cog(Leveling(bot))