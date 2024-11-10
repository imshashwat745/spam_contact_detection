from ..interfaces.spam_details_storage_interface import SpamDetailsStorageInterface
from app.dtos import SpamDetailsDTO
from app.models import SpamDetails, User, Contact


class SpamDetailsStorageImpl(SpamDetailsStorageInterface):

    def mark_contact_as_spam(self, spam_details_dto: SpamDetailsDTO) -> bool:
        user = User.objects.get(id=spam_details_dto.marked_by)
        contact = Contact.objects.get(id=spam_details_dto.contact_id)

        spam_details, created = SpamDetails.objects.get_or_create(
            marked_by=user, contact=contact
        )

        if created:
            return spam_details
        else:
            return False

    def get_count_of_spam(self, contact_id: int) -> int:
        count = SpamDetails.objects.filter(contact_id=contact_id).count()

        return count
