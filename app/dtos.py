from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    name: str
    password: str
    contact_id: int
    email: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class ContactDTO:
    country_code: int
    phone_number: int
    contact_id: Optional[int] = None


@dataclass
class UserContactDTO:
    user_id: int
    contact_id: int
    user_contact_id: Optional[int] = None


@dataclass
class SpamDetailsDTO:
    contact_id: int
    marked_by: int
    id: Optional[int] = None


@dataclass
class SearchInfoDTO:
    name: str
    country_code: int
    phone_number: int
    contact_id: int
    user_id: Optional[int] = None
    spam_count: Optional[int] = 0
    email: Optional[str] = None

    def __eq__(self, other):
        if isinstance(other, SearchInfoDTO):
            return (
                self.name == other.name
                and self.user_id == other.user_id
                and self.contact_id == other.contact_id
                and self.country_code == other.country_code
                and self.phone_number == other.phone_number
            )
        return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.user_id,
                self.contact_id,
                self.country_code,
                self.phone_number,
            )
        )
