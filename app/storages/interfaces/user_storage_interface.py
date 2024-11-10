from abc import ABC, abstractmethod
from typing import List
from ...dtos import UserDTO, SearchInfoDTO, ContactDTO
from ...models import User


class UserStorageInterface(ABC):

    @abstractmethod
    def does_user_exist(self, contact_id: int) -> bool:
        pass

    @abstractmethod
    def create_user(self, user_dto: UserDTO, contact_id: int) -> User:
        pass

    @abstractmethod
    def get_user(self, contact_id: int) -> User:
        pass

    @abstractmethod
    def get_users_whose_name_starts_with(self, search_query) -> List[SearchInfoDTO]:
        pass

    @abstractmethod
    def get_users_whose_name_contains_but_not_starts_with(
        self, search_query
    ) -> List[SearchInfoDTO]:
        pass

    @abstractmethod
    def get_user_having_contact(self, contact_dto: ContactDTO) -> SearchInfoDTO:
        pass
