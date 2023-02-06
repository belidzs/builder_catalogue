from typing import Any, List, Dict
import requests


class LegoApi():
    """Provides access to the LEGO API"""
    BASE_URL = "https://d16m5wbro86fg2.cloudfront.net/api"

    def get_user_id(self, name: str) -> str:
        """Returns the id based on the username"""
        url = f"{LegoApi.BASE_URL}/user/by-username/{name}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't determine user id by name")
        id = response.json()["id"]
        return id
    
    def get_user_details(self, id: str) -> Dict[Any, Any]:
        """Returns detailed information about a user"""
        url = f"{LegoApi.BASE_URL}/user/by-id/{id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't find user information")
        return response.json()
        
    def get_sets(self) -> List[Dict[Any, Any]]:
        """Returns a list of all available sets"""
        url = f"{LegoApi.BASE_URL}/sets"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't get list of sets")
        sets = response.json()["Sets"]
        return sets
    
    def get_set_details(self, id: str) -> Dict[Any, Any]:
        """Returns detailed information about a set"""
        url = f"{LegoApi.BASE_URL}/set/by-id/{id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't find set details")
        return response.json()
