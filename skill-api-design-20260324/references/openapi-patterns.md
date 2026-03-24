# OpenAPI 3.x Pattern Library

## Complete Resource CRUD Pattern

```yaml
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/PageLimit'
        - $ref: '#/components/parameters/PageCursor'
        - name: sort
          in: query
          schema:
            type: string
            default: -created_at
          description: "Sort by field. Prefix - for descending. e.g. -created_at,name"
        - name: filter[status]
          in: query
          schema:
            type: string
            enum: [active, inactive, suspended]
        - name: filter[role]
          in: query
          schema:
            type: string
            enum: [admin, user, guest]
      responses:
        '200':
          description: Paginated list of users
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
              description: Requests allowed per window
            X-RateLimit-Remaining:
              schema: { type: integer }
              description: Requests remaining in current window
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '429':
          $ref: '#/components/responses/TooManyRequests'
        '500':
          $ref: '#/components/responses/InternalError'
    post:
      summary: Create user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
            example:
              email: "user@example.com"
              name: "Jane Doe"
              role: "user"
      responses:
        '201':
          description: User created
          headers:
            Location:
              schema: { type: string, format: uri }
              description: URL of the created resource
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'
        '422':
          $ref: '#/components/responses/Unprocessable'
        '500':
          $ref: '#/components/responses/InternalError'

  /users/{userId}:
    get:
      summary: Get user
      operationId: getUser
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
    patch:
      summary: Update user
      operationId: updateUser
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/UserId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
      responses:
        '200':
          description: Updated user
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'
        '422':
          $ref: '#/components/responses/Unprocessable'
    delete:
      summary: Delete user
      operationId: deleteUser
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'

  /users/{userId}/orders:
    get:
      summary: List user's orders
      operationId: listUserOrders
      tags: [Users, Orders]
      parameters:
        - $ref: '#/components/parameters/UserId'
        - $ref: '#/components/parameters/PageLimit'
        - $ref: '#/components/parameters/PageCursor'
      responses:
        '200':
          description: Paginated list of orders
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderList'
        '404':
          $ref: '#/components/responses/NotFound'
```

## Reusable Components

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

  parameters:
    UserId:
      name: userId
      in: path
      required: true
      schema:
        type: string
        format: uuid
      description: Unique user identifier (UUID)
    PageLimit:
      name: limit
      in: query
      schema:
        type: integer
        default: 20
        minimum: 1
        maximum: 100
      description: Number of items per page
    PageCursor:
      name: cursor
      in: query
      schema:
        type: string
      description: Pagination cursor from previous response

  schemas:
    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              example: VALIDATION_ERROR
            message:
              type: string
              example: "Request validation failed"
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                    example: email
                  message:
                    type: string
                    example: "Must be a valid email address"
                  value:
                    type: string
                    example: "not-an-email"
            requestId:
              type: string
              example: "req_abc123xyz"

    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
        email:
          type: string
          format: email
        name:
          type: string
        role:
          type: string
          enum: [admin, user, guest]
        status:
          type: string
          enum: [active, inactive, suspended]
        createdAt:
          type: string
          format: date-time
          example: "2026-03-24T12:00:00Z"
        updatedAt:
          type: string
          format: date-time
        deletedAt:
          type: string
          format: date-time
          nullable: true

    UserCreate:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 255
        role:
          type: string
          enum: [admin, user, guest]
          default: user
        password:
          type: string
          format: password
          minLength: 8
          writeOnly: true

    UserUpdate:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 255
        status:
          type: string
          enum: [active, inactive]

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        nextCursor:
          type: string
          nullable: true
          description: Cursor for next page. Null if no more pages.
        hasMore:
          type: boolean
        total:
          type: integer
          nullable: true
          description: "Total count. Null for cursor pagination."

    Order:
      type: object
      properties:
        id:
          type: string
          format: uuid
        userId:
          type: string
          format: uuid
        status:
          type: string
          enum: [pending, paid, shipped, delivered, cancelled, refunded]
        totalAmount:
          type: number
          format: decimal
          example: 99.99
        currency:
          type: string
          example: USD
        createdAt:
          type: string
          format: date-time

    OrderList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Order'
        pagination:
          $ref: '#/components/schemas/Pagination'

  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: BAD_REQUEST
              message: "Invalid request parameters"
              details:
                - field: limit
                  message: "Must be between 1 and 100"
                  value: 999
              requestId: "req_abc123"

    Unauthorized:
      description: Authentication required
      headers:
        WWW-Authenticate:
          schema:
            type: string
          description: "Challenge string, e.g. Bearer realm='api'"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: UNAUTHORIZED
              message: "Authentication required"
              requestId: "req_abc123"

    Forbidden:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: NOT_FOUND
              message: "User not found"
              requestId: "req_abc123"

    Conflict:
      description: Resource already exists or state conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unprocessable:
      description: Semantically invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    TooManyRequests:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema: { type: integer }
        X-RateLimit-Remaining:
          schema: { type: integer }
        X-RateLimit-Reset:
          schema:
            type: integer
            description: Unix timestamp when the rate limit resets
        Retry-After:
          schema:
            type: integer
            description: Seconds to wait before retrying
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: RATE_LIMIT_EXCEEDED
              message: "Too many requests. Please retry after 60 seconds."
              requestId: "req_abc123"

    InternalError:
      description: Unexpected server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: INTERNAL_ERROR
              message: "An unexpected error occurred"
              requestId: "req_abc123"
```

## Authentication Patterns

### Bearer JWT
```yaml
security:
  - BearerAuth: []
```

### API Key
```yaml
security:
  - ApiKeyAuth: []
```

### Optional Auth
```yaml
security:
  - BearerAuth: []
  - []
```
(The empty array `[]` means optional — endpoint works with or without auth)

### Multiple Auth Schemes
```yaml
security:
  - BearerAuth: []
  - ApiKeyAuth: []
```

## Deprecation Header

When deprecating an endpoint, include in response:
```yaml
Deprecation: true
Sunset: Sat, 31 Dec 2027 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

## Rate Limiting Response Headers

Always include on every response:
- `X-RateLimit-Limit: 1000` — requests per window
- `X-RateLimit-Remaining: 999` — remaining in current window
- `X-RateLimit-Reset: 1742894400` — Unix timestamp when window resets

For 429 responses, also include:
- `Retry-After: 60` — seconds to wait
