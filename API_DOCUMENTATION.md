# **Local Events Management System API**

Welcome to the Local Events Management System API! This API allows for managing local events, including user authentication, event creation, registration, and searching/filtering of events.

## **Base/Local URL**

`http://127.0.0.1:8000`

## **Table of Contents**

- [Authentication](#authentication)
  - [Token Types](#token-types)
- [Users](#users)
  - [Create Admin](#create-admin)
  - [Initial Admin Create](#initial-admin-create)
  - [Admin Login](#admin-login)
  - [Admin Logout](#admin-logout)
  - [User Login](#user-login)
  - [User Logout](#user-logout)
  - [Register User](#register-user)
- [Token](#token)
  - [Refresh Token](#refresh-token)
- [Events](#events)
  - [Create Event](#create-event)
  - [Create Event Category](#create-event-category)
  <!-- - [Schema](#schema)
  - [Retrieve Schema](#retrieve-schema) -->

## **Authentication**

### Token Types

The Local Events Management System API uses different types of tokens for different user roles:

- **Admin Users**: Use JWT (JSON Web Tokens) provided by SimpleJWT for authentication.
- **Regular Users**: Use session tokens for authentication.

## **Users**

### Create Admin

**Endpoint**: `POST /api/users/admin/create/`

**Description**: Create an Admin Account.

**Request Parameters**:

- **email** (string, format: email, maxLength: 254) - Required
- **password** (string, maxLength: 128) - Required
- **first_name** (string, maxLength: 150) - Required
- **last_name** (string, maxLength: 150) - Required

**Sample Request**:

```json
{
  "email": "admin@example.com",
  "password": "password123",
  "first_name": "Admin",
  "last_name": "User"
}
```

### Initial Admin Create

**Endpoint**: `POST /api/users/admin/initial-create/`

**Description**: Create an initial Admin Account.

**Request Parameters**:

- **email** (string, format: email, maxLength: 254) - Required
- **password** (string, maxLength: 128) - Required
- **first_name** (string, maxLength: 150) - Required
- **last_name** (string, maxLength: 150) - Required

**Sample Request**:

```json
{
  "email": "admin@example.com",
  "password": "password123",
  "first_name": "Admin",
  "last_name": "User"
}
```

### Admin Login

**Endpoint**: `POST /api/users/admin/login/`

**Description**: Admin user login and return refresh and access token.

**Request Parameters**:

- **email** (string, format: email, maxLength: 254) - Required
- **password** (string, maxLength: 128) - Required

**Sample Request**:

```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

### Admin Logout

**Endpoint**: `POST /api/users/admin/logout/`

**Description**: Logout admin user.

**Request Parameters**:

- **message** (string) - Required

**Sample Request**:

```json
{
  "message": "Admin logout"
}
```

### Register User

**Endpoint**: `POST /api/users/users/register/`

**Description**: Register a new user.

**Request Parameters**:

- **email** (string, format: email, maxLength: 254) - Required
- **password** (string, maxLength: 128) - Required
- **first_name** (string, maxLength: 150) - Required
- **last_name** (string, maxLength: 150) - Required

**Sample Request**:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "User",
  "last_name": "Example"
}
```

### User Login

**Endpoint**: `POST /api/users/users/login/`

**Description**: Authenticate a user and return a CSRF token.

**Request Parameters**:

- **email** (string, format: email, maxLength: 254) - Required
- **password** (string, maxLength: 128) - Required

**Sample Request**:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### User Logout

**Endpoint**: `POST /api/users/users/logout/`

**Description**: Log out the authenticated user.

**Request Parameters**:

- **message** (string) - Required

**Sample Request**:

```json
{
  "message": "User logout"
}
```

## **Token**

### Refresh Token

**Endpoint**: `POST /api/token/refresh/`

**Description**: Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

**Request Parameters**:

- **refresh** (string) - Required

**Sample Request**:

```json
{
  "refresh": "your-refresh-token"
}
```

## **Events**

### Create Event

**Endpoint**: `POST /api/events/`

**Description**: Create a new event.

**Request Parameters**:

- **event_name** (string, maxLength: 100) - Required
- **event_hosts** (string, maxLength: 200) - Required
- **description** (string, maxLength: 200) - Required
- **image_url** (string, format: uri, maxLength: 200) - Required
- **event_date** (string, format: date-time) - Required
- **location** (string, maxLength: 100) - Required
- **registration_deadline** (string, format: date-time) - Required
- **capacity** (integer, min: -2147483648, max: 2147483647) - Required
- **status** (enum: UPCOMING, ONGOING, COMPLETED, CANCELED) - Required
- **category** (integer) - Required

**Sample Request**:

```json
{
  "event_name": "Sample Event",
  "event_hosts": "Host Name",
  "description": "Event Description",
  "image_url": "http://example.com/image.jpg",
  "event_date": "2024-08-01T10:00:00Z",
  "location": "Event Location",
  "registration_deadline": "2024-07-25T00:00:00Z",
  "capacity": 100,
  "status": "UPCOMING",
  "category": 1
}
```

### Create Event Category

**Endpoint**: `POST /api/events/category/`

**Description**: Create a new event category.

**Request Parameters**:

- **name** (string, maxLength: 100) - Required

**Sample Request**:

```json
{
  "name": "Music"
}
```

<!-- ## Schema

### Retrieve Schema

**Endpoint**: `GET /api/schema/`

**Description**: Retrieve the OpenAPI schema for the API. The format can be selected via content negotiation.

**Request Parameters**:

- **format** (string, enum: json, yaml) - Optional
- **lang** (string, enum: multiple languages) - Optional

**Sample Request**:

```
GET /api/schema/?format=json&lang=en
``` -->
