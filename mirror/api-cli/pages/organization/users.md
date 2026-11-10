---
title: Users
url: https://platform.claude.com/docs/en/api/cli/organization/users
---

# Users

## List Users

`$ ant organization:users list`

**GET** `/v1/organizations/users`

List the organization's members.

### Parameters

- `--after-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `--before-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `--email: optional string` (query parameter)

  Filter by user email.

  format: email

- `--limit: optional number` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  minimum: 1, maximum: 1000

- `--role: optional array of string` (query parameter)

  Filter to items whose `role` equals one of the supplied values. Repeatable; values are OR'ed together.

  Accepted values depend on the organization type: Console and API organizations accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude Enterprise organizations accept `user`, `owner`, `primary_owner`, `membership_admin`, and `managed`.

### Returns

- `ListResponse_User_: object`

  - `data: array of OrganizationUser`

    - `type: "user"`

      Object type.

      For Users, this is always `"user"`.

    - `id: string`

      ID of the User.

    - `added_at: string`

      RFC 3339 datetime string indicating when the User joined the Organization.

      format: date-time

    - `email: string`

      Email of the User.

    - `name: string`

      Name of the User.

    - `role: "admin" or "billing" or "claude_code_user" or 6 more`

      Organization role of the User.

      - `"admin"`

      - `"billing"`

      - `"claude_code_user"`

      - `"developer"`

      - `"managed"`

      - `"membership_admin"`

      - `"owner"`

      - `"primary_owner"`

      - `"user"`

  - `first_id: string`

    First ID in the `data` list. Can be used as the `before_id` for the previous page.

  - `has_more: boolean`

    Indicates if there are more results in the requested page direction.

  - `last_id: string`

    Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```bash
ant organization:users list
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
      "added_at": "2024-10-30T23:58:27.427722Z",
      "email": "user@emaildomain.com",
      "name": "Jane Doe",
      "role": "admin",
      "type": "user"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

## Get User

`$ ant organization:users retrieve`

**GET** `/v1/organizations/users/{user_id}`

Retrieve a member of the organization by user ID.

### Parameters

- `--user-id: string` (path parameter)

  ID of the User.

### Returns

- `organization_user: object`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "admin" or "billing" or "claude_code_user" or 6 more`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

### Example

```bash
ant organization:users retrieve \
  --user-id user_id
```

#### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "added_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "name": "Jane Doe",
  "role": "admin",
  "type": "user"
}
```

## Update User

`$ ant organization:users update`

**POST** `/v1/organizations/users/{user_id}`

Update a member's organization role.

### Parameters

- `--user-id: string` (path parameter)

  ID of the User.

- `--role: "billing" or "claude_code_user" or "developer" or 2 more`

  New role for the User.

  The accepted values depend on the organization type. Console and API organizations accept `user`, `developer`, `billing`, and `claude_code_user`; `admin` cannot be assigned through the API. Claude Enterprise organizations accept `user` and `managed`; changing a User's role to `managed` requires the `write:rbac_groups` scope in addition to `write:members`.

  - `"billing"`

  - `"claude_code_user"`

  - `"developer"`

  - `"managed"`

  - `"user"`

### Returns

- `organization_user: object`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "admin" or "billing" or "claude_code_user" or 6 more`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

### Example

```bash
ant organization:users update \
  --user-id user_id \
  --role user
```

#### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "added_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "name": "Jane Doe",
  "role": "admin",
  "type": "user"
}
```

## Remove User

`$ ant organization:users remove`

**DELETE** `/v1/organizations/users/{user_id}`

Remove a member from the organization.

### Parameters

- `--user-id: string` (path parameter)

  ID of the User.

### Returns

- `OrganizationUserRemoveResponse: object`

  - `type: "user_deleted"`

    Deleted object type.

    For Users, this is always `"user_deleted"`.

  - `id: string`

    ID of the User.

### Example

```bash
ant organization:users remove \
  --user-id user_id
```

#### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "type": "user_deleted"
}
```

## Domain types

### Cannot Remove Last Member Error Details

- `cannot_remove_last_member_error_details: object`

  The user is the organization's only member. Add another member before removing this one.

  - `error_code: "cannot_remove_last_member"`

### Organization User

- `organization_user: object`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "admin" or "billing" or "claude_code_user" or 6 more`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`
