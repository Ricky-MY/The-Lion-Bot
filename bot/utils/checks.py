from bot.constants import Admins

def is_admin(ctx) -> bool:
    return ctx.message.author.id in Admins.ID_LIST

def has_higher_role(member_1, member_2):
    return member_1.top_role > member_2.top_role