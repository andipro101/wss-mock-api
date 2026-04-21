# WSS Mock API

A mock implementation of the Security Center REST API built with FastAPI and PostgreSQL. Used for local testing of TDI assembly lines before connecting to the real WSS system.

## Stack

- **FastAPI** — REST API framework
- **SQLAlchemy** — ORM
- **PostgreSQL** — database (via Docker)
- **Docker Compose** — container orchestration

## Running

```bash
docker compose up --build
```

API available at: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

## Seed Test Data

On first run the database is empty. Populate it using the Swagger UI:

```
POST http://localhost:8000/test/reset
```

Or via the Swagger UI at `http://localhost:8000/docs` — find `/test/reset` and click **Try it out**.

This creates 3 test users: `user1` (Pierre), `svsupport9` (Galin), `draft-user`.  
Calling it again wipes and re-seeds from scratch.

## API Documentation

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI — interactive, execute requests directly |
| `http://localhost:8000/redoc` | ReDoc — clean read-only reference |

---

# Security Center REST API Reference

Security Center provides REST APIs to get or modify entities.

All REST APIs use JSON as input and produce JSON as output.

Any modification of an entity that is not in SDM FINAL state fails with an explicit error message asking to first make the entity FINAL manually before doing a new call to the REST API.

## URLs of REST APIs

All Security Center REST APIs are under the following common sub path:

```text
https://{hostname}:{port}/securitycenter/restapi/
```

Where `{hostname}` is the server name.

Example full path to the user REST API:

```text
https://computer1.ion.com:20104/securitycenter/restapi/user/
```

REST API documentation is available on each Suite installation under:

```text
https://{hostname}:{port}/securitycenter/restapidoc.html
```

## User REST APIs

### Get all users

- URL: `/restapi/user/`
- HTTP method: `GET`
- Request parameters: none

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `Array[UserPojo]` |
| 400 | An error occurred during the get all users request | `SingleResponsePojo` |

### Create multiple users

- URL: `/restapi/user/`
- HTTP method: `POST`

Request parameters:

| Name | Located in | Required | Description | Schema |
|---|---|---|---|---|
| Body | Body | Yes | The list of users to create in JSON format | `Array[UserPojo]` |

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `Array[SingleResponsePojo]` |
| 400 | An error occurred during the create users request | `Array[SingleResponsePojo]` |

### Update multiple users

- URL: `/restapi/user/`
- HTTP method: `PATCH`

Request parameters:

| Name | Located in | Required | Description | Schema |
|---|---|---|---|---|
| Body | Body | Yes | The list of users to update in JSON format | `Array[UserPojo]` |

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `Array[SingleResponsePojo]` |
| 400 | An error occurred during the update users request | `Array[SingleResponsePojo]` |

### Get a single user

- URL: `/restapi/user/{userid}`
- HTTP method: `GET`

Request parameters:

| Name | Located in | Required | Description | Schema |
|---|---|---|---|---|
| userid | path | Yes | The ID of the user to retrieve | `String` |

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `UserPojo` |
| 400 | An error occurred during the get user request | `SingleResponsePojo` |

### Revoke a single user

Keeps the user in the system but locked.

- URL: `/restapi/user/{userid}`
- HTTP method: `DELETE`

Request parameters:

| Name | Located in | Required | Description | Schema |
|---|---|---|---|---|
| userid | path | Yes | The ID of the user to revoke | `String` |

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `SingleResponsePojo` |
| 400 | An error occurred during the revoke user request | `SingleResponsePojo` |

### Purge a single user

Removes the user from the system.

- URL: `/restapi/user/purge/{userid}`
- HTTP method: `DELETE`

Request parameters:

| Name | Located in | Required | Description | Schema |
|---|---|---|---|---|
| userid | path | Yes | The ID of the user to purge | `String` |

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `SingleResponsePojo` |
| 400 | An error occurred during the purge user request | `SingleResponsePojo` |

## User Role Assignment REST APIs

### Get all user role assignments of all users

- URL: `/restapi/userroleassignment/`
- HTTP method: `GET`
- Request parameters: none

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `Array[UserRoleAssignmentPojo]` |
| 400 | An error occurred during the get all user role assignments request | `SingleResponsePojo` |

### Override multiple user role assignments

- URL: `/restapi/userroleassignment/`
- HTTP method: `POST`

