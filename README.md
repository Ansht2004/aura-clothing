# Aura Apparel - Modern E-Commerce Platform

A professional, responsive e-commerce website for **Aura Apparel**, a modern clothing brand. Built for desktop, tablet, and mobile browsers with a React TypeScript frontend, Python Flask REST API, and relational MySQL/SQLite database with SQLAlchemy ORM.

Developed as a comprehensive MCA Master Project implementation following the project synopsis specifications, complete with an algorithmic product-ranking recommendation engine, atomic inventory management, verified reviews, and a separate, access-controlled web-based administrative dashboard.

---

## Key Features

### Customer Website
- **Authentication & Profiles:** Registration, login, logout, profile update, password change, and multi-address management with default flags.
- **Brand Identity & Experience:** Luxury minimalist aesthetic (Aura Apparel), high-res imagery, typography, announcement bar, and mobile responsive drawer.
- **Product Discovery:** Search by title/brand/fabric, filtering by category, size (`XS`-`XL`), color swatches, price range, minimum rating, and in-stock toggle. Multi-criteria sorting (Popularity, Rating, Price Low-High, Price High-Low, Newest).
- **Product Details:** Multi-image gallery, interactive color and size swatches with real-time variant stock checks, accordion tabs for materials and care instructions, verified buyer reviews with star distribution, and **MCA Product Ranking Recommendations** ("You May Also Like").
- **Shopping Bag & Wishlist:** Real-time quantity updates, subtotal, tax (8%), complimentary shipping progress bar ($100 threshold), and one-click wishlist transfers.
- **Promotional Coupons:** Instant voucher validation with real-time savings feedback (e.g., `WELCOME15`, `LUXE20`).
- **Checkout & Payment:** Step-by-step accordion checkout (Address selection -> Shipping method -> Payment simulation: Card, UPI, NetBanking, COD -> Order placement).
- **Order Tracking & Lifecycle:** Visual 4-stage tracking stepper (`Placed` -> `Processing` -> `Shipped` -> `Delivered`). Instant invoice download/print.
- **Cancellations, Returns & Refunds:** Direct cancellation for processing orders with automatic inventory restoration; return/refund request filing for delivered orders.
- **In-App Notification Center:** Real-time notification badge with order confirmation, dispatch updates, and promotional alerts.

### Access-Controlled Admin Dashboard (`/admin`)
- **Protected RBAC Access:** Dedicated dashboard restricted to administrator accounts (`role: 'admin'`).
- **Executive Metrics & KPIs:** Total revenue, total orders, total patrons, active catalogue count, critical low-stock count, pending return requests, and order pipeline distribution.
- **Catalogue CRUD:** Add, edit, and delete products, categories, descriptions, image URLs, and pricing.
- **Variant Inventory Monitor:** Real-time stock management per size and color with instant restock modal and low-stock alerts (<10 units).
- **Orders & Tracking Management:** Update lifecycle statuses (`processing`, `shipped`, `delivered`, `cancelled`) and record air waybill tracking numbers and carriers.
- **Cancellation & Return Processing:** Review patron return requests with Approve (triggers payment refund and inventory return) or Reject options and admin response notes.
- **Voucher / Coupon Management:** Publish discount codes with percentage/fixed types, minimum spend, and usage caps.
- **Patrons Directory:** Review customer accounts with order counts and lifetime spend statistics.

---

## Default Demo Accounts

For rapid testing and grading, pre-configured fictional accounts are available in the system:

