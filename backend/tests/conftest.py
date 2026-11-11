import pytest
import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, User, Category, Product, ProductVariant, Coupon, Address

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()

        # Seed minimal test fixtures
        admin = User(email="testadmin@aura.com", full_name="Admin User", role="admin")
        admin.set_password("AdminPass123!")

        customer = User(email="testcustomer@aura.com", full_name="Customer User", role="customer")
        customer.set_password("CustomerPass123!")

        db.session.add_all([admin, customer])
        db.session.commit()

        cat = Category(name="Test Dresses", slug="test-dresses", description="Category for testing")
        db.session.add(cat)
        db.session.commit()

        prod = Product(
            name="Classic Silk Dress",
            slug="classic-silk-dress",
            description="Luxury silk dress",
            category_id=cat.id,
            base_price=100.0,
            discount_price=80.0,
            average_rating=4.5,
            sales_count=20
        )
        db.session.add(prod)
        db.session.commit()

        variant = ProductVariant(
            product_id=prod.id,
            size="M",
            color="Black",
            color_hex="#000000",
            sku="TST-SLK-M-BLK",
            stock_quantity=15
        )
        db.session.add(variant)

        coupon = Coupon(
            code="SAVE20",
            discount_type="percentage",
            discount_value=20.0,
            min_order_amount=50.0,
            is_active=True
        )
        db.session.add(coupon)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def customer_token(client):
    res = client.post('/api/auth/login', json={
        'email': 'testcustomer@aura.com',
        'password': 'CustomerPass123!'
    })
    return res.get_json()['access_token']

@pytest.fixture
def admin_token(client):
    res = client.post('/api/auth/login', json={
        'email': 'testadmin@aura.com',
        'password': 'AdminPass123!'
    })
    return res.get_json()['access_token']
