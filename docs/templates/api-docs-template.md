# Smart Home System API Documentation

## Overview

The Smart Home System API provides a comprehensive interface for managing and controlling smart home devices, including lights, thermostats, security systems, and more. This RESTful API allows developers to integrate with the smart home ecosystem and build applications that can monitor and control home automation devices.

**Base URL**: `https://api.smart-home-system.com/v1`
**Content Type**: `application/json`

## Authentication

All API requests require authentication using Bearer tokens. Include the token in the Authorization header of your requests.

### Authentication Header
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Obtaining an Access Token

1. **User Login**
   ```http
   POST /auth/login
   Content-Type: application/json
   
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. **API Key Authentication**
   ```http
   POST /auth/api-key
   Content-Type: application/json
   
   {
     "api_key": "your_api_key"
   }
   ```

## Endpoints

### Devices

#### Get All Devices
```http
GET /devices
```

**Response**
```json
{
  "devices": [
    {
      "id": "device_123",
      "name": "Living Room Light",
      "type": "light",
      "status": "online",
      "room": "living_room",
      "manufacturer": "Philips Hue",
      "capabilities": ["on_off", "brightness", "color"]
    }
  ],
  "total_count": 15,
  "page": 1,
  "per_page": 20
}
```

#### Get Device by ID
```http
GET /devices/{device_id}
```

**Parameters**
- `device_id` (string, required): The unique identifier of the device

#### Control Device
```http
POST /devices/{device_id}/control
Content-Type: application/json

{
  "action": "turn_on",
  "parameters": {
    "brightness": 75,
    "color": "#FF5733"
  }
}
```

### Rooms

#### Get All Rooms
```http
GET /rooms
```

#### Get Room Devices
```http
GET /rooms/{room_id}/devices
```

### Scenes

#### Get All Scenes
```http
GET /scenes
```

#### Activate Scene
```http
POST /scenes/{scene_id}/activate
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
  "description": "Turn on lights and adjust thermostat in the morning",
  "cron_expression": "0 7 * * *",
  "actions": [
    {
      "device_id": "light_123",
      "action": "turn_on",
      "parameters": {
        "brightness": 50
      }
    }
  ],
  "enabled": true
}
```

## Request/Response Examples

### Example: Turning on a light

**Request**
```http
POST /devices/light_123/control
Authorization: Bearer abc123def456
Content-Type: application/json

{
  "action": "turn_on",
  "parameters": {
    "brightness": 80,
    "color": "warm_white"
  }
}
```

**Response**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "message": "Device light_123 turned on successfully",
  "device": {
    "id": "light_123",
    "name": "Living Room Light",
    "status": "on",
    "brightness": 80,
    "color": "warm_white"
  }
}
```

### Example: Getting device list

**Request**
```http
GET /devices?room=living_room&type=light
Authorization: Bearer abc123def456
```

**Response**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "devices": [
    {
      "id": "light_123",
      "name": "Main Light",
      "type": "light",
      "status": "online",
      "room": "living_room",
      "capabilities": ["on_off", "brightness", "color"]
    },
    {
      "id": "light_456",
      "name": "Lamp",
      "type": "light",
      "status": "offline",
      "room": "living_room",
      "capabilities": ["on_off", "brightness"]
    }
  ],
  "total_count": 2,
  "page": 1,
  "per_page": 20
}
```

## Error Codes

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Error Response Format

```json
{
  "error": {
    "code": "device_not_found",
    "message": "The requested device was not found",
    "details": "Device with ID 'invalid_id' does not exist",
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_abc123def456"
  }
}
```

### Common Error Codes

- `invalid_token` - Authentication token is invalid or expired
- `device_offline` - Requested device is currently offline
- `invalid_parameters` - Request parameters are invalid
- `rate_limit_exceeded` - Too many requests in a short period
- `device_busy` - Device is currently processing another command
- `unsupported_operation` - Requested operation is not supported by the device

## Rate Limiting

The API enforces rate limits to ensure fair usage:
- **Standard users**: 100 requests per minute
- **Premium users**: 1000 requests per minute
- **Enterprise users**: Custom limits

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642253400
```

## Pagination

List endpoints support pagination using `page` and `per_page` parameters:

```http
GET /devices?page=2&per_page=10
```

Response includes pagination metadata:
```json
{
  "devices": [...],
  "total_count": 150,
  "page": 2,
  "per_page": 10,
  "total_pages": 15
}
```

## Webhooks

The API supports webhooks for real-time device status updates:

### Webhook Events
- `device.status_changed` - Device status changed
- `device.value_changed` - Device value updated
- `scene.activated` - Scene activated
- `schedule.triggered` - Schedule executed

### Webhook Payload Example
```json
{
  "event": "device.status_changed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "device_id": "light_123",
    "old_status": "off",
    "new_status": "on",
    "brightness": 75
  }
}
```