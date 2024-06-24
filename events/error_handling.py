import nextcord 
from nextcord.ext import commands, application_checks
from main import embed_color, ThrowError

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, application_checks.errors.ApplicationMissingPermissions):
            missing_permissions = "\n• ".join(error.missing_permissions)
            await ThrowError(interaction=interaction, error=f"You do not have enough of the following permissions:\n```• {missing_permissions}\n```", error_type="Missing Permissions")
        elif isinstance(error, application_checks.errors.ApplicationBotMissingPermissions):
            missing_permissions = "\n• ".join(error.missing_permissions)
            await ThrowError(interaction=interaction, error=f"I do not have enough of the following permissions:\n```• {missing_permissions}```", error_type="Missing Permissions")
        elif isinstance(error, application_checks.errors.ApplicationNoPrivateMessage):
            await ThrowError(interaction=interaction, error="I cannot perform this command in dms.")
        elif isinstance(error, application_checks.errors.ApplicationNSFWChannelRequired):
            nsfw_channel = nextcord.Embed(
                title=f"Error: NSFW Command",
                description="You cannot use this command outside an age-restricted channel, please activate it in your channel settings.",
                color=embed_color
            )
            nsfw_channel.set_image(url="https://i.imgur.com/cuQq9cm.gif")
            await interaction.response.send_message(embed=nsfw_channel, ephemeral=True)
        elif isinstance(error, application_checks.errors.ApplicationNotOwner):
            await ThrowError(interaction=interaction, error=f"This command can only be used by my owner.", error_type="Owner Only")
        else:
            await ThrowError(interaction=interaction, error="I got an unknown error, please wait a few minutes and try again.", error_type="Unknown")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))