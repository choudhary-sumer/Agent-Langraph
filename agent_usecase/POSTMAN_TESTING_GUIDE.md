# Postman Testing Guide for Agent POC API

**Base URL**: `http://localhost:8000` (or `http://localhost:8001` if you configured it)

**Note**: No session creation needed! `conversation_id` is optional and will be auto-generated if omitted.

---

## Endpoint Overview

- **POST** `/chat` - **Single endpoint for all tool testing** (accounts, facilities, notes)
- **GET** `/health` - Health check
- **GET** `/conversations` - List all conversations
- **GET** `/conversations/{conversation_id}` - Get conversation stats
- **DELETE** `/conversations/{conversation_id}` - Delete a conversation

---

## Step 1: Initial Request (Get conversation_id)

**First Request** - Omit `conversation_id` to get one auto-generated:

**URL**: `POST http://localhost:8000/chat`

**Body** (JSON):
```json
{
  "text": "show account overview",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Testing",
  "account_id": "A-011977763"
}
```

**Response** will include `conversation_id` in the response. Copy it for subsequent requests.

**Example Response**:
```json
{
  "conversation_id": "abc123-def456-...",
  "final_response": "...",
  "card_key": "account_overview",
  ...
}
```

---

## Tool Testing - All Scenarios

### 1. fetch_account_details (Account Overview)

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "show account overview",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Account Overview Test",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: `card_key = "account_overview"` with account data in response.

---

### 2. fetch_facility_details (Facility by ID)

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "show facility overview for facility F-015766066",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Facility Test",
  "account_id": "A-011977763",
  "facility_id": "F-015766066",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Alternative** (without facility_id in body, let agent infer):
```json
{
  "text": "show facility overview",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Facility Test",
  "account_id": "A-011977763",
  "facility_id": "F-015766066",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: `card_key = "facility_overview"` with facility data.

---

### 3. save_notes - Simple Note

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "save note: Met with Dimod Account. Discussed status.",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Save Note Test",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: `card_key = "notes_overview"` or `"other"`, success message.

---

### 4. save_notes - Multi-line Note

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "save note:\n- Discussed loyalty points.\n- Agreed to follow up on facility license by Friday.\n- Owner prefers email.",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Multi-line Note",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

---

### 5. save_notes - Note with Title/Context

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "save note (title: Facility F-015766066): Confirmed renewal path and shipping address.",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Facility Note",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

---

### 6. save_notes - Validation Test (Missing Content)

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "save note",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Validation Test",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: `card_key = "other"`, `final_response` asks for note content.

---

### 7. fetch_notes - All Notes for Account

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "fetch all notes",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Fetch Notes",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: `card_key = "notes_overview"`, array of notes in `note_overview`.

---

### 8. fetch_notes - Last N Notes

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "fetch last 2 notes",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Fetch Last N",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: Returns only the 2 most recent notes.

---

### 9. fetch_notes - By Date (DD/MM/YYYY format)

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "fetch notes for 29/10/2025",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "Fetch by Date",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: Returns notes matching the date (if any exist in mock_store).

---

### 10. fetch_facility_details - All Facilities for Account

**URL**: `POST http://localhost:8000/chat`

**Body**:
```json
{
  "text": "show all facilities for this account",
  "user_id": "sumer.choudhary@bitcot.com",
  "title": "All Facilities",
  "account_id": "A-011977763",
  "conversation_id": "<YOUR_CONVERSATION_ID>"
}
```

**Expected**: `card_key = "facility_overview"` with multiple facilities.

---

## Testing Tips

1. **First Request**: Omit `conversation_id` - you'll get one in the response.
2. **Subsequent Requests**: Include the `conversation_id` to maintain conversation context.
3. **Multi-turn Testing**: Use the same `conversation_id` for follow-up questions.
4. **Mock Data Available**:
   - Account: `A-011977763` (Dimod Account)
   - Facilities: `F-013203268` (TEST Delete Facility), `F-015766066` (Diamond Facility)
   - Pre-seeded notes exist for users: `sumer.choudhary@bitcot.com`, `kaushal.sethia.c@evolus.com`

---

## Conversation Management Endpoints

### List All Conversations
**URL**: `GET http://localhost:8000/conversations`

### Get Conversation Stats
**URL**: `GET http://localhost:8000/conversations/{conversation_id}`

### Delete Conversation
**URL**: `DELETE http://localhost:8000/conversations/{conversation_id}`

---

## Health Check

**URL**: `GET http://localhost:8000/health`

---

## Complete Test Sequence Example

1. **First Request** (get conversation_id):
   ```json
   {
     "text": "hello",
     "user_id": "sumer.choudhary@bitcot.com",
     "title": "Test",
     "account_id": "A-011977763"
   }
   ```
   Copy `conversation_id` from response.

2. **Test Account Overview** (use conversation_id from step 1)

3. **Test Save Note** (use same conversation_id)

4. **Test Fetch Notes** (use same conversation_id)

5. **Test Facility Overview** (use same conversation_id)

---

## Notes About Mock Data

- All notes are **account-scoped** (saved under `account_id`, not `user_id`)
- Mock store has pre-seeded notes for account `A-011977763`
- When you save notes, they're stored in-memory (reset when server restarts)
- Account and facility data is static from `mock_store.py`

