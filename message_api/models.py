from django.db import models
import uuid

# Create your models here.
class Message(models.Model):
    account_id = models.CharField(max_length=100)
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender_number = models.CharField(max_length=50)
    receiver_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender_number} to {self.receiver_number}"