| Role | Email | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@auraapparel.com` | `Admin@123456` | Full administrative control (`/admin`) |
| **Demo Customer** | `customer@auraapparel.com` | `Customer@123456` | Shopping bag, orders, wishlist, profile |

*(Note: The Sign-In screen also includes **One-Click Demo Login** buttons that automatically prefill and authenticate these accounts!)*

---

## Active Promotional Vouchers

| Voucher Code | Discount | Minimum Spend | Description |
| :--- | :--- | :--- | :--- |
| `WELCOME15` | **15% OFF** | $50.00 | New patron welcome promotion |
| `LUXE20` | **20% OFF** | $150.00 | Luxury collection promotional voucher |
| `SUMMER25` | **25% OFF** | $200.00 | Summer linen collection promotion |
| `FLAT30` | **$30 FLAT** | $120.00 | Fixed dollar discount on qualifying orders |

---

## Technology Stack

- **Frontend:** React 19, TypeScript, Tailwind CSS, Lucide React, React Router 7, Vite.
- **Backend:** Python 3.12, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS, PyMySQL, Werkzeug.
- **Database:** MySQL 8.0+ / SQLite (Zero-dependency instant local execution with seamless MySQL connector).
- **Test Suite:** Pytest with 7 comprehensive functional, API, database, usability, and security test suites.

---

## Quick Start & Setup Instructions

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ and npm installed

### Option A: One-Click Master Launcher (Recommended)
Simply double-click **`START_AURA_CLOTHING.bat`** in the project root:
1. Clears any stale or hanging processes holding port 5000 or 3000.
2. Boots the Flask REST API on `http://127.0.0.1:5000`.
3. Performs an automated health check verifying the database and API endpoints.
4. Boots the React Vite frontend on `http://localhost:3000`.
5. Automatically opens `http://localhost:3000` in your default browser.

To stop both servers cleanly at any time, run **`STOP_AURA_CLOTHING.bat`**.

You can also run them individually with `run_backend.bat` and `run_frontend.bat`.

---

### Option B: Manual Command-Line Execution

#### 1. Backend Setup & Run
```powershell
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database with >1,800 fictional test records
python seed_data.py

# Run the Flask REST API server
python app.py
```
*API will be available at `http://localhost:5000` with health check at `http://localhost:5000/api/health`.*

#### 2. Frontend Setup & Run
```powershell
cd frontend

# Install node dependencies
npm install

# Run the development server
npm run dev
```
*Frontend will be live at `http://localhost:3000`.*

---

## MySQL Database Configuration

The application natively supports MySQL via SQLAlchemy. To connect to an existing MySQL server:

