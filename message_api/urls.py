from django.urls import path
from . import views

urlpatterns = [
    path('get/messages/<str:account_id>', views.get_messages, name='get-messages'),
    path('create', views.create_message, name='create-message'),
    path('search', views.search_messages, name='search-message'),
]
