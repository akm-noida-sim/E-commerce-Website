# API reference

Base URL: `http://localhost:5000/api`. Send JSON and a bearer token for protected endpoints.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register`, `/auth/login` | Create account / receive JWT |
| GET | `/auth/me` | Current account |
| GET | `/products`, `/products/:id`, `/categories` | Catalog. Supports `q`, `category`, `sort` |
| POST/PUT/DELETE | `/products[/:id]` | Admin product management |
| GET | `/cart` | Current customer cart |
| POST | `/cart/items` | Add `{productId, quantity}` |
| PATCH | `/cart/items/:productId` | Set `{quantity}`; zero removes |
| POST | `/orders` | Checkout with `shippingAddress` and `paymentMethod` |
| GET | `/orders`, `/orders/:id` | Own order history/tracking |
| GET/PATCH | `/admin/orders[/:id]` | Admin all orders/status update |
| GET | `/dashboard/customer`, `/dashboard/admin` | Role-specific metrics |

Admin endpoints require a JWT whose role claim is `admin`. Promote a trusted account directly in MongoDB during initial setup; never provide a public role-selection field.
