import nextcord
from nextcord.ext import commands, application_checks
from nextcord.ui import View, Button
from main import embed_color, ThrowError
import sqlite3
import aiosqlite

class Confirmation(View):
    def __init__(self, interaction: nextcord.Interaction, db: aiosqlite.Connection):
        super().__init__()
        self.interaction = interaction
        self.db = db

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.message.delete()
        await self.confirmation_callback(self.interaction, confirmed=True)

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.message.delete()
        await self.confirmation_callback(self.interaction, confirmed=False)

class Reward(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def add_reward_role(self, interaction: nextcord.Interaction, guild_id, role_id, required_level):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute("SELECT required_level FROM rewards WHERE guild_id = ? AND role_id = ?", (guild_id, role_id)) as cursor:
                existing_role = await cursor.fetchone()
                if existing_role:
                    await ThrowError(
                        interaction=interaction,
                        error=f"The role <@&{role_id}> is already a reward for level {existing_role[0]}.",
                        error_type="Leveling"
                    )
                    return
                else:
                    await db.execute(
                        "INSERT OR REPLACE INTO rewards (guild_id, role_id, required_level) VALUES (?, ?, ?)",
                        (guild_id, role_id, required_level)
                    )
                    await db.commit()

    async def clear_reward_roles(self, guild_id):
        async with aiosqlite.connect("leveling.db") as db:
            await db.execute("DELETE FROM rewards WHERE guild_id = ?", (guild_id,))
            await db.commit()

    @nextcord.slash_command(name="reward", description="rewards for leveling")
    @application_checks.has_permissions(administrator=True)
    async def reward(self, interaction: nextcord.Interaction):
        pass

    @reward.subcommand(name="add_role", description="Add a reward role for leveling up")
    @application_checks.has_permissions(administrator=True)
    async def add_role(self, interaction: nextcord.Interaction, role: nextcord.Role, level: int):
        if level < 1:
            await ThrowError(interaction=interaction, error="Level cannot be 0 or a negative number.", error_type="Leveling")
            return
        else:
            embed = nextcord.Embed(
                title="Success",
                description=f"Successfully added <@&{role.id}> as a reward for level {level}",
                color=embed_color
            )
            await self.add_reward_role(interaction, interaction.guild.id, role.id, level)
            await interaction.response.send_message(embed=embed)

    @reward.subcommand(name="clear_roles", description="Clear all reward roles for leveling up")
    @application_checks.has_permissions(administrator=True)
    async def clear_roles(self, interaction: nextcord.Interaction):
        await self.clear_reward_roles(interaction.guild.id)
        embed = nextcord.Embed(
            title="Success",
            description=f"Successfully cleared all reward roles.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

    @reward.subcommand(name="message", description="Add a custom levelup message")
    @application_checks.has_permissions(administrator=True)
    async def reward_message(self, interaction: nextcord.Interaction, message: str = None):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute('SELECT reward_message FROM custom WHERE guild_id = ?', (interaction.guild.id,)) as cursor:
                result = await cursor.fetchone()
                if result:
                    existing_message = result[0]
                    view = Confirmation(interaction, db)
                    embed = nextcord.Embed(
                        title="Are you sure?",
                        description=f"There is already an existing custom level up message:\n\n```{existing_message}```\n\nDo you want to replace it with the new message?",
                        color=embed_color
                    )
                    msg = await interaction.response.send_message(embed=embed, view=view)

                    async def confirmation_callback(self, confirmed: bool):
                        if confirmed:
                            async with aiosqlite.connect("leveling.db") as db:
                                await db.execute(
            "INSERT INTO custom (guild_id, reward_message) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET reward_message = excluded.reward_message",
            (interaction.guild.id, message)
            )
                                await db.commit()
                            embed = nextcord.Embed(
                                title="Success",
                                description="The level up reward message has been successfully set!",
                                color=embed_color
                            )
                            await interaction.followup.send(embed=embed)
                        else:
                            await interaction.followup.send("Cancelled.", ephemeral=True)

                    view.confirmation_callback = lambda self, confirmed: confirmation_callback(self, confirmed)
                else:
                    if not message:
                        embed = nextcord.Embed(
                            title="Reference",
                            description="`{username}` -> the user name\n`{usermention}` -> mention the user \n`{level}` -> the level of the user\n`{if condition}` -> if condition met return message\n`{else} -> if the previous condition has not been met return message`",
                            color=embed_color
                        )
                        embed.add_field(name="Example", value="**Input**\nCongratulations {usermention}! You have leveled up to {level}!", inline=False)
                        embed.add_field(name="Output", value=f"**Congratulations** {interaction.user.mention}! You have leveled up to 5!", inline=False)
                        await interaction.response.send_message(embed=embed)
                    else:
                        await db.execute('REPLACE INTO custom (guild_id, reward_message) VALUES (?, ?)', (interaction.guild.id, message))
                        await db.commit()
                        embed = nextcord.Embed(
                            title="Success",
                            description="The level up reward message has been successfully set!",
                            color=embed_color
                        )
                        await interaction.response.send_message(embed=embed)
    @reward.subcommand(name="info", description="Shows informations regarding customizing the levelup")
    async def reward_info(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="Reference",
            description="`{username}` -> returns the username\n`{usermention}` -> mention the user \n`{user_globalname}` -> returns the user display name\n`{level}` -> the level of the user\n`{if <condition>}` -> if condition met return message\n`{else}` -> if the previous condition has not been met return message\n`{endif}` -> end the if condition\n`{reward}` -> return True if the level is a required reward level (used in conditions)\n`{reward_role}` -> return the current reward role for the level (Returns None if there is no reward role for the level)"
                        "\n`{isOnDms}` -> return True if the message will be sent in DMs (used in conditions)\n`{isOnChannel}` -> return True if the message will be sent in a guild channel (used in conditions)",
            color=embed_color
                )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Reward(bot))