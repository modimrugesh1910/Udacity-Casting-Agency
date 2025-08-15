## 🔗 Live API URL

The Casting Agency API is deployed and accessible at:

https://udacity-casting-agency-lj4k.onrender.com/

All endpoints are secured via Auth0 RBAC and require a valid JWT.

---

## 🔐 Authentication Setup

1. Log in to the Auth0 account at: [https://your-tenant.auth0.com](https://your-tenant.auth0.com)
2. Obtain a JWT token by logging in as a user with the desired role.
3. Use the token to authorize requests:

### Roles and Permissions

| Role | Permissions |
|------|-------------|
| **Casting Assistant** | `get:actors`, `get:movies` |
| **Casting Director** | All above + `post:actors`, `patch:actors`, `delete:actors`, `patch:movies` |
| **Executive Producer** | All above + `post:movies`, `delete:movies` |

---

### 🔑 Example JWT Usage

Make requests with the `Authorization` header like this:

```bash
curl https://casting-agency-api.onrender.com/actors \
  -H "Authorization: Bearer <your_access_token>"
