# Book Exchange System

## Overview
The Book Exchange System is a robust platform that allows users to register, add books, and exchange them with other users. It utilizes a relational database for persistent storage and Kafka for real-time event processing.

## Architecture and Design Patterns

The system implements several design patterns and architectural principles:

1. **Service-Oriented Architecture (SOA)**: The system is divided into distinct services (UserService, BookService, ExchangeService, etc.), each responsible for a specific domain of functionality.

2. **Repository Pattern**: Used in database interactions, abstracting the data persistence layer from the business logic.

3. **Factory Pattern**: Implemented in the creation of database connections and Kafka producers/consumers.

4. **Observer Pattern**: Utilized through the Kafka messaging system, where services can publish events (e.g., book added) and other parts of the system can subscribe to and react to these events.

5. **Singleton Pattern**: Applied to service classes to ensure a single instance is used throughout the application.

6. **Command Pattern**: Implemented in the Kafka message handling, where different actions (add_book, update_book, etc.) are encapsulated as commands.

7. **Model-View-Controller (MVC)**: Although not explicitly implemented (as there's no UI), the system's structure separates data models, business logic (controllers), and data presentation.

## Key Components

1. **User Management**: Handles user registration and profile management.
2. **Book Management**: Manages adding, updating, and retrieving books.
3. **Exchange System**: Facilitates book exchanges between users.
4. **Kafka Integration**: Provides real-time event processing and system updates.
5. **Database Layer**: Manages persistent storage of user, book, and exchange data.

## Technologies Used

- Python: Primary programming language
- PostgreSQL: Relational database for data persistence
- Kafka: Message broker for event-driven architecture
- psycopg2: PostgreSQL adapter for Python
- confluent_kafka: Kafka client for Python

## Key Features

1. User registration with duplicate prevention
2. Book management (add, update, retrieve) with ISBN-based deduplication
3. Book exchange functionality
4. Real-time event processing using Kafka
5. Persistent data storage using PostgreSQL

## Future Enhancements

1. User authentication and authorization
2. Advanced search and recommendation features
3. User and book rating system
4. Transaction management for book exchanges
5. Frontend interface for user interaction

## Running the System

1. Ensure PostgreSQL and Kafka are installed and running.
2. Set up the database and Kafka topics as specified in the configuration files.
3. Install required Python packages: `pip install psycopg2 confluent_kafka`
4. Run the main script: `python main.py`

## Testing

The system includes a basic test suite in `main.py` that demonstrates core functionalities including user registration, book management, and exchange creation.