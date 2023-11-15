from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Message

class MessageAPITests(APITestCase):

    def setUp(self):
        # Create some messages for testing
        Message.objects.create(account_id="111", sender_number="0987654321", receiver_number="1234567890")
        Message.objects.create(account_id="222", sender_number="0987654321", receiver_number="1234567890")

    def test_get_messages(self):
        """
        Ensure we can retrieve messages for a given account id.
        """
        url = reverse('get-messages', kwargs={'account_id':'111'})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_message(self):
        """
        Ensure we can create a new message object.
        """
        url = reverse('create-message')
        data = {
            'account_id': '333',
            'sender_number': '5555555555',
            'receiver_number': '6666666666',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(Message.objects.get(account_id='333').sender_number, '5555555555')

    def test_search_messages_by_sender_number(self):
        """
        Ensure we can search messages by sender number.
        """
        url = reverse('search-message') + '?sender_number=0987654321'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Since we have two messages with the same sender
        self.assertEqual(len(response.data['results']), 2)

    def test_search_messages_by_message_id(self):
        """
        Ensure we can search messages by message ID.
        """
        message = Message.objects.get(account_id="111")
        url = reverse('search-message') + f'?message_id={message.message_id}'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['message_id'], str(message.message_id))
    
    def test_search_messages_by_receiver_number(self):
        """
        Ensure we can search messages by sender number.
        """
        url = reverse('search-message') + '?receiver_number=1234567890'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Since we have two messages with the same sender
        self.assertEqual(len(response.data['results']), 2)
