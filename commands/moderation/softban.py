import nextcord
from nextcord.ext import commands
from main import embed_color, ThrowError
from datetime import datetime

class SoftBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="softban", description="Softban a user (Ban then immedietely unban to delete user's messages)")
    async def softban(self, interaction: nextcord.Interaction, user: nextcord.Member, *, reason: str = "No reason provided", notify: bool = False):
        """
        Softban a user

        Parameters
        ----------
        user:
            Enter the guild member.
        reason:
            Enter the reason (Optional)
        notify:
            Notify the user (False by default)
        """
        if user == interaction.user:
            ThrowError(interaction=interaction, error="You cannot soft-ban yourself.")

        embed = nextcord.Embed(
            title= "Success",
            description= f"{user.global_name if user.global_name else user.name} has been successfully soft-banned.",
            color=embed_color
        )
        embed.add_field(name="Reason", value=reason)
        embed.timestamp = datetime.now()
        embed.set_footer(text=f'User ID: {user.id}', icon_url=self.bot.user.avatar.url)

        await interaction.response.send_message(embed=embed)
        await user.ban(reason=reason)
        await interaction.guild.unban(user)

        if notify:
            embed = nextcord.Embed(
                title="Banned",
                description=f"You have been banned for the following reason:\n```\n{reason}\n```",
                color=embed_color
            )

            embed.timestamp = datetime.now()
            embed.set_footer(text=f'User ID: {user.id}', icon_url=self.bot.user.avatar.url)
            await user.send(embed=embed)

def setup(bot):
    bot.add_cog(SoftBan(bot))