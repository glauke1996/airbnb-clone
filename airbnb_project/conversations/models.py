from django.db import models
from core import models as core_models

# Create your models here.
class Conversation(core_models.AbstractTimeStampedModel):
    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_message(self):
        return self.messages.count()

    count_message.short_description = "Number Of Message"

    def count_participants(self):
        return self.messages.count()

    count_participants.short_description = "Number Of Participants"


class Message(core_models.AbstractTimeStampedModel):
    text = models.TextField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="messages"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    def __str__(self):
        return str(self.text)
