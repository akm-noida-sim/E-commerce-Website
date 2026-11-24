# Architecture

ShopSphere uses a separated SPA/API architecture. React calls Flask REST endpoints over HTTPS, Flask validates and authorizes every request, and PyMongo persists documents to MongoDB.

```
React + Vite ── JWT bearer ──> Flask blueprints ──> PyMongo ──> MongoDB Atlas
     cart state       auth / products / cart / orders       users, products, carts, orders
```

Passwords are bcrypt hashes. JWTs contain only identity and role claims. Checkout recalculates totals from stored product prices and decrements stock atomically with a stock predicate. Order reads are constrained by `userId`; admin routes independently verify the JWT role.
