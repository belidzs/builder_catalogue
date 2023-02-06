"""Provides access to the LEGO API"""
import requests
from typing import Any, List, Dict


class LegoApi():
    """Provides access to the LEGO API"""
    BASE_URL = "https://d16m5wbro86fg2.cloudfront.net/api"

    def get_users(self) -> List[Dict[str, Any]]:
        """Returns the list of users"""
        url = f"{LegoApi.BASE_URL}/users"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't get users")
        return response.json()["Users"]

    def get_user_id(self, username: str) -> str:
        """Returns the id based on the username"""
        url = f"{LegoApi.BASE_URL}/user/by-username/{username}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't determine user id by name")
        id = response.json()["id"]
        return id
    
    def get_user_details(self, id: str) -> Dict[str, Any]:
        """Returns detailed information about a user"""
        url = f"{LegoApi.BASE_URL}/user/by-id/{id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't find user information")
        return response.json()
    
    def get_user_details_by_username(self, username:str) -> Dict[str, Any]:
        return self.get_user_details(self.get_user_id(username))
        
    def get_sets(self) -> List[Dict[str, Any]]:
        """Returns a list of all available sets"""
        url = f"{LegoApi.BASE_URL}/sets"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't get list of sets")
        sets = response.json()["Sets"]
        return sets
    
    def get_set_details(self, id: str) -> Dict[str, Any]:
        """Returns detailed information about a set"""
        url = f"{LegoApi.BASE_URL}/set/by-id/{id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("Couldn't find set details")
        return response.json()
