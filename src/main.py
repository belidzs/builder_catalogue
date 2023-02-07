import logging
from typing import Any, List
from api import LegoApi
from model import Set  


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_buildable_sets(api: LegoApi, username: str) -> List[Set]:
    """Returns a list of sets the user can build"""
    # get user
    user = api.get_user_details_by_username(username)
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

def find_build_partner(api: LegoApi, username: str, set: str) -> List[Any]:
    user = api.get_user_details(api.get_user_id(username))
    partners = []
    for user in api.get_users():
        user_detail = api.get_user_details(user["id"])
        print(user_detail)


if __name__ == "__main__":
    api = LegoApi()
    username = "brickfan35"
    result = get_buildable_sets(api, username)
    logger.info(f"{username} can build the following sets: {[set.name for set in result]}")
    username = "landscape-artist"
    set = "tropical-island"
    #result = find_build_partner(api, username, set)
