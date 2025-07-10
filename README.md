# Employee Search API with FastAPI

A high-performance employee search microservice with Redis caching, rate limiting, and dynamic filtering capabilities.

## Features

- 🔍 Dynamic employee search with flexible filters
- 🚦 Rate limiting (10 requests/minute)
- 💾 Redis caching for faster responses
- 📊 Pagination support
- 🐳 Docker containerization
- ✅ Unit tests included

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ahmad110abbas/employee-search-api.git
cd employee-search-api
```

### 2. Start the services
```bash
docker-compose up --build
```

### 3. Verify services are running
- API: http://localhost:8000
- Redis Insight (if needed): http://localhost:8001

## API Documentation

### POST /search/employees

Search employees with dynamic filters

**Parameters:**
- `page`: Page number (default: 1)
- `size`: Results per page (default: 10)

**Request Body:**
```json
{
  "filters": {
    "department": "Engineering",
    "status": ["active", "not_started"],
    "location": ["New York", "Chicago"],
    "full_name": "John"
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "contact_info": "john.doe@example.com",
      "department": "Engineering",
      "position": "Senior Developer",
      "location": "New York",
      "status": "active"
    }
  ],
  "pagination": {
    "total": 1,
    "page": 1,
    "size": 10,
    "total_pages": 1
  }
}
```

## Configuration

Edit `config.ini` to customize the service:

```ini
[APP]
DEBUG = False

[DATABASE]
URL = sqlite:///./employees.db

[REDIS]
HOST = redis
PORT = 6379
DB = 0
EXPIRE_SECONDS = 300  # 5 minutes

[RATE_LIMIT]
REQUESTS_PER_MINUTE = 100
WINDOW_SECONDS = 60

[EMPLOYEE]
STATUS_OPTIONS = active,not_started,terminated
```

## Running Tests

To run unit tests:

```bash
docker-compose run app pytest tests/
```

## API Usage Examples

### Search active employees in New York
```bash
curl -X POST http://localhost:8000/search/employees \
  -H "Content-Type: application/json" \
  -d '{"filters": {"status": "active", "location": "New York"}}'
```

### Search for developers
```bash
curl -X POST http://localhost:8000/search/employees?page=2&size=5 \
  -H "Content-Type: application/json" \
  -d '{"filters": {"position": "Developer"}}'
```

### Search by name
```bash
curl -X POST http://localhost:8000/search/employees \
  -H "Content-Type: application/json" \
  -d '{"filters": {"full_name": "Smith"}}'
```

## Development Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac)
venv\Scripts\activate    # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start Redis:
```bash
docker run -d -p 6379:6379 --name redis redis
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## Deployment

To deploy to production:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.