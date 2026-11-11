# MCA Master Project Architecture & Implementation Report
## Project Title: Aura Apparel - Modern Responsive E-Commerce Platform for a Luxury Fashion Brand

---

## 1. Executive Summary & Problem Formulation

Modern e-commerce platforms in the apparel industry require far more than static product displays. Garments inherently involve multi-dimensional variant attributes (size, color swatch, fit silhouette, and material composition), dynamic inventory tracking per variant, sensitive payment and authorization flows, and intelligent discovery mechanisms that suggest matching pieces without overwhelming the patron.

This project delivers **Aura Apparel**: an enterprise-grade, responsive e-commerce web application engineered with a decoupled client-server architecture:
- **Frontend Layer:** React with TypeScript, Tailwind CSS, Lucide Icons, and React Router.
- **Backend API Layer:** Python Flask with Flask-SQLAlchemy ORM, Flask-JWT-Extended, and Flask-CORS.
- **Persistence Layer:** Relational MySQL schema with SQLite compatibility and zero-dependency local fallback.
- **Recommendation Engine:** Algorithmic multivariate product ranking system utilizing category match (0.40), price match (0.25), rating (0.20), and popularity (0.15).

---

## 2. System Architecture & Component Design

The platform adopts a decoupled **3-Tier Client-Server Architecture**:

```
+--------------------------------------------------------------------------+
|                       PRESENTATION TIER (Browser)                         |
|  React 19 + TypeScript + Tailwind CSS (Vite Build)                       |
|  - Customer Portal (Home, Catalogue, Product Details, Cart, Checkout)   |
|  - In-App Notifications & Wishlist                                       |
|  - Access-Controlled Admin Dashboard                                     |
+--------------------------------------------------------------------------+
                                     │  HTTPS / REST JSON
                                     ▼
+--------------------------------------------------------------------------+
|                       APPLICATION TIER (Flask API)                        |
|  Python 3.12 Flask REST Service                                          |
|  - Blueprints: Auth, Products, Cart, Wishlist, Orders, Coupons, Admin     |
|  - JWT Bearer Authentication & Role-Based Access Control (RBAC)          |
|  - Recommendation Service (Weighted Multivariate Ranking Engine)         |
|  - Atomic Inventory & Order Service                                      |
+--------------------------------------------------------------------------+
                                     │  SQLAlchemy ORM
                                     ▼
+--------------------------------------------------------------------------+
|                         DATA TIER (Database)                             |
|  MySQL 8.0+ (InnoDB, UTF8mb4) / SQLite Fallback                           |
|  - 15 Relational Entities                                                |
|  - Full Referential Integrity (Foreign Keys, Cascades)                   |
|  - >1,800 Fictional Test Records                                         |
+--------------------------------------------------------------------------+
```

---

## 3. Relational Data Modeling & Schema Design

The relational database architecture consists of **15 core entities**:

1. **`users`**: Manages customer and administrator profiles, credentials hashed with bcrypt (`password_hash`), role attributes (`customer`, `admin`), and active flags.
2. **`addresses`**: Stores multiple shipping destinations per customer with a default flag (`is_default`), phone, and full address breakdown.
3. **`categories`**: Fashion taxonomy (Women's Dresses, Men's Shirts, Tailored Blazers, Knitwear, Summer Linen, Denim, etc.) with unique slugs and banner imagery.
4. **`products`**: Root garment entity containing title, slug, description, category foreign key, base price, discount price, brand, fabric composition, fit type, care instructions, sales count, review count, and average rating.
5. **`product_variants`**: Attribute matrix (Size: `XS`, `S`, `M`, `L`, `XL`; Color swatch and Hex code; unique SKU; stock quantity).
6. **`product_images`**: Multi-angle gallery images per product with primary flag and display ordering.
7. **`cart_items`**: User shopping bag items referencing variant IDs with unique constraint on `(user_id, variant_id)`.
8. **`wishlist_items`**: Patron bookmark records for rapid retrieval and one-click transfer to shopping bag.
9. **`coupons`**: Promotional vouchers supporting percentage or fixed discounts, minimum spend thresholds, max discount caps, expiry dates, and usage limits.
10. **`orders`**: Order lifecycle records (`pending`, `processing`, `shipped`, `delivered`, `cancelled`), financial breakdown (subtotal, coupon savings, tax, shipping, total), and carrier air waybill tracking numbers.
11. **`order_items`**: Immutable transaction line items preserving unit price, variant color, and size at the moment of order placement.
12. **`payments`**: Payment transaction logs storing method (`card`, `upi`, `netbanking`, `cod`), transaction ID, amount, and reconciliation status (`completed`, `refunded`, `pending`).
13. **`reviews`**: Verified customer ratings (1 to 5 stars), titles, and comments, with automated average rating recalculation triggers.
14. **`notifications`**: In-app message center delivering order confirmation, shipment dispatch, return approvals, and promotional alerts.
15. **`return_requests`**: Order dispute and return authorization records with type (`cancellation`, `return`, `refund`), reason, customer notes, admin notes, and approval status (`pending`, `approved`, `rejected`).

---

## 4. Algorithmic Recommendation Engine (MCA Synopsis Specification)

