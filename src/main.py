import logging
from typing import Any, Dict, List, Tuple
from api import LegoApi  


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def flatten_pieces(pieces: Dict[str, Any]) -> Tuple[str, str, int]:
    """Returns owned pieces flattened to a tuple in the following format: (pieceId, color, count)"""
    for piece in pieces:
        for variant in piece["variants"]:
            yield (piece["pieceId"], variant["color"], variant["count"])

def is_buildable(set, inventory: Dict[Tuple[str, str, int], int]) -> bool:
    """Determines whether a set could be built by using the inventory provided"""
    buildable = True
    for piece in set["pieces"]:
        if (piece["part"]["designID"], str(piece["part"]["material"])) not in inventory.keys():
            # if user doesn't have a necessary piece, the set can't be built, so we break out from the cycle
            buildable = False
            break
        if inventory[(piece["part"]["designID"], str(piece["part"]["material"]))] < piece["quantity"]:
            # if user has less than the necessary amount of a piece, the set can't be built, so we break out from the cycle
            buildable = False
            break
    return buildable

def get_buildable_sets(api: LegoApi, username: str) -> List[Dict[str, Any]]:
    """Returns a list of sets the user can build"""
    # get user
    user = api.get_user_details_by_username(username)
    
    # build an inventory which can be searched in O(1)
    inventory = {}
    for piece in flatten_pieces(user["collection"]):
        inventory[(piece[0], piece[1])] = piece[2]

    sets = api.get_sets()
    
    # first approach: keep only those sets which require less than or equal number of pieces than the user has
    filtered_sets = []
    for set in sets:
        if set["totalPieces"] <= user["brickCount"]:
            filtered_sets.append(set)

    logger.debug(f"Eliminated {len(sets) - len(filtered_sets)} sets due to total piece count constraints")

    # loop through the remaining sets
    result = []
    for set in filtered_sets:
        set_details = api.get_set_details(set["id"])
        if is_buildable(set_details, inventory):
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
    #result = get_buildable_sets(api, username)
    #logger.info(f"{username} can build the following sets: {[x['name'] for x in result]}")
    username = "landscape-artist"
    set = "tropical-island"
    result = find_build_partner(api, username, set)
    print(result)
