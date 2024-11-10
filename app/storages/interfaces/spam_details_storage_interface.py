from abc import ABC, abstractmethod
from ...dtos import SpamDetailsDTO
from ...models import SpamDetails


class SpamDetailsStorageInterface(ABC):

    @abstractmethod
    def mark_contact_as_spam(self, spam_details_dto: SpamDetailsDTO) -> bool:
        pass

    @abstractmethod
    def get_count_of_spam(self, contact_id: int) -> int:
        pass
