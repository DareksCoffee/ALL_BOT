import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_embed(self, m):
        return len(m.embeds) > 0 and not m.content

    def has_attachment(self, m):
        return m.attachments

    def is_bot(self, m):
        return m.author == self.bot.user

    def is_user(self, m):
        return m.author != self.bot.user

    @nextcord.slash_command(name="purge", description="purge the chat")
    @application_checks.has_permissions(manage_channels=True, manage_messages=True)
    async def purge(self, interaction: nextcord.Interaction, amount: int):
        pass
    @purge.subcommand(name="any", description="Purge any messages.")
    @application_checks.has_permissions(manage_channels=True, manage_messages=True)
    async def _any(self, interaction: nextcord.Interaction, amount: int):
        """
        Purge any message.

        Parameters
        ----------
        amount:
            Enter the amount of message to delete.
        """
        message_deleted = await interaction.channel.purge(limit=amount)
        embed = nextcord.Embed(
            title="Success!",
            description=f"Successfully deleted `{amount}` messages.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed, delete_after=5)

    @purge.subcommand(name="attachments", description="delete messages that contains attachments")
    @application_checks.has_permissions(manage_channels=True, manage_messages=True)
    async def attachments(self, interaction: nextcord.Interaction, amount: int):
        """
        Purge messages that contains an attachment.

        Parameters
        ----------
        amount:
            Enter the amount of message to delete.
        """

        message_deleted = await interaction.channel.purge(limit=amount, check=self.has_attachment)
        embed = nextcord.Embed(
            title="Success!",
            description=f"Successfully deleted `{amount}` messages that contains attachments.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed, delete_after=5)

    @purge.subcommand(name="embed", description="delete messages that contains embed")
    @application_checks.has_permissions(manage_channels=True, manage_messages=True)
    async def embed(self, interaction: nextcord.Interaction, amount: int):
        """
        Purge messages that contains embed.

        Parameters
        ----------
        amount:
            Enter the amount of message to delete.
        """

        message_deleted = await interaction.channel.purge(limit=amount, check=self.is_embed)
        embed = nextcord.Embed(
            title="Success!",
            description=f"Successfully deleted `{amount}` messages that contains embed.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed, delete_after=5)
    @purge.subcommand(name="bot", description="delete bot messages")
    @application_checks.has_permissions(manage_channels=True, manage_messages=True)
    async def bot(self, interaction: nextcord.Interaction, amount: int):
        """
        Purge messages by bots.

        Parameters
        ----------
        amount:
            Enter the amount of message to delete.
        """
        message_deleted = await interaction.channel.purge(limit=amount, check=self.is_bot)
        embed = nextcord.Embed(
            title="Success!",
            description=f"Successfully deleted `{amount}` bot messages",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed, delete_after=5)
    @purge.subcommand(name="humans", description="Purge humans messages.")
    @application_checks.has_permissions(manage_channels=True, manage_messages=True)
    async def user(self, interaction: nextcord.Interaction, amount: int):
        """
        Purge messages sent by a human.

        Parameters
        ----------
        amount:
            Enter the amount of message to delete.
        """
        message_deleted = await interaction.channel.purge(limit=amount, check=self.is_user)
        embed = nextcord.Embed(
            title="Success!",
            description=f"Successfully deleted `{amount}` human messages.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed, delete_after=5)

def setup(bot):
    bot.add_cog(Purge(bot))