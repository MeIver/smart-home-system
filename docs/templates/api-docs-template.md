# Smart Home System API Documentation

## Overview

The Smart Home System API provides a comprehensive interface for managing and controlling smart home devices, including lights, thermostats, security systems, and more. This RESTful API enables developers to integrate smart home functionality into their applications.

**Base URL**: `https://api.smart-home-system.com/v1`

## Authentication

All API requests require authentication using JSON Web Tokens (JWT). Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Obtaining a Token

```http
POST /auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

## Endpoints

### Devices

#### Get All Devices
```http
GET /devices
```

**Response:**
```json
{
  "devices": [
    {
      "id": "device_123",
      "name": "Living Room Light",
      "type": "light",
      "status": "on",
      "location": "living_room"
    }
  ]
}
```

#### Get Device by ID
```http
GET /devices/{device_id}
```

#### Control Device
```http
POST /devices/{device_id}/control
Content-Type: application/json

{
  "action": "turn_on",
  "parameters": {
    "brightness": 75
  }
}
```

### Rooms

#### Get All Rooms
```http
GET /rooms
```

#### Get Room by ID
```http
GET /rooms/{room_id}
```

#### Create Room
```http
POST /rooms
Content-Type: application/json

{
  "name": "Bedroom",
  "description": "Main bedroom"
}
```

### Scenes

#### Get All Scenes
```http
GET /scenes
```

#### Execute Scene
```http
POST /scenes/{scene_id}/execute
```

#### Create Scene
```http
POST /scenes
Content-Type: application/json

{
  "name": "Movie Night",
  "actions": [
    {
      "device_id": "light_1",
      "action": "turn_off"
    }
  ]
}
```

### Schedules

#### Get All Schedules
```http
GET /schedules
```

#### Create Schedule
```http
POST /schedules
Content-Type: application/json

{
  "name": "Morning Routine",
  "cron_expression": "0 7 * * *",
  "actions": [
    {
      "device_id": "thermostat_1",
      "action": "set_temperature",
      "parameters": {
        "temperature": 22
      }
    }
  ]
}
```

## Request/Response Examples

### Example 1: Turn on a light

**Request:**
```http
POST /devices/light_123/control
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "action": "turn_on",
  "parameters": {
    "brightness": 80
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Device light_123 turned on successfully",
  "device": {
    "id": "light_123",
    "name": "Living Room Light",
    "status": "on",
    "brightness": 80
  }
}
```

### Example 2: Get device status

**Request:**
```http
GET /devices/light_123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": "light_123",
  "name": "Living Room Light",
  "type": "light",
  "status": "on",
  "brightness": 80,
  "location": "living_room",
  "last_updated": "2024-01-15T10:30:00Z"
}
```

## Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | BAD_REQUEST | Invalid request parameters |
| 401 | UNAUTHORIZED | Authentication required or invalid token |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Resource conflict |
| 422 | UNPROCESSABLE_ENTITY | Validation failed |
| 429 | TOO_MANY_REQUESTS | Rate limit exceeded |
| 500 | INTERNAL_ERROR | Server error |
| 503 | SERVICE_UNAVAILABLE | Service temporarily unavailable |

### Error Response Format

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Device not found",
    "details": "The requested device with ID 'invalid_id' does not exist"
  }
}
```

## Rate Limits

- **Standard**: 1000 requests per hour
- **Burst**: 100 requests per minute
- **Authentication**: 10 login attempts per minute

## Pagination

For endpoints returning lists, use query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Example:**
```http
GET /devices?page=2&limit=50
```

## Webhooks

The API supports webhooks for real-time notifications. Register webhook endpoints to receive events:

- `DEVICE_STATE_CHANGED`
- `SCENE_EXECUTED`
- `SCHEDULE_TRIGGERED`
- `SECURITY_ALERT`

## Versioning

API version is specified in the URL path. Current version: `v1`

## Support

For API support and questions:
- Documentation: https://docs.smart-home-system.com
- Support Email: api-support@smart-home-system.com
- Community Forum: https://community.smart-home-system.com