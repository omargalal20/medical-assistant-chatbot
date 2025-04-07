# Medical Q&A Assistant Backend

## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
- [Project Structure](#project-structure)

# Getting Started

### Prerequisites

- Python must be installed on local device. You can install it from
  the [Python installation guide](https://www.python.org/downloads/).
- uv must be installed, as it is used here as the dependency manager. You can install it from
  the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### Setup

1. **Clone the repository**
    - cd into backend:
      ``` 
      cd backend

2. **Create `.env` File:**
    - Create a `.env` file inside the `./app` directory, where it contains source code.
    - Add the following content to the `.env` file based on `.env.template`:
      ```
      ENVIRONMENT=
      APP_NAME=
      APP_VERSION=
3. **Setup virtual environment for the project**
    - Run in terminal:
      ``` 
      uv sync
      uv lock
    - After running commands this should create a .venv folder if not:
      ``` 
      uv venv
    - Choose the local python interpreter by selecting the current virtual environment in the used IDE.
    - Choose existing not generating new one, and select the following `.venv\Scripts\python.exe`.
4. **Run Project**
    - After setting up virtual environment enter the `./app` directory and run the main function in the `main.py`.

# **Project Structure**

The core application code is organized here. It adheres to the layered architecture, with each layer encapsulating
specific functionality.

## **business/**

Handles the application's business logic.

- **`clients/`**:  
  Contains integration logic for third-party services (e.g., authentication, LLM communication).  
  Example: `AuthenticationClient` and `LLMClient` for external API calls.

- **`dependencies.py`**:  
  Shared business dependencies such as client initializations or common business-level utility functions.

- **`mappers/`**:  
  Converts data structures between business logic and data layers.

- **`services/`**:  
  Contains core business logic. Service classes orchestrate workflows between clients, repositories, and other layers.

---

## **config/**

Handles application configuration.

- **`settings.py`**:  
  Manages application configuration settings (e.g., environment variables, API keys).

---

## **data/**

Deals with persistence and database-related logic.

- **`database/`**:  
  Database connection and session handling.

- **`models/`**:  
  ORM models (e.g., SQLAlchemy models) for database tables.

- **`repositories/`**:  
  Handles data access logic, isolating queries from the business logic.

---

## **presentation/**

Defines the presentation layer, including API routes, request/response validation, and middleware.

- **`dependencies.py`**:  
  Shared dependencies for request handling (e.g., authentication).

- **`mappers/`**:  
  Maps between request/response schemas and domain objects.

- **`middleware/`**:  
  Custom middleware for request/response lifecycle events.

- **`routers/`**:  
  Organizes API endpoints into modules.
    - **`v1/`**:  
      Versioned API routes for backward compatibility.

- **`schemas/`**:  
  Pydantic models for request and response validation.
    - **`request/`**:  
      Defines input validation schemas.
    - **`response/`**:  
      Defines output validation schemas.