import logging
from uuid import UUID
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Message
from .serializers import MessageSerializer

# Configure logger for this module
logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_messages(request, account_id):
    """
    Retrieve messages for a specific account_id with pagination to handle large datasets.
    """
    try:
        # Initialize pagination
        paginator = PageNumberPagination()
        paginator.page_size = 50  # Or another suitable page size

        # Try to get messages for a given account_id using pagination
        messages_queryset = Message.objects.filter(account_id=account_id)
        
        # Check if messages exist before serialization
        if not messages_queryset.exists():
            logger.info('No messages found for account_id %s', account_id)
            return Response({'detail': 'No messages found for this account.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Paginate the queryset
        paginated_messages = paginator.paginate_queryset(messages_queryset, request)
        serializer = MessageSerializer(paginated_messages, many=True)
        
        # Return the paginated responses
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        logger.error('An error occurred while retrieving messages for account_id %s: %s', account_id, e, exc_info=True)
        return Response({'detail': 'An error occurred processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_message(request):
    """
    Create a new message with the provided data.
    """
    serializer = MessageSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info('Message created successfully with data: %s', request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.warning('Failed to create message with data: %s', request.data)
        logger.warning('Errors: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_messages(request):
    """
    API view to search messages based on message_id, sender_number, and receiver_number.
    Implements pagination to handle large datasets efficiently.
    """
    try:
        # Initialize pagination
        paginator = PageNumberPagination()
        paginator.page_size = 100  # Adjust the page size to suit your needs

        # Filter the queryset based on query parameters
        queryset = Message.objects.all()
        query_params = request.query_params

        message_ids = query_params.get('message_id')
        sender_number = query_params.get('sender_number')
        receiver_number = query_params.get('receiver_number')
      
        # Build the filters before evaluating the queryset
        if message_ids:
            message_ids = message_ids.strip('"')
            message_id_list = message_ids.split(',')
            valid_message_ids = []
            for mid in message_id_list:
                try:
                    valid_uuid = UUID(mid, version=4)
                    valid_message_ids.append(valid_uuid)
                except ValueError:
                    return Response({'error': f'Invalid message_id: {mid}'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(message_id__in=valid_message_ids)
        if sender_number:
            sender_numbers = sender_number.strip('"')
            sender_number_list = sender_numbers.split(',')
            queryset = queryset.filter(sender_number__in=sender_number_list)
        if receiver_number:
            receiver_numbers = receiver_number.strip('"')
            receiver_number_list = receiver_numbers.split(',')
            queryset = queryset.filter(receiver_number__in=receiver_number_list)
            

        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If page is None, which means pagination is not applied due to empty page or any other reason
        logger.info('No messages found matching the search criteria.')
        return Response({'detail': 'No messages found matching the search criteria.'}, status=status.HTTP_404_NOT_FOUND)

    except ValueError as ve:
        # Handle specific error like ValueError for invalid query parameters
        logger.error('ValueError: %s', ve)
        return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # For any other exceptions, log the error and return a 500 response
        logger.exception('An unexpected error occurred.')
        return Response({'detail': 'An error occurred processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