1. Create the MySQL database:
   ```sql
   CREATE DATABASE aura_clothing CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Set the `DATABASE_URL` environment variable before running:
   ```powershell
   $env:DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/aura_clothing"
   ```
3. Run `python seed_data.py` to initialize tables and seed records, or run the provided DDL script:
   ```powershell
   mysql -u root -p aura_clothing < backend/schema_mysql.sql
   ```
*If `DATABASE_URL` is omitted, the application seamlessly defaults to SQLite (`aura_clothing.db`), allowing full functionality without requiring an external MySQL server running.*

---

## Running Automated Tests

A comprehensive automated test suite covers functional, API, database, usability, and security tests:

```powershell
cd backend
.\venv\Scripts\activate
python -m pytest --rootdir="." -v
```

All 7 test suites pass with 100% success rate:
- `test_user_password_hashing`: Verifies bcrypt one-way password hashing.
- `test_coupon_validation_and_calculation`: Verifies discount formulas and spend limits.
- `test_user_registration_and_login`: Tests customer registration and JWT issuance.
- `test_product_listing_and_filtering`: Tests catalogue search, filters, and pagination.
- `test_recommendation_algorithm_weights`: Verifies the exact MCA weights (0.40, 0.25, 0.20, 0.15).
- `test_cart_order_inventory_lifecycle`: Verifies atomic stock deduction and order cancellation stock restoration.
- `test_security_and_rbac`: Verifies protected admin routes, token tampering rejection, and 403 Forbidden checks.

---

## Project Structure

```
aura-clothing/
├── README.md                      # Setup, run, and feature documentation
├── API_DOCUMENTATION.md           # Full REST API endpoints and payloads specification
├── MCA_PROJECT_REPORT.md          # Architectural report, ER diagrams, and algorithms
├── run_backend.bat                # One-click backend launcher
├── run_frontend.bat               # One-click frontend launcher
├── run_tests.bat                  # One-click test suite executor
├── seed_database.bat              # Database seeder launcher
│
├── backend/                       # Python Flask REST API
│   ├── app.py                     # App factory, CORS, JWT & Blueprint registration
│   ├── config.py                  # Environment configurations & database URI
│   ├── models.py                  # 15 SQLAlchemy relational database models
│   ├── schema_mysql.sql           # Complete MySQL DDL export script
│   ├── seed_data.py               # Database seeder (>1,800 fictional test records)
│   ├── requirements.txt           # Python backend dependencies
│   ├── pytest.ini                 # Pytest configuration
│   ├── blueprints/                # Modular Flask route controllers
│   │   ├── auth_bp.py             # User registration, login, profile, RBAC
│   │   ├── products_bp.py         # Catalogue search, filters, details
│   │   ├── cart_bp.py             # Shopping bag management
│   │   ├── wishlist_bp.py         # Wishlist bookmarks
│   │   ├── addresses_bp.py        # Delivery address CRUD
│   │   ├── coupons_bp.py          # Voucher validation & calculations
│   │   ├── orders_bp.py           # Checkout, orders, cancellations, returns
│   │   ├── reviews_bp.py          # Customer star ratings & reviews
│   │   ├── notifications_bp.py    # In-app notification center
│   │   ├── admin_bp.py            # Administrative control & metrics
│   │   └── recommendations_bp.py  # Personalized & trending endpoints
│   ├── services/
│   │   ├── recommendation_service.py # MCA weighted ranking algorithm (0.40, 0.25, 0.20, 0.15)
│   │   └── inventory_service.py   # Atomic stock check, reservation, and rollback
│   └── tests/
│       ├── conftest.py            # Pytest test fixtures
│       └── test_backend.py        # 7 automated test suites
│
└── frontend/                      # React TypeScript Client
    ├── index.html                 # HTML shell with Google Fonts
    ├── package.json               # Frontend dependencies & scripts
    ├── vite.config.ts             # Vite configuration
    ├── tailwind.config.js         # Tailwind luxury theme styling
    ├── tsconfig.json              # TypeScript compiler settings
    └── src/
        ├── App.tsx                # Client router & context providers
        ├── main.tsx               # React application entry point
        ├── index.css              # Global styling & Tailwind directives
        ├── types/                 # TypeScript interfaces & types
        │   └── index.ts
        ├── services/
        │   └── api.ts             # Centralized typed REST client
        ├── context/
        │   ├── AuthContext.tsx    # User session & JWT state
        │   ├── CartContext.tsx    # Shopping bag & voucher calculations
        │   ├── WishlistContext.tsx# Saved items state
        │   └── NotificationContext.tsx # Message alerts state
        ├── components/
        │   ├── common/            # Reusable UI components
        │   │   ├── Navbar.tsx     # Responsive navigation & search
        │   │   ├── Footer.tsx     # Brand footer, newsletter & links
        │   │   ├── ProductCard.tsx# Garment card with wishlist & badge
        │   │   ├── ReviewStars.tsx# Star rating visualizer
        │   │   ├── LoadingSpinner.tsx
        │   │   └── EmptyState.tsx
        │   └── admin/
        │       └── AdminRoute.tsx # Protected administrator route guard
        └── pages/
            ├── HomePage.tsx       # Hero, categories, promotions & trending
            ├── ProductListPage.tsx# Search, multi-attribute filter sidebar
            ├── ProductDetailPage.tsx # Gallery, swatches, reviews, recommendations
            ├── CartPage.tsx       # Shopping bag & coupon voucher input
            ├── CheckoutPage.tsx   # Step-by-step payment & order placement
            ├── OrderConfirmationPage.tsx # Receipt & tracking timeline
            ├── OrderHistoryPage.tsx# Past orders & return requests
            ├── WishlistPage.tsx   # Bookmark collection
            ├── ProfilePage.tsx    # Profile details & address book
            ├── AuthPage.tsx       # Sign In / Register with demo buttons
            └── AdminDashboard.tsx # Comprehensive admin control suite
```
