"""Provides access to the LEGO API."""
import requests
from typing import List
from model import DetailedSet, DetailedUser, Set, User, InventoryItem


class LegoApi():
    """Provides access to the LEGO API."""
    BASE_URL = "https://d16m5wbro86fg2.cloudfront.net/api"

    def get_users(self) -> List[User]:
        """Returns the list of all users."""
        url = f"{LegoApi.BASE_URL}/users"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't get users")
        result = []
        for user in response.json()["Users"]:
            result.append(User(user["id"], user["username"], user["brickCount"]))
        return result

    def get_user(self, username: str) -> User:
        """Returns information about a user by its username."""
        url = f"{LegoApi.BASE_URL}/user/by-username/{username}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't determine user id by name")
        user = response.json()
        return User(user["id"], user["username"], user["brickCount"])
    
    def get_user_details(self, id: str) -> DetailedUser:
        """Returns detailed information about a user by its id."""
        url = f"{LegoApi.BASE_URL}/user/by-id/{id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't find user information")
        user = response.json()
        collection ={}
        for piece in user["collection"]:
            for variant in piece["variants"]:
                collection[InventoryItem(piece["pieceId"], variant["color"])] = variant["count"]
        return DetailedUser(user["id"], user["username"], user["brickCount"], collection)
    
    def get_user_details_by_username(self, username:str) -> DetailedUser:
        return self.get_user_details(self.get_user(username).id)
        
    def get_sets(self) -> List[Set]:
        """Returns a list of all available sets."""
        url = f"{LegoApi.BASE_URL}/sets"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't get list of sets")
        result = []
        for set in response.json()["Sets"]:
            result.append(Set(set["id"], set["name"], set["totalPieces"]))
        return result
    
    def get_set(self, name: str) -> Set:
        """Returns a set by its name."""
        url = f"{LegoApi.BASE_URL}/set/by-name/{name}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't get set")
        set = response.json()
        return Set(set["id"], set["name"], set["totalPieces"])
    
    def get_set_details(self, id: str) -> DetailedSet:
        """Returns detailed information about a set."""
        url = f"{LegoApi.BASE_URL}/set/by-id/{id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't find set details")
        set = response.json()
        pieces = {}
        for piece in set["pieces"]:
            pieces[InventoryItem(piece["part"]["designID"], str(piece["part"]["material"]))] = piece["quantity"]
        return DetailedSet(set["id"], set["name"], set["totalPieces"], pieces)
    
    def get_set_details_by_name(self, name: str) -> DetailedSet:
        """Returns detailed information about a set based by its name."""
        return self.get_set_details(self.get_set(name).id)
