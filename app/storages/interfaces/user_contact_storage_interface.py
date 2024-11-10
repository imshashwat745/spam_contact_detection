from abc import ABC, abstractmethod
from typing import List
from ...dtos import SearchInfoDTO, ContactDTO


class UserContactStorageInterface(ABC):

    @abstractmethod
    def get_user_contacts_whose_name_starts_with(
        self, search_query
    ) -> List[SearchInfoDTO]:
        pass

    @abstractmethod
    def get_user_contacts_whose_name_contains_but_not_starts_with(
        self, search_query
    ) -> List[SearchInfoDTO]:
        pass

    @abstractmethod
    def get_user_contacts_having_contact(
        self, contact_dto: ContactDTO
    ) -> List[SearchInfoDTO]:
        pass

    @abstractmethod
    def does_contact_list_of_contact_has_current_user(
        self, jwt_contact_id: int, user_id: int
    ) -> bool:
        pass
