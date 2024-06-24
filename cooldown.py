import asyncio
import time

class Cooldown:
    def __init__(self):
        self.guild_cooldowns = {}

    async def check_cooldown(self, user_id, guild_id):
        if guild_id in self.guild_cooldowns and user_id in self.guild_cooldowns[guild_id]:
            cooldown_end_time = self.guild_cooldowns[guild_id][user_id]['end_time']
            remaining_time = cooldown_end_time - time.time()
            if remaining_time > 0:
                return remaining_time
            else:
                del self.guild_cooldowns[guild_id][user_id]
                if not self.guild_cooldowns[guild_id]:
                    del self.guild_cooldowns[guild_id]
        return False

    async def start_cooldown(self, duration: int, user_id, guild_id):
        if guild_id not in self.guild_cooldowns:
            self.guild_cooldowns[guild_id] = {}
        self.guild_cooldowns[guild_id][user_id] = {'end_time': time.time() + duration}
        await asyncio.sleep(duration)
        del self.guild_cooldowns[guild_id][user_id]
        if not self.guild_cooldowns[guild_id]:
            del self.guild_cooldowns[guild_id]