import nextcord
from nextcord.ext import commands, application_checks
from nextcord.ui import Button, View
from events.logger import Logger
from main import embed_color
from datetime import datetime
from main import embed_color, ThrowError
import asyncio

class VoteKick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.votes = {}

    @nextcord.slash_command(name="votekick", description="Start a vote to kick a user")
    @application_checks.has_permissions(kick_members=True)
    async def votekick(self, interaction: nextcord.Interaction, member: nextcord.Member):
        """
        Start a vote kick for a guild member.

        Parameters
        ----------
        member:
            Enter the guild member.
        """
        if member == interaction.user:
            await ThrowError(interaction=interaction, error="You cannot initiate a vote kick against yourself.")
            return

        if member == self.bot.user:
            await ThrowError(interaction=interaction, error="I cannot be kicked via vote kick.")
            return

        if member.guild_permissions.administrator:
            await ThrowError(interaction=interaction, error="You cannot initiate a vote kick against an administrator.")
            return

        if member.id in self.votes:
            await ThrowError(interaction=interaction, error="A vote kick is already in progress for this user.")
            return

        self.votes[member.id] = {"voters": set(), "votes_needed": len(interaction.guild.members) // 2}

        embed = nextcord.Embed(
            title=f"Vote kick initiated for {member.display_name}",
            description=f"Click the button below to vote on kicking {member.display_name}. {self.votes[member.id]['votes_needed']} votes needed.",
            color=embed_color
        )
        logger = Logger(self.bot)
        logging = nextcord.Embed(
            description=f"A votekick has been initiated for {member.display_name}",
            color=embed_color
        )
        logging.add_field(name="User", value= f"{member.name} ({member.id})", inline=False)
        logging.add_field(name="Moderator", value= f"{interaction.user.name} ({interaction.user.id})", inline=False)

        logging.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
        logging.set_thumbnail(url=member.avatar.url)
        logging.timestamp = datetime.now()
        logging.set_footer(text=interaction.guild.name, icon_url=self.bot.user.avatar.url)

        await logger.send_log_message(interaction.guild, logging, "moderation")
        view = VoteKickButtonView(member.id, self.votes, self.bot)
        view.message = await interaction.response.send_message(embed=embed, view=view)

        try:
            await asyncio.sleep(60)
            del self.votes[member.id]
            await view.message.delete()
        except asyncio.TimeoutError:
            pass

class VoteKickButtonView(View):
    def __init__(self, member_id, votes, bot):
        super().__init__()
        self.member_id = member_id
        self.votes = votes
        self.bot = bot

    async def interaction_check(self, interaction):
        return interaction.user.id not in self.votes[self.member_id]['voters']

    @nextcord.ui.button(label="Vote to Kick", style=nextcord.ButtonStyle.green)
    async def vote_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        self.votes[self.member_id]['voters'].add(interaction.user.id)
        await interaction.response.send_message("Your vote has been counted.", ephemeral=True)
        
        await self.update_embed(interaction)

        if len(self.votes[self.member_id]['voters']) >= self.votes[self.member_id]['votes_needed']:
            member = interaction.guild.get_member(self.member_id)
            await member.kick(reason="Vote kick passed.")
            logger = Logger(self.bot)
            logging = nextcord.Embed(
                description=f"The vote kick for {member.display_name} was successful",
                color=embed_color
            )
            logging.add_field(name="User", value= f"{member.name} ({member.id})", inline=False)

            logging.set_author(name="ALL Logging", icon_url=self.bot.user.avatar.url)
            logging.set_thumbnail(url=member.avatar.url)
            logging.timestamp = datetime.now()
            logging.set_footer(text=interaction.guild.name, icon_url=self.bot.user.avatar.url)
            await logger.send_log_message(interaction.guild, logging, "moderation")
            await interaction.response.send_message(f"{member.display_name} has been successfully vote kicked.")
            del self.votes[self.member_id]
            await self.message.delete()

    async def update_embed(self, interaction: nextcord.Interaction):
        votes_remaining = self.votes[self.member_id]['votes_needed'] - len(self.votes[self.member_id]['voters'])

        embed = interaction.message.embeds[0]
        embed.description = f"Click the button below to vote to kick {interaction.guild.get_member(self.member_id).display_name}. {votes_remaining} votes remaining."
        await interaction.message.edit(embed=embed)

def setup(bot):
    bot.add_cog(VoteKick(bot))