import pytest
from models import db, User, Product, Category, ProductVariant, Coupon
from services.recommendation_service import RecommendationEngine

# -------------------------------------------------------------
# 1. Database Model Tests
# -------------------------------------------------------------
def test_user_password_hashing(app):
    with app.app_context():
        user = User(email="unique@aura.com", full_name="Unique User")
        user.set_password("MySecretPass#2026")
        assert user.password_hash != "MySecretPass#2026"
        assert user.check_password("MySecretPass#2026") is True
        assert user.check_password("WrongPassword") is False

def test_coupon_validation_and_calculation(app):
    with app.app_context():
        coupon = Coupon(
            code="SPRING10",
            discount_type="percentage",
            discount_value=10.0,
            min_order_amount=100.0,
            is_active=True
        )
        # Below min order
        valid, msg = coupon.is_valid(subtotal=80.0)
        assert valid is False
        assert "Minimum order subtotal" in msg

        # Meets min order
        valid, msg = coupon.is_valid(subtotal=150.0)
        assert valid is True
        discount = coupon.calculate_discount(150.0)
        assert discount == 15.0  # 10% of 150

# -------------------------------------------------------------
# 2. Functional & API Authentication Tests
# -------------------------------------------------------------
def test_user_registration_and_login(client):
    # Register new customer
    reg_res = client.post('/api/auth/register', json={
        'email': 'newshopper@aura.com',
        'password': 'SecurePassword123',
        'full_name': 'New Shopper',
        'phone': '1234567890'
    })
    assert reg_res.status_code == 201
    data = reg_res.get_json()
    assert 'access_token' in data
    assert data['user']['email'] == 'newshopper@aura.com'

    # Duplicate registration should fail
    dup_res = client.post('/api/auth/register', json={
        'email': 'newshopper@aura.com',
        'password': 'AnotherPassword',
        'full_name': 'Duplicate User'
    })
    assert dup_res.status_code == 409

    # Successful login
    login_res = client.post('/api/auth/login', json={
        'email': 'newshopper@aura.com',
        'password': 'SecurePassword123'
    })
    assert login_res.status_code == 200
    assert 'access_token' in login_res.get_json()

# -------------------------------------------------------------
# 3. Product Listing & Filtering API Tests
# -------------------------------------------------------------
def test_product_listing_and_filtering(client):
    res = client.get('/api/products')
    assert res.status_code == 200
    data = res.get_json()
    assert 'products' in data
    assert len(data['products']) >= 1

    # Search filter
    search_res = client.get('/api/products?search=Silk')
    assert search_res.status_code == 200
    assert len(search_res.get_json()['products']) >= 1

# -------------------------------------------------------------
# 4. Usability & Recommendation System Weighted Math Tests
# -------------------------------------------------------------
def test_recommendation_algorithm_weights(app):
    """
    Verifies that the product recommendation engine precisely respects the
    MCA synopsis weights:
      Category: 0.40
      Price:    0.25
      Rating:   0.20
      Pop:      0.15
    """
    engine = RecommendationEngine(w_cat=0.40, w_price=0.25, w_rating=0.20, w_pop=0.15)
    with app.app_context():
        target = Product(
            id=10, category_id=1, base_price=100.0, discount_price=100.0,
            average_rating=5.0, sales_count=50, review_count=0
        )
        # Candidate 1: Same category, exact price, 5-star, max pop
        cand1 = Product(
            id=11, category_id=1, base_price=100.0, discount_price=100.0,
            average_rating=5.0, sales_count=50, review_count=0
        )
        score1 = engine.score_candidate(target, cand1, max_sales=50.0)
        # Should achieve perfect 1.0 (0.40*1 + 0.25*1 + 0.20*1 + 0.15*1)
        assert score1['score'] == 1.0
        assert score1['breakdown']['category_score'] == 1.0
        assert score1['breakdown']['price_score'] == 1.0
        assert score1['breakdown']['rating_score'] == 1.0
        assert score1['breakdown']['popularity_score'] == 1.0

        # Candidate 2: Different category (cat=0), different price (50% diff -> price=0.5)
        cand2 = Product(
            id=12, category_id=2, base_price=150.0, discount_price=150.0,
            average_rating=2.5, sales_count=0, review_count=0
        )
        score2 = engine.score_candidate(target, cand2, max_sales=50.0)
        # Cat: 0.0 * 0.40 = 0.0
        # Price: (1 - 50/100) = 0.5 * 0.25 = 0.125
        # Rating: 2.5/5.0 = 0.5 * 0.20 = 0.10
        # Pop: 0.0 * 0.15 = 0.0
        # Total = 0.225
        assert score2['score'] == 0.225