Request parameters:

| Name | Located in | Required | Description | Schema |
|---|---|---|---|---|
| Body | Body | Yes | The list of user role assignments to override in JSON format | `Array[UserRoleAssignmentPojo]` |

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `Array[SingleResponsePojo]` |
| 400 | An error occurred during the override user role assignments request | `Array[SingleResponsePojo]` |

### Get all user role assignments of a single user

- URL: `/restapi/userroleassignment/{userid}`
- HTTP method: `GET`

Request parameters:

| Name | Located in | Required | Description | Schema |
|---|---|---|---|---|
| userid | path | Yes | The ID of the user to use for role assignments retrieving | `String` |

Response:

| Status Code | Reason | Response Model |
|---|---|---|
| 200 | Successful operation | `Array[UserRoleAssignmentPojo]` |
| 400 | An error occurred during the get role assignments of a single user request | `SingleResponsePojo` |

## Pojo Definitions

### SingleResponsePojo

| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| entityType | String | required | The entity type | `User` |
| entityId | String | required | The entity ID | `user1` |
| result | String | required | The request's result | `Success` |
| errorMessage | String | optional | An error message | `A user with this ID already exists` |

```json
{
  "entityType": "User",
  "entityId": "user1",
  "result": "Success",
  "errorMessage": null
}
```

### UserPojo

| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| id | String | required | The user ID | `user1` |
| name | String | required | The user name | `Pierre` |
| email | String | required | The user email | `pierre@email.com` |
| adminCenter | String | required | The admin center the user belongs to | `ROOT-ADMIN-CENTER` |
| timeZone | String | optional | The appropriate time zone for the user | `GMT` |
| menuName | String | optional | The name of the Application Manager menu definition file | `SYSTEM-MENU` |
| comment | String | optional | Comments | `Any comment` |
| administrator | Boolean | optional | Grants administrative rights | `false` |
| webUser | Boolean | optional | Defines the user as a web user | `false` |
| keepTxTrader | Boolean | optional | Can create transactions on behalf of another user | `false` |
| lockedLogin | Boolean | optional | Disables access to the system | `false` |
| platformUsers | Boolean | optional | ION platform entitlement | `false` |
| platformServices | Boolean | optional | ION platform entitlement | `false` |
| platformSystem | Boolean | optional | ION platform entitlement | `false` |
| platformProcesses | Boolean | optional | ION platform entitlement | `false` |
| platformComponents | Boolean | optional | ION platform entitlement | `false` |
| platformEntitlements | Boolean | optional | ION platform entitlement | `false` |
| platformProfile | String | optional | ION platform user profile | `Publisher`, `Viewer` or `Administrator` |
| version | Integer | optional | The user profile version | `0` |
| databaseLogin | Boolean | optional | Not required as input | `false` |
| databaseLoginOriginal | Boolean | optional | Not required as input | `false` |
| lockedDBLogin | Boolean | optional | Not required as input | `false` |
| transitive | Boolean | optional | Not required as input | `false` |

```json
{
  "adminCenter": "ROOT-ADMIN-CENTER",
  "timeZone": "UTC",
  "menuName": "SYSTEM-MENU",
  "comment": "test comment",
  "administrator": true,
  "webUser": true,
  "keepTxTrader": false,
  "lockedLogin": false,
  "platformUsers": true,
  "platformServices": false,
  "platformSystem": false,
  "platformProcesses": false,
  "platformComponents": false,
  "platformEntitlements": false,
  "platformProfile": "Administrator",
  "version": 0,
  "databaseLogin": false,
  "databaseLoginOriginal": false,
  "lockedDBLogin": false,
  "transitive": false,
  "id": "user1",
  "name": "Pierre",
  "email": "pierre@email.com"
}
```

### UserRoleAssignmentPojo

| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| userId | string | required | The user ID | `user1` |
| roleIDs | array[string] | required | The list of role IDs assigned to the user | `ACCOUNTANT, ADMINISTRATOR` |
| missingRoleAction | string | optional | Action if a role ID is unknown | `Create`, `Fail`, or `Ignore` |

```json
{
  "userId": "user1",
  "missingRoleAction": "Ignore",
  "roleIDs": [
    "ACCOUNTANT",
    "BACK-OFFICE"
  ]
}
```
