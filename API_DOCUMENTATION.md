# Aura Apparel - REST API Documentation

Aura Apparel exposes a standard RESTful JSON API running on Python Flask, designed according to OpenAPI 3.0 conventions with token-based JSON Web Token (JWT) authorization, role-based access control, and strict input validation.

- **Base URL:** `http://localhost:5000/api`
- **Authentication Header:** `Authorization: Bearer <access_token>`
- **Content Type:** `application/json`

---

## 1. Authentication Endpoints (`/api/auth`)

### `POST /api/auth/register`
Creates a new customer account and generates a welcome notification.
- **Request Body:**
  ```json
  {
    "full_name": "Victoria Sterling",
    "email": "victoria@example.com",
    "password": "SecurePassword123!",
    "phone": "+1 (555) 019-2831"
  }
  ```
- **Response `201 Created`:**
  ```json
  {
    "message": "Registration successful",
    "access_token": "eyJhbGciOi...",
    "user": {
      "id": 43,
      "email": "victoria@example.com",
      "full_name": "Victoria Sterling",
      "phone": "+1 (555) 019-2831",
      "role": "customer",
      "is_active": true
    }
  }
  ```

### `POST /api/auth/login`
Authenticates a user and returns a signed JWT access token.
- **Request Body:**
  ```json
  {
    "email": "customer@auraapparel.com",
    "password": "Customer@123456"
  }
  ```
- **Response `200 OK`:** Returns access token and user profile object.

### `GET /api/auth/profile`
*(Requires `Authorization: Bearer <token>`)*
Returns authenticated user details.

### `PUT /api/auth/profile`
*(Requires `Authorization: Bearer <token>`)*
Updates user's name or contact phone.

### `PUT /api/auth/change-password`
*(Requires `Authorization: Bearer <token>`)*
Verifies old password and hashes new password with bcrypt.

---

## 2. Product & Category Endpoints (`/api`)

### `GET /api/categories`
Returns all fashion categories with slug, descriptions, and product counts.

### `GET /api/products`
Retrieves paginated and filtered product catalogue.
- **Query Parameters:**
  - `search` (string): Search query across product name, description, brand, and fabric.
  - `category` (string): Category slug (e.g. `womens-dresses`, `summer-linen`).
  - `size` (string): Garment size (`XS`, `S`, `M`, `L`, `XL`).
  - `color` (string): Color filter (`Black`, `White`, `Navy`, `Olive`, `Beige`, etc.).
  - `min_price`, `max_price` (float): Price range filters.
  - `min_rating` (float): Minimum average star rating (e.g. `4.0`).
  - `in_stock` (bool): If `true`, returns only items with positive inventory.
  - `featured` (bool): Filter items flagged for promotional highlight.
  - `sort` (enum): `popular`, `rating`, `price_asc`, `price_desc`, `newest`.
  - `page` (int, default 1), `per_page` (int, default 12).
- **Response `200 OK`:**
  ```json
  {
    "products": [ ... ],
    "pagination": {
      "page": 1,
      "per_page": 12,
      "total_items": 74,
      "total_pages": 7,
      "has_next": true,
      "has_prev": false
    }
  }
  ```

### `GET /api/products/<id>`
Returns complete product details, image gallery, all size/color variants with inventory status, ratings breakdown (1-5 stars), and recent verified patron reviews.

### `GET /api/products/<id>/recommendations`
Returns top related garment recommendations calculated via the MCA project synopsis formula:
$$\text{Score} = 0.40 \cdot S_{\text{cat}} + 0.25 \cdot S_{\text{price}} + 0.20 \cdot S_{\text{rating}} + 0.15 \cdot S_{\text{pop}}$$
- **Response `200 OK`:**
  ```json
  {
    "product_id": 1,
    "algorithm": "MCA-weighted-ranking",
    "weights": {
      "category_match": 0.40,
      "price_match": 0.25,
      "rating": 0.20,
      "popularity": 0.15
    },
    "recommendations": [
      {
        "product": { ... },
        "score": 0.9425,
        "breakdown": {
          "category_score": 1.0,
          "price_score": 0.95,
          "rating_score": 0.92,
          "popularity_score": 0.86
        }
      }
    ]
  }
  ```

---

## 3. Shopping Cart Endpoints (`/api/cart`)
*(All require `Authorization: Bearer <token>`)*