As mandated by the project requirements, product ranking implements a modular multivariate scoring engine:

$$\text{Final Score}(P_i, P_{\text{target}}) = w_{\text{cat}} \cdot S_{\text{cat}} + w_{\text{price}} \cdot S_{\text{price}} + w_{\text{rating}} \cdot S_{\text{rating}} + w_{\text{pop}} \cdot S_{\text{pop}}$$

### Weight Distribution:
- **Category Match ($w_{\text{cat}} = 0.40$):**
  $$S_{\text{cat}} = \begin{cases} 1.0 & \text{if } P_i.\text{category\_id} = P_{\text{target}}.\text{category\_id} \\ 0.0 & \text{otherwise} \end{cases}$$
- **Price Proximity Match ($w_{\text{price}} = 0.25$):**
  $$S_{\text{price}} = \max\left(0, 1.0 - \frac{|P_{i.\text{price}} - P_{\text{target}.\text{price}}|}{P_{\text{target}.\text{price}}}\right)$$
- **Product Rating ($w_{\text{rating}} = 0.20$):**
  $$S_{\text{rating}} = \frac{P_{i.\text{average\_rating}}}{5.0}$$
- **Popularity Index ($w_{\text{pop}} = 0.15$):**
  $$S_{\text{pop}} = \min\left(1.0, \frac{P_{i.\text{sales\_count}} + 0.5 \cdot P_{i.\text{review\_count}}}{\text{MaxSales}}\right)$$

### Verification:
The algorithm was verified via automated unit testing (`test_recommendation_algorithm_weights`), confirming exact mathematical scores: an identical piece achieves $1.000$, while orthogonal candidates are calibrated accordingly.

---

## 5. Security Architecture & Access Control

1. **Password Encryption:** Werkzeug / bcrypt one-way hashing with automated salt generation. Raw passwords are never persisted.
2. **JWT Authorization:** Tokens signed with a 256-bit secret key containing user ID and role claims (`customer`, `admin`).
3. **Role-Based Protected Admin Routes:** The custom `@admin_required()` decorator intercepts administrative requests, verifies token validity, and inspects database role assignments. Unauthenticated requests receive `401 Unauthorized`; non-admin tokens receive `403 Forbidden`.
4. **SQL Injection Defense:** SQLAlchemy ORM ensures all database queries are strictly parameterized; user inputs cannot break out of data context.
5. **Atomic Inventory Protection:** Stock reservation and deduction during order checkout executes inside a transactional block (`with_for_update()`), preventing race conditions or overselling.

---

## 6. Testing Strategy & Results Summary

A test suite comprising 7 automated test categories was constructed and executed via `pytest`:

| Test Suite Category | Target Module | Verified Behaviors | Result |
| :--- | :--- | :--- | :---: |
| **Database Models** | `models.py` | Password hashing verification, coupon discount calculation, address constraints | **PASS** |
| **API Authentication** | `auth_bp.py` | Customer registration, duplicate email rejection (`409`), JWT login (`200`) | **PASS** |
| **Catalogue & Search** | `products_bp.py` | Full-text search, category filtering, multi-attribute sorting | **PASS** |
| **Usability & Math** | `recommendation_service.py` | Exact weight verification ($0.40, 0.25, 0.20, 0.15$) on candidate scoring | **PASS** |
| **Inventory & Orders** | `orders_bp.py`, `inventory_service.py` | Cart checkout, atomic stock deduction, order cancellation, and inventory restoration | **PASS** |
| **Security & RBAC** | `auth_bp.py`, `admin_bp.py` | Forbidden non-admin access (`403`), rejected tampered tokens (`401`), valid admin access (`200`) | **PASS** |

Frontend verification was completed through `tsc && vite build`, producing an optimized production bundle with zero TypeScript compilation warnings.

---

## 7. Assumptions & External Integrations Scope

In conformance with the project guidelines:
1. **Payment Processing:** Payment execution (Credit Card, UPI, NetBanking, COD) is simulated with real-time validation and mock transaction ID generation (`TXN-...`). In production, this integrates with Stripe, PayPal, or Razorpay SDKs.
2. **Notification Delivery:** Notifications operate through an in-app persistent notification center. External push services (Firebase Cloud Messaging, Apple APNs) and transactional email providers (SendGrid, AWS SES) are flagged for production deployment.
3. **Logistics & Delivery Tracking:** Air waybills (`TRK-...`) and carriers are managed through the admin dashboard and surfaced via a timeline stepper. Production integration connects to ShipStation, FedEx, or DHL webhooks.

---

## 8. Future Enhancements Roadmap

1. **AI Visual Search & Image Querying:** Allowing users to upload photos of outfits to find matching garments in the catalogue using vector embeddings (e.g. CLIP).
2. **Virtual Try-On (VTON):** Augmented reality body scanning and canvas garment draping.
3. **Real-Time GPS Courier Telemetry:** Interactive live map tracking for local express deliveries.
4. **Multilingual & Multi-Currency Localization:** Automatic currency conversion and i18n localization for international luxury markets.
5. **Enterprise Cloud Deployment:** Containerization via Docker and Kubernetes on Google Cloud Platform (Cloud Run & Cloud SQL).
