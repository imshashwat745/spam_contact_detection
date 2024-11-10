from django.db import models

# Create your models here.


class Contact(models.Model):
    country_code = models.IntegerField()
    phone_number = models.IntegerField()
    spam_marked_by = models.ManyToManyField(
        "User", through="SpamDetails", related_name="marked_spam"
    )

    class Meta:
        unique_together = ["country_code", "phone_number"]

    def __str__(self):
        return f"{self.country_code} - {self.phone_number}"


class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, unique=True)
    password = models.BinaryField(max_length=500, null=True)
    email = models.EmailField(null=True, blank=True)

    contacts = models.ManyToManyField(
        Contact, through="UserContact", related_name="users"
    )

    def __str__(self):
        return self.name


class UserContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)

    class Meta:
        unique_together = ["user", "contact"]

    def __str__(self):
        return f"{self.user.name} - {self.contact.phone_number}"


class SpamDetails(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["marked_by", "contact"]

    def __str__(self):
        return f"{self.marked_by.name} - {self.contact.phone_number}"
