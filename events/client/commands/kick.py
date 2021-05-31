import discord
from vars.client import client
from helpers import notify

@client.command()
async def kick(ctx, Member: discord.Member = None):
    try:
        if not Member or Member == ctx.author:
            await notify.error(ctx, "No user found", None, 5)
            return
        if ctx.message.author.guild_permissions.kick_members:
            await ctx.guild.kick(Member)
            await notify.success(ctx, f'You have successfully banned the user {Member.display_name}!', None, 8)
        else:
            await notify.error(ctx, 'You are not allowed to ban here :( ', None, 5)
    except:
        notify.exception()
