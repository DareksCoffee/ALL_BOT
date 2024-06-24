import requests
import nextcord
from main import embed_color, TOKEN
from emojis import Emojis
from nextcord.ext import commands

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(name="user", description="user")
    async def user(self, interaction: nextcord.Interaction):
        pass

    @user.subcommand(name="avatar", description="Get the avatar of the user")
    async def avatar(self, interaction: nextcord.Interaction, user: nextcord.Member):
        """
        Returns the avatar of the user

        Parameters
        ----------
        user:
            Enter the guild member.
        """
        embed = nextcord.Embed(
            title=f"{user.name}'s avatar",
            color=embed_color
        )
        embed.set_image(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)
    @user.subcommand(name="banner", description="Get the banner of the user")
    async def banner(self, interaction: nextcord.Interaction, user: nextcord.Member):
        req = await self.bot.http.request(nextcord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]

        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
            embed = nextcord.Embed(
                title=f"{user.name}'s banner",
                color=embed_color
            )
            embed.set_image(url=banner_url)
            await interaction.response.send_message(embed=embed) 
        else:   
            await interaction.response.send_message(f"{user.name} does not have a banner.") 
    @user.subcommand(name="info", description="Information regarding the user")
    async def info(self, interaction: nextcord.Interaction, user: nextcord.User):
        """
        Returns informations regarding the guild member.

        Parameters
        ----------
        user:
            Enter the guild member.
        """
        isOwner = False
        if str(user.id) == "419463672700600322":
            isOwner = True
        emojis = Emojis()
        badge_icons = {
            'staff': emojis.staff_badge,
            'partner': emojis.partner,
            'bug_hunter': emojis.bug_hunter,
            'hypesquad_bravery': emojis.purple_hyped,
            'hypesquad_brilliance': emojis.red_hyped,
            'hypesquad_balance': emojis.green_hyped,
            'early_supporter': emojis.early_supporter,
            'verified_bot_developer': emojis.verified_dev,
            "active_developer": emojis.active_dev 
        }
        description = f"Informations regarding the account of {user.mention}" if not isOwner else "This user is the owner of ALL"
        badge_text = ""
        for badge, emoji in badge_icons.items():
            if getattr(user.public_flags, badge):
                badge_text += f"{emoji} "
        req = await self.bot.http.request(nextcord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        embed = nextcord.Embed(
            title=f"{user.global_name}'s Information",
            description=description,
            color=embed_color
        )
        embed.add_field(name="Badges", value=badge_text if badge_text else "No badges",inline=False)
        embed.add_field(name="Joined Discord", value=user.created_at.strftime("%B %d, %Y"),inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%B %d, %Y") if user.joined_at else "Not in server",inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
            embed.set_image(url=banner_url)

        roles = [f"<@&{role.id}>" for role in sorted(user.roles[1:], reverse=True, key=lambda r: r.position)]
        roles_text = "\n".join(roles)
        embed.add_field(name=f"Roles[{len(roles)}]", value=roles_text if roles_text else "No roles",inline=False)
        if user.activity:
            embed.add_field(name=f"Activity", value=user.activity.name)
        embed.set_footer(text=f"ID : {user.id}")
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(User(bot))