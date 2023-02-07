"""Describes the data structures used in the LEGO Code Challenge."""
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class InventoryItem():
    """An InventoryItem is a brick identified by its design number and its color."""
    design_id: str
    color: str


@dataclass()
class User():
    """A user."""
    id: str
    username: str
    brick_count: int


@dataclass()
class DetailedUser(User):
    """A user complete with their brick inventory."""
    collection: Dict[InventoryItem, int]


@dataclass()
class Set():
    """A set to be built."""
    id: str
    name: str
    brick_count: int    


@dataclass()
class DetailedSet(Set):
    """A set to be built complete with the required pieces."""
    pieces: Dict[InventoryItem, int]

    def is_buildable(self, provided_pieces: Dict[InventoryItem, int]):
        """Determines whether a set could be built using only the provided pieces"""
        buildable = True
        for set_piece in self.pieces:
            if set_piece not in provided_pieces:
                # if user doesn't have a necessary piece, the set can't be built, so we break out from the cycle
                buildable = False
                break
            if provided_pieces[set_piece] < self.pieces[set_piece]:
                # if user has less than the necessary amount of a piece, the set can't be built, so we break out from the cycle
                buildable = False
                break
        return buildable