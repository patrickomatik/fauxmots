# API Documentation

Fauxmots provides a simple REST API for interacting with the captured emails programmatically.

## Base URL

All API endpoints are relative to your Fauxmots server, for example:
```
http://localhost:5000/api/
```

## Endpoints

### List Emails

Retrieves a list of all captured emails.

**URL**: `/api/emails`

**Method**: `GET`

**Response**:
```json
{
  "emails": [
    {
      "id": 1,
      "sender": "sender@example.com",
      "recipients": ["recipient@example.com"],
      "subject": "Test Email",
      "date": "2023-01-01 12:34:56",
      "filename": "20230101123456_abcd1234.eml",
      "size": 1024,
      "has_attachments": false
    },
    ...
  ]
}
```

### Get Server Configuration

Retrieves the current SMTP server configuration.

**URL**: `/api/config`

**Method**: `GET`

**Response**:
```json
{
  "smtp_host": "127.0.0.1",
  "smtp_port": 1025
}
```

## Example Usage

### Using cURL

List all emails:
```bash
curl http://localhost:5000/api/emails
```

Get server configuration:
```bash
curl http://localhost:5000/api/config
```

### Using Python with Requests

```python
import requests

# List all emails
response = requests.get('http://localhost:5000/api/emails')
emails = response.json()['emails']
print(f"Found {len(emails)} emails")

# Get server configuration
config = requests.get('http://localhost:5000/api/config').json()
print(f"SMTP server running at {config['smtp_host']}:{config['smtp_port']}")
```

### Using JavaScript with Fetch

```javascript
// List all emails
fetch('http://localhost:5000/api/emails')
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.emails.length} emails`);
    data.emails.forEach(email => {
      console.log(`${email.subject} from ${email.sender}`);
    });
  });

// Get server configuration
fetch('http://localhost:5000/api/config')
  .then(response => response.json())
  .then(config => {
    console.log(`SMTP server running at ${config.smtp_host}:${config.smtp_port}`);
  });
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: The request was successful
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An unexpected error occurred

Error responses include a JSON object with an error message:

```json
{
  "error": "Resource not found"
}
```

## Rate Limits

There are currently no rate limits implemented in the API.

## Future Enhancements

The following API endpoints are planned for future releases:

1. `GET /api/emails/{id}`: Get details for a specific email
2. `DELETE /api/emails/{id}`: Delete a specific email
3. `DELETE /api/emails`: Delete all emails
4. `GET /api/stats`: Get server statistics (email count, storage usage, etc.)
