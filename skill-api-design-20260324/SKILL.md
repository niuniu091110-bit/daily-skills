---
name: api-design
description: "Design, document, and review REST APIs. Use when creating new APIs, improving existing API design, writing OpenAPI specs, designing API endpoints, reviewing API contracts, or resolving API design disputes. Triggers on: design an API, REST endpoint, API spec, OpenAPI, Swagger, API review, endpoint naming, pagination, versioning, error handling."
---

# API Design

Design clean, consistent, and developer-friendly REST APIs.

## Core Principles

1. **Resources over actions** — URLs represent nouns (things), not verbs (operations)
2. **Consistency** — Same patterns everywhere; predictable structure
3. **Stateless** — Each request carries all info; no server-side session
4. **Layered** — Client can't assume reach beyond one hop
5. **Backward compatible** — Additive changes only; breaking changes require versioning

## URL Design

### Structure

```
https://api.example.com/v1/{resource}/{id}/{sub-resource}
```

Rules:
- Lowercase, hyphen-separated: `/user-profiles`, not `/userProfiles`
- Plural nouns for collections: `/users`, not `/user`
- No verbs in path: `/orders/{id}/cancel` → use `POST /orders/{id}` with `status: "cancelled"`
- IDs in path for specifics: `/users/{userId}/orders`
- Keep ≤3 path segments deep

### Good vs Bad Examples

| Good | Bad |
|------|-----|
| `GET /users` | `GET /getUsers` |
| `POST /users` | `POST /createUser` |
| `GET /users/{id}` | `GET /user?id=123` |
| `DELETE /users/{id}` | `GET /users/delete?id=123` |
| `POST /orders/{id}/refund` | `POST /refundOrder?orderId=...` |

## HTTP Methods

| Method | Purpose | Idempotent | Body |
|--------|---------|-----------|------|
| GET | Retrieve resource(s) | Yes | No |
| POST | Create new resource | No | Yes |
| PUT | Replace entire resource | Yes | Yes |
| PATCH | Partial update | No | Yes |
| DELETE | Remove resource | Yes | Rarely |

**Rules:**
- `GET` — never mutate data; never have side effects
- `POST` — create; idempotency via client-generated `idempotency-key` header
- `PUT` — full replace; send all fields including optional ones
- `PATCH` — partial update; send only changed fields
- `DELETE` — return 204 on success, 404 if already gone (idempotent)

## Status Codes

| Code | Meaning | When to Use |
|------|---------|------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST creating resource |
| 204 | No Content | Successful DELETE, action with no body |
| 400 | Bad Request | Invalid input, validation failure |
| 401 | Unauthorized | Missing or invalid auth |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, state conflict |
| 422 | Unprocessable | Semantically invalid (e.g., invalid email format) |
| 429 | Too Many Requests | Rate limit hit |
| 500 | Server Error | Unexpected failure |
| 503 | Service Unavailable | Planned downtime, overload |

## Error Response Format

Always return a consistent error body:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address",
        "value": "not-an-email"
      }
    ],
    "requestId": "req_abc123"
  }
}
```

Rules:
- Use `code` (machine-readable string) not just HTTP status
- `message` is safe to show to end users
- `details` array for field-level validation errors
- Always include `requestId` for tracing

## Pagination

Use cursor-based pagination for large datasets (preferred):

```
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true,
    "total": null
  }
}
```

For offset pagination (simple cases, ≤10k items):
```
GET /users?offset=40&limit=20
```

**Rules:**
- Default `limit` ≤ 100; max 1000
- Always return `hasMore` or `nextCursor`
- Never return `total` for cursor pagination (expensive)

## Sorting & Filtering

```
GET /users?sort=-created_at,name&filter[status]=active&filter[role]=admin
```

Rules:
- Prefix `-` for descending: `-created_at`
- Multiple sort fields comma-separated
- `filter[field]` for exact match
- `filter[field][gte]` for range queries
- OpenAPI `style: form` and `explode: true` for array filters

## Authentication

| Method | Use Case |
|--------|----------|
| Bearer JWT | User sessions, short-lived |
| API Key | Server-to-server, long-lived |
| OAuth 2.0 | Third-party access |

For API keys:
- Pass in `X-API-Key` header (not URL query param)
- Never log or return the key
- Scoped permissions: read-only, read-write, admin

## Versioning

Use URL path versioning (most common):

```
/v1/users    ← stable
/v2/users    ← breaking changes
```

Rules:
- Version at resource level: `/v1/orders`, `/v2/orders` can coexist
- Increment version for **breaking** changes only
- Breaking = removing fields, changing types, changing semantics
- Non-breaking = adding fields, adding endpoints, adding optional params
- Maintain old versions for ≥12 months after deprecation notice
- Return `Deprecation` header with sunset date for deprecated endpoints

## Request & Response Conventions

### Request
- Accept `Content-Type: application/json`
- Support `Accept-Language: en` for error messages
- Idempotency key for POST: `Idempotency-Key: <uuid>`

### Response
- Always `Content-Type: application/json`
- Return full resource on 200/201 (not wrapped)
- Use `data` envelope only when wrapping collections:
  ```json
  { "data": [...], "meta": {...} }
  ```
- ISO 8601 for all dates: `"2026-03-24T12:00:00Z"`
- ISO 4217 for currency: `"USD"`, `"HKD"`
- UUIDs for all IDs: `"550e8400-e29b-41d4-a716-446655440000"`

## OpenAPI Spec Basics

When writing or reviewing OpenAPI specs:

```yaml
openapi: 3.1.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
        - name: cursor
          in: query
          schema: { type: string }
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
components:
  schemas:
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'
```

**Rules:**
- Always specify `description` on operations
- Use `$ref` to avoid duplication
- Specify all error responses (400, 401, 403, 404, 500)
- Use semantic `summary` (imperative: "List users", not "Lists users")

## Design Review Checklist

- [ ] Resources named with plural nouns; no verbs in paths
- [ ] Correct HTTP methods used for each operation
- [ ] Proper status codes returned (not just 200 for everything)
- [ ] Error responses include machine-readable `code` + human `message`
- [ ] Pagination uses cursor-based for large datasets
- [ ] Authentication uses appropriate method (Bearer/API Key/OAuth)
- [ ] Versioning strategy defined before breaking changes happen
- [ ] All dates in ISO 8601 format
- [ ] OpenAPI spec includes all error responses
- [ ] No sensitive data logged or returned in responses
- [ ] IDs are UUIDs, not sequential integers (avoid enumeration)
- [ ] Rate limiting headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## OpenAPI Reference

See `references/openapi-patterns.md` for complete OpenAPI YAML patterns including request bodies, responses, authentication, and pagination.

## Tools

- [Swagger Editor](https://editor.swagger.io/) — Interactive OpenAPI editor
- [Stoplight](https://stoplight.io/) — API design platform
- [Redoc](https://redocly.com/) — OpenAPI documentation renderer
- [JSONLint](https://jsonlint.com/) — Validate JSON
- HTTP clients: `curl`, [Insomnia](https://insomnia.rest/), [Postman](https://www.postman.com/)
