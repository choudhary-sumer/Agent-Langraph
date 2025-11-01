# Agent POC - LangGraph + FastAPI

A single-agent architecture built with LangGraph and FastAPI that supports multi-turn conversations with short-term memory.

## Features

- **Single Agent Architecture**: Uses LangGraph's `create_react_agent` for agent creation
- **Multi-turn Conversations**: Maintains conversation history and context
- **Structured Output**: Returns both JSON and natural language responses
- **Modular Design**: Clean separation of concerns across different modules
- **FastAPI Integration**: RESTful API with automatic documentation
- **Memory Management**: Conversation memory with cleanup capabilities

## Project Structure

```
agent_poc/
├── app/
│   ├── agent/           # Agent creation and management
│   ├── api/             # FastAPI endpoints
│   ├── memory/          # Conversation memory
│   ├── models/          # Pydantic models
│   ├── prompts/         # Prompt templates
│   └── tools/           # Agent tools
├── tests/               # Test files
├── main.py             # Application entry point
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Tools Available

1. **fetch_account_details** - Retrieve account related information
2. **fetch_facility_details** - Retrieve facility related information  
3. **save_notes** - Save MOM or notes given by user
4. **fetch_notes** - Retrieve notes based on user_id/date/last 5 notes

## Response Format

The agent returns structured responses with:

- `conversation_id`: Unique conversation identifier
- `final_response`: Human-friendly natural language response
- `card_key`: UI card type (`account_overview`, `facility_overview`, `notes_overview`, `other`)
- `account_overview`: Account details array
- `facility_overview`: Facility details array
- `note_overview`: Notes array

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database setup**: Not required.
   - The app now runs entirely in in-memory mode for conversations and uses `app/data/mock_store.py` for mock data.
   - You can skip any PostgreSQL installation or migration steps.

3. **Set Environment Variables**:
   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key
   # Only OPENAI_API_KEY is required (database settings are not used)
   ```

4. **Initialize**: No database initialization required - the app runs in in-memory mode.

5. **Run the Application**:
   ```bash
   python start_server.py
   ```

   Or with uvicorn directly:
   ```bash
   uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /chat` - **Main endpoint for all tool testing** (accounts, facilities, notes)
- `GET /conversations/{conversation_id}` - Get conversation info
- `DELETE /conversations/{conversation_id}` - Delete conversation
- `GET /conversations` - List all conversations
- `POST /cleanup` - Clean up old conversations

## Data Structure

The application uses in-memory mock data storage:

- **Mock Data Store**: `app/data/mock_store.py` - Centralized in-memory storage for accounts, facilities, and notes
- **Conversation Memory**: In-memory storage (no database required)
- **Mock Data**: Pre-seeded with sample accounts, facilities, and notes for testing

All tools read from and write to the mock store. Conversation memory is maintained in-memory during the server session.

## Example Usage

### API Request Format

The `/chat` endpoint accepts the following request format:

**Account Overview Request:**
```json
{
  "text": "show account overview",
  "user_id": "kaushal.sethia.c@evolus.com",
  "title": "sample",
  "account_id": "A-011977763"
}
```

**Fetch Account Details:**
```json
{
  "text": "fetch account details",
  "user_id": "3867",
  "title": "postman_test",
  "account_id": "A-011977763"
}
```

**Fetch Facility Details:**
```json
{
  "text": "fetch facility details",
  "user_id": "3867",
  "title": "postman_test",
  "account_id": "A-011977763",
  "facility_id": "F-013203268"
}
```

**Follow-up Question:**
```json
{
  "text": "how many points do I need to go to next tier",
  "user_id": "kaushal.sethia.c@evolus.com", 
  "title": "sample",
  "account_id": "A-011977763",
  "conversation_id": "c625fbc7-cc93-4a7e-841b-180872a9420a"
}
```

## Development

For development, install additional dependencies:

```bash
pip install -r requirements-dev.txt
```

Set up pre-commit hooks:

```bash
pre-commit install
```

## Postman Collection

A Postman collection is provided (`postman_collection.json`) with pre-configured requests for easy testing. Import this collection into Postman to test all endpoints.

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

The application can be configured through environment variables in `.env`:

### Application Settings
- `OPENAI_API_KEY`: Your OpenAI API key **(required)**
- `MODEL_NAME`: Model to use (default: gpt-4o-mini)
- `DEBUG`: Enable debug mode (default: false)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `WORKERS`: Number of workers (default: 1)
- `RELOAD`: Enable auto-reload (default: false)

**Note**: No database configuration is needed. The application runs entirely in-memory for both conversation memory and mock data.

## Development

The codebase follows a modular architecture:

- **Tools**: Implemented as LangChain tools with proper schemas
- **Prompts**: Structured prompts with JSON schema enforcement
- **Memory**: Conversation memory with cleanup capabilities
- **Models**: Pydantic models for request/response validation
- **API**: FastAPI with proper error handling and documentation

## Notes

- **Mock Data**: The application uses in-memory mock data from `mock_store.py` for testing
- **No Database**: All data (conversations and business data) is stored in-memory during the session
- **Testing**: Use the `/chat` endpoint for all tool testing (account, facility, notes operations)
- **Conversation ID**: Omit `conversation_id` in the first request to get one auto-generated, then use it for multi-turn conversations
- **Production**: In production, replace mock data with actual API calls and implement persistent storage
- Configure CORS settings appropriately for your frontend
- Set up proper logging and monitoring for production use
