import typing
import uuid
import collections

import discord

from cogs.utils.profiles.field import Field


class Profile(object):
    """A class for an abstract template object that's saved to guild
    This contains no user data, but rather the metadata for the template itself
    """

    all_profiles: typing.Dict['profile_id', 'Profile'] = {}
    all_guilds: typing.Dict['guild_id', typing.Dict['name', 'Profile']] = collections.defaultdict(dict)

    __slots__ = ("profile_id", "colour", "guild_id", "verification_channel_id", "name", "archive_channel_id")

    def __init__(self, profile_id:uuid.UUID, colour:int, guild_id:int, verification_channel_id:int, name:str, archive_channel_id:int):
        self.profile_id = profile_id
        self.colour = colour
        self.guild_id = guild_id
        self.verification_channel_id = verification_channel_id
        self.name = name
        self.archive_channel_id = archive_channel_id

        self.all_profiles[self.profile_id] = self
        self.all_guilds[self.guild_id][self.name] = self

    @property
    def fields(self) -> typing.List[Field]:
        """Returns a list of cogs.utils.profiles.fields.Field objects for this particular profile"""

        try:
            return [i for i in sorted(Field.all_profile_fields.get(self.profile_id), key=lambda x: x.index) if i.deleted is False]
        except TypeError:
            return list()

    def get_profile_for_member(self, member:typing.Union[discord.Member, int]) -> 'cogs.utils.profiles.user_profile.UserProfile':
        """Gets the filled profile for a given member"""

        from cogs.utils.profiles.user_profile import UserProfile
        member_id = getattr(member, 'id', member)
        return UserProfile.all_profiles.get((member_id, self.guild_id, self.name))