- `GET /api/cart`: Returns cart items, live item quantities, subtotals, tax (8%), shipping, and total.
- `POST /api/cart`: Body `{ "variant_id": 12, "quantity": 1 }`. Validates stock before adding.
- `PUT /api/cart/<id>`: Body `{ "quantity": 2 }`. Validates variant stock availability.
- `DELETE /api/cart/<id>`: Removes single item from cart.
- `DELETE /api/cart`: Clears entire cart.

---

## 4. Wishlist Endpoints (`/api/wishlist`)
*(All require `Authorization: Bearer <token>`)*

- `GET /api/wishlist`: Returns user's saved wishlist products.
- `POST /api/wishlist/toggle`: Body `{ "product_id": 5 }`. Adds if not present; removes if already saved.
- `DELETE /api/wishlist/<product_id>`: Removes item from wishlist.

---

## 5. Coupon & Promotional Endpoints (`/api/coupons`)

### `POST /api/coupons/validate`
Validates a coupon against a shopping bag subtotal.
- **Request Body:**
  ```json
  {
    "code": "WELCOME15",
    "subtotal": 148.0
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "valid": true,
    "message": "Coupon 'WELCOME15' applied! You saved $22.20.",
    "coupon": {
      "code": "WELCOME15",
      "discount_type": "percentage",
      "discount_value": 15.0,
      "discount_amount": 22.20,
      "new_subtotal": 125.80
    }
  }
  ```

### `GET /api/coupons/active`
Returns list of currently active public promotional discount vouchers.

---

## 6. Orders & Checkout Endpoints (`/api/orders`)
*(All require `Authorization: Bearer <token>`)*

### `POST /api/orders`
Authorizes checkout, deducts variant stock atomically, records payment simulation, applies coupon, and clears user's cart.
- **Request Body:**
  ```json
  {
    "address_id": 1,
    "payment_method": "card",
    "coupon_code": "WELCOME15",
    "notes": "Please deliver to concierge desk."
  }
  ```
- **Response `201 Created`:** Returns complete order record with tracking number and order items.

### `GET /api/orders`
Returns past order history for authenticated user.

### `GET /api/orders/<id>`
Returns details, items, payment transaction, and return requests for a specific order.

### `POST /api/orders/<id>/cancel`
Cancels pending/processing order, triggers refund, and restores variant inventory.

### `POST /api/orders/<id>/return-request`
Logs a formal return or refund request for delivered orders.
- **Request Body:**
  ```json
  {
    "request_type": "return",
    "reason": "Size slightly larger than expected",
    "customer_notes": "Requesting exchange for size S."
  }
  ```

---

## 7. Customer Reviews & Notifications

- `GET /api/products/<id>/reviews`: Returns public reviews and star ratings.
- `POST /api/products/<id>/reviews`: Submits verified customer review with rating (1-5), headline, and comment. Automatically recalculates product average rating.
- `GET /api/notifications`: Returns in-app notifications and unread badge count.
- `PUT /api/notifications/<id>/read`: Marks individual notification as read.
- `PUT /api/notifications/read-all`: Marks all notifications as read.

---

## 8. Admin Control Endpoints (`/api/admin/*`)
*(Requires `Authorization: Bearer <token>` with `role: "admin"`)*

- `GET /api/admin/metrics`: Summary KPIs (Revenue, Orders, Patrons, Catalogue, Low Stock, Pending Returns, Status distribution).
- `GET /api/admin/products`: Full product listing with pagination and search.
- `POST /api/admin/products`: Creates new product with images and variants.
- `PUT /api/admin/products/<id>`: Updates product metadata and pricing.
- `DELETE /api/admin/products/<id>`: Cascades deletion of product and its variants.
- `GET /api/admin/inventory`: Variant inventory matrix highlighting low stock (<10 units).
- `PUT /api/admin/inventory/<variant_id>`: Restocks variant units directly.
- `GET /api/admin/orders`: List all orders with status filtering.
- `PUT /api/admin/orders/<id>/status`: Transitions order status (`processing`, `shipped`, `delivered`, `cancelled`) and records air waybill tracking number.
- `GET /api/admin/requests`: Lists cancellation, return, and refund requests.
- `PUT /api/admin/requests/<id>`: Approves or rejects request; triggers automatic inventory and payment refund synchronization.
- `GET /api/admin/coupons` & `POST /api/admin/coupons`: Manages discount vouchers.
- `GET /api/admin/customers`: Customer directory with lifetime spend metrics.
