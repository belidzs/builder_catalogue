import logging
import bisect
import math
from typing import List
from api import LegoApi
from model import DetailedSet, DetailedUser, Set, User
from copy import copy


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_buildable_sets(api: LegoApi, user: DetailedUser) -> List[Set]:
    """Returns a list of sets the user can build on their own."""
    # get user
    sets = api.get_sets()
    
    # first approach: keep only those sets which require less than or equal number of pieces than the user has
    filtered_sets: List[Set] = []
    for set in sets:
        if set.brick_count <= user.brick_count:
            filtered_sets.append(set)

    logger.debug(f"Eliminated {len(sets) - len(filtered_sets)} sets due to total piece count constraints")

    # loop through the remaining sets
    result = []
    for set in filtered_sets:
        set_details = api.get_set_details(set.id)
        if set_details.is_buildable(user.collection):
            result.append(set)
    return result

def find_build_partner(api: LegoApi, user: DetailedUser, set: DetailedSet) -> List[DetailedUser]:
    """Returns a list of users who have the proper bricks to build the desired set together with the provided user."""
    partners = []
    for partner in api.get_users():
        if partner.id == user.id:
            continue

        # build common inventory with the partner candidate
        partner_detail = api.get_user_details(partner.id)
        common_inventory = copy(user.collection)
        for piece in partner_detail.collection:
            if piece in common_inventory:
                common_inventory[piece] += partner_detail.collection[piece]
            else:
                common_inventory[piece] = partner_detail.collection[piece]

        # check whether the common inventory is sufficient to build the desired set
        if set.is_buildable(common_inventory):
            partners.append(partner_detail)
    return partners

def median(api: LegoApi, asking_user: User) -> int:
    """Returns the number of bricks at least 50% of all users have, excluding the asking user."""
    users = api.get_users()
    if len(users) == 1:
        # the only user is the asking user
        return 0
    brick_counts = []
    for user in users:
        if user.id == asking_user.id:
            continue
        bisect.insort(brick_counts, user.brick_count)
    logger.debug(brick_counts)
    index = int(math.floor(len(brick_counts) / 2))
    return(brick_counts[index])


if __name__ == "__main__":
    api = LegoApi()

    # main challenge
    user = api.get_user_details_by_username("brickfan35")
    result = get_buildable_sets(api, user)
    logger.info(f"{user.username} can build the following sets: {[set.name for set in result]}")
    
    # first stretch goal
    user = api.get_user_details_by_username("landscape-artist")
    set = api.get_set_details_by_name("tropical-island")
    result = find_build_partner(api, user, set)
    logger.info(f"{user.username} can partner up with the following users to build {set.name}: {[partner.username for partner in result]}")

    # second stretch goal
    user = api.get_user("megabuilder99")
    result = median(api, user)
    logger.info(f"{user.username} should build their custom set with a size <= {result} in order to at least 50% of the users have more bricks than required")
