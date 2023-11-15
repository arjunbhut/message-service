
# Message Service

## Description
Message Service is a Django-based application designed to provide a robust messaging API. This project leverages the power and flexibility of Django to create an efficient and scalable messaging platform.

## Installation
To set up Message Service on your local machine, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Virtual Environment**: It's recommended to create a virtual environment for this project to manage dependencies. You can use `virtualenv` or `conda` to create one.
3. **Install Dependencies**: Run `pip install -r requirements.txt` to install the required Python dependencies.
4. **Initial Setup**: In settings.py update the Database config, Navigate to the project directory and run `python manage.py migrate` to set up the initial database schema.

## Usage
To run the Message Service:

1. **Start the Django Server**: Execute `python manage.py runserver` from the project directory. This will start the local development server.
2. **Access the Application**: The service will be available at `http://localhost:8000`.

## API Endpoints
The following API endpoints are available in this project:
- **/get/messages/<account_id>**: Returns all the messages with the sender and
receiver details pertaining to the provided account id.
- **/create**: Post call which saves the message with the sender and receiver
details.
- Search for keys using the following filters.
Assume you have keys: message_id, sender_number, receiver_number
- **/search?message_id=”1,2”** would return messages with the given
message ids.
- **/search?sender_number=”1,2”** would return messages with the given
sender_number - can single sender number or multiple sender numbers
under a given account ID.
- **/search?receiver_number=”1,2”** would return messages with the given
receiver_number - can single sender number or multiple receiver
numbers

## Docker Support
If you prefer to use Docker:

1. **Build the Docker Image**: Run `docker build -t message_service .` in the project directory.
2. **Run the Docker Container**: Execute `docker run -p 8000:8000 message_service`.
