# ShopSphere

ShopSphere is a production-minded full-stack e-commerce application for browsing products, maintaining a server-backed cart, placing cash-on-delivery orders, tracking fulfillment, and running a role-protected store dashboard.

## Highlights

- JWT + bcrypt authentication with user/admin authorization boundaries
- Searchable, filterable product catalog and stock-aware cart
- Secure checkout: server-calculated totals and inventory decrement
- Customer order history; admin sales, customer, order, and inventory metrics
- Responsive React/Vite interface with Flask REST API and MongoDB persistence

## Stack

React, Vite, Tailwind CSS, Flask, PyMongo/MongoDB, Flask-JWT-Extended, and bcrypt.

## Run locally

Prerequisites: Node 20+, Python 3.10+, and MongoDB (local or Atlas).

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python backend/run.py
```

In another terminal:

```powershell
cd frontend
Copy-Item ..\.env.example .env
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:5000/api` in `frontend/.env`. To make an administrator, update only a trusted account in MongoDB: `db.users.updateOne({email: "you@example.com"}, {$set: {role: "admin"}})` and sign in again.

## API, design, tests, deployment

See [API documentation](docs/API.md), [architecture](docs/ARCHITECTURE.md), and [deployment guide](docs/DEPLOYMENT.md). Run API tests with `pytest backend/tests` from the repository root. The `screenshots/` folder is ready for verified product screenshots before publishing.

## Future enhancements

Razorpay order creation/webhook verification, product image storage, pagination, email receipts, coupon rules, refresh-token rotation, and a full admin product/order UI are natural next additions.
