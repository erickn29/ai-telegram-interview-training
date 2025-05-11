# Bot Sobes TG

A Telegram bot for technical interview training with questions and answers across
various tech stacks.

## Features

- User authentication and profile management
- Training sessions with technical interview questions
- Multiple technology stacks to choose from
- Voice message to text conversion (speech recognition)
- Performance statistics and leaderboards
- LLM-assisted answering capabilities

## Tech Stack

- Python 3.12
- Aiogram 3.15.0 - Telegram Bot API framework
- SQLAlchemy 2.0 - ORM for database operations
- PostgreSQL - Database (via asyncpg and psycopg2)
- Alembic - Database migrations
- Redis - Caching
- Pydantic - Data validation and settings management
- SpeechRecognition - Voice message processing
- SQLAdmin - Admin interface

## Project Structure

- `src/` - Main source code
    - `handler/` - Bot command and callback handlers
        - `commands/` - Command handlers (start, auth, profile, etc.)
        - `callbacks/` - Callback query handlers
        - `messages/` - Message handlers
    - `utils/` - Helper utilities
        - `speech_to_text.py` - Voice message transcription
        - `text.py` - Text processing utilities
    - `core/` - Core functionality and configuration
    - `model/` - Database models
    - `repository/` - Data access layer
    - `service/` - Business logic layer
    - `schema/` - Pydantic models/schemas
    - `keyboard/` - Telegram keyboard layouts
    - `enums/` - Enumeration classes
    - `admin/` - Admin interface
- `tests/` - Test suite

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bot_sobes_tg.git
cd bot_sobes_tg
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Create and set up environment variables:

```bash
cp secrets/example.env secrets/.env
# Edit the .env file with your settings
```

4. Run database migrations:

```bash
cd src
alembic upgrade head
```

5. Start the bot:

```bash
poetry run python src/main.py
```

## Development

Development dependencies include:

- Black - Code formatter
- Ruff - Linter
- Bandit - Security linter
- Pytest - Testing framework

Run tests:

```bash
poetry run pytest
```

Format code:

```bash
poetry run black .
```

Lint code:

```bash
poetry run ruff check .
```

## License

[Add license information here]