import logging
from typing import Any, Dict, List, Tuple
from api import LegoApi    


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def flatten_pieces(pieces) -> Tuple[str, str, int]:
    """Returns the pieces as a tuple: (pieceId, color, count)"""
    for piece in pieces:
        for variant in piece["variants"]:
            yield (piece["pieceId"], variant["color"], variant["count"])

def get_buildable_sets(api: LegoApi, username: str) -> List[Dict[Any, Any]]:
    """Returns a list of sets the user can build"""
    # get user
    id = api.get_user_id(username)
    user = api.get_user_details(id)
    
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

    result = []
    for set in filtered_sets:
        full_set = api.get_set_details(set["id"])
        buildable = True
        for piece in full_set["pieces"]:
            if (piece["part"]["designID"], str(piece["part"]["material"])) not in inventory.keys():
                buildable = False
                break
            if inventory[(piece["part"]["designID"], str(piece["part"]["material"]))] < piece["quantity"]:
                buildable = False
                break
        if buildable:
            result.append(set)
    return result


if __name__ == "__main__":
    api = LegoApi()
    username = "brickfan35"
    result = get_buildable_sets(api, username)
    logger.info(f"{username} can build the following sets: {[x['name'] for x in result]}")