# -------------------------------------------------------------
# 5. Cart, Coupon, Order & Inventory Lifecycle Tests
# -------------------------------------------------------------
def test_cart_order_inventory_lifecycle(client, customer_token, app):
    headers = {'Authorization': f'Bearer {customer_token}'}

    with app.app_context():
        variant = ProductVariant.query.filter_by(sku="TST-SLK-M-BLK").first()
        initial_stock = variant.stock_quantity
        variant_id = variant.id

    # 1. Add to cart
    add_res = client.post('/api/cart', json={'variant_id': variant_id, 'quantity': 2}, headers=headers)
    assert add_res.status_code == 201

    # 2. View cart
    cart_res = client.get('/api/cart', headers=headers)
    assert cart_res.status_code == 200
    assert cart_res.get_json()['summary']['item_count'] == 2

    # 3. Add delivery address
    addr_res = client.post('/api/addresses', json={
        'full_name': 'Test Customer',
        'phone': '5551234567',
        'address_line1': '100 Broadway',
        'city': 'New York',
        'state': 'NY',
        'postal_code': '10001'
    }, headers=headers)
    assert addr_res.status_code == 201
    address_id = addr_res.get_json()['address']['id']

    # 4. Validate coupon
    coupon_res = client.post('/api/coupons/validate', json={'code': 'SAVE20', 'subtotal': 160.0})
    assert coupon_res.status_code == 200
    assert coupon_res.get_json()['valid'] is True

    # 5. Place order
    checkout_res = client.post('/api/orders', json={
        'address_id': address_id,
        'payment_method': 'card',
        'coupon_code': 'SAVE20'
    }, headers=headers)
    assert checkout_res.status_code == 201
    order_data = checkout_res.get_json()['order']
    order_id = order_data['id']
    assert order_data['discount_amount'] > 0

    # 6. Verify inventory was deducted atomically
    with app.app_context():
        updated_variant = ProductVariant.query.get(variant_id)
        assert updated_variant.stock_quantity == initial_stock - 2

    # 7. Customer cancels order -> verify inventory is restored
    cancel_res = client.post(f'/api/orders/{order_id}/cancel', json={'reason': 'Changed mind'}, headers=headers)
    assert cancel_res.status_code == 200

    with app.app_context():
        restored_variant = ProductVariant.query.get(variant_id)
        assert restored_variant.stock_quantity == initial_stock

# -------------------------------------------------------------
# 6. Security & Role-Based Access Control (RBAC) Tests
# -------------------------------------------------------------
def test_security_and_rbac(client, customer_token, admin_token):
    # Customer trying to access Admin metrics must receive 403 Forbidden
    cust_res = client.get('/api/admin/metrics', headers={'Authorization': f'Bearer {customer_token}'})
    assert cust_res.status_code == 403

    # Unauthenticated request must receive 401 Unauthorized
    unauth_res = client.get('/api/admin/metrics')
    assert unauth_res.status_code == 401

    # Tampered/invalid token must receive 401
    tampered_res = client.get('/api/admin/metrics', headers={'Authorization': 'Bearer invalid.tampered.token'})
    assert tampered_res.status_code == 401

    # Administrator can successfully access Admin metrics
    admin_res = client.get('/api/admin/metrics', headers={'Authorization': f'Bearer {admin_token}'})
    assert admin_res.status_code == 200
    assert 'overview' in admin_res.get_json()
