from abc import ABC, abstractmethod
from ...dtos import ContactDTO
from ...models import Contact


class ContactStorageInterface(ABC):

    @abstractmethod
    def does_contact_exist(self, contact_dto: ContactDTO) -> bool:
        pass

    @abstractmethod
    def create_contact(self, contact_dto: ContactDTO) -> Contact:
        pass

    @abstractmethod
    def get_contact(self, contact_dto: ContactDTO) -> Contact:
        pass
