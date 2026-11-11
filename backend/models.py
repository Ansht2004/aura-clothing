from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def utcnow():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), default='customer', nullable=False)  # 'customer', 'admin'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    addresses = db.relationship('Address', backref='user', cascade='all, delete-orphan', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', cascade='all, delete-orphan', lazy=True)
    wishlist_items = db.relationship('WishlistItem', backref='user', cascade='all, delete-orphan', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', cascade='all, delete-orphan', lazy=True)
    return_requests = db.relationship('ReturnRequest', backref='user', lazy=True)

    @property
    def customer_code(self):
        if self.role == 'admin':
            return f"AUR-ADM-{self.id:04d}"
        return f"AUR-CUST-{self.id:04d}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_code': self.customer_code,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='United States', nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'phone': self.phone,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'is_featured': self.is_featured,
            'product_count': len(self.products) if self.products else 0
        }


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    base_price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True)
    brand = db.Column(db.String(100), default='Aura Apparel', nullable=False)
    material = db.Column(db.String(100), nullable=True)
    fit_type = db.Column(db.String(50), nullable=True)  # Slim, Regular, Relaxed, Oversized
    care_instructions = db.Column(db.Text, nullable=True)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    average_rating = db.Column(db.Float, default=0.0, nullable=False)
    review_count = db.Column(db.Integer, default=0, nullable=False)
    sales_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    variants = db.relationship('ProductVariant', backref='product', cascade='all, delete-orphan', lazy=True)
    images = db.relationship('ProductImage', backref='product', cascade='all, delete-orphan', lazy=True, order_by='ProductImage.display_order')
    reviews = db.relationship('Review', backref='product', cascade='all, delete-orphan', lazy=True, order_by='desc(Review.created_at)')
    wishlist_items = db.relationship('WishlistItem', backref='product', cascade='all, delete-orphan', lazy=True)

    @property
    def total_stock(self):
        return sum(v.stock_quantity for v in self.variants) if self.variants else 0

    @property
    def in_stock(self):
        return self.total_stock > 0

    @property
    def primary_image(self):
        for img in self.images:
            if img.is_primary:
                return img.image_url
        if self.images:
            return self.images[0].image_url
        return 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?auto=format&fit=crop&w=600&q=80'

    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'category_slug': self.category.slug if self.category else None,
            'base_price': self.base_price,
            'discount_price': self.discount_price,
            'effective_price': self.discount_price if (self.discount_price and self.discount_price > 0) else self.base_price,
            'brand': self.brand,
            'material': self.material,
            'fit_type': self.fit_type,
            'care_instructions': self.care_instructions,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'average_rating': round(self.average_rating, 1),
            'review_count': self.review_count,
            'sales_count': self.sales_count,
            'total_stock': self.total_stock,
            'in_stock': self.in_stock,
            'primary_image': self.primary_image,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_details:
            data['images'] = [img.to_dict() for img in self.images]
            data['variants'] = [v.to_dict() for v in self.variants]
            data['available_sizes'] = sorted(list(set(v.size for v in self.variants if v.stock_quantity > 0)))
            
            # Map each color to its exact corresponding photograph
            color_map = {}
            for v in self.variants:
                if v.color not in color_map:
                    # Look for image tagged with this color first
                    matched_img = next((img.image_url for img in self.images if img.color == v.color), None)
                    if not matched_img and self.images:
                        idx = len(color_map) % len(self.images)
                        matched_img = self.images[idx].image_url
                    color_map[v.color] = {
                        'color': v.color,
                        'color_hex': v.color_hex,
                        'image_url': matched_img or self.primary_image
                    }
            data['available_colors'] = list(color_map.values())
        else:
            data['images'] = [img.to_dict() for img in self.images[:1]]
            data['available_sizes'] = list(set(v.size for v in self.variants))
            color_map = {}
            for v in self.variants:
                if v.color not in color_map:
                    matched_img = next((img.image_url for img in self.images if img.color == v.color), None)
                    color_map[v.color] = {
                        'color': v.color,
                        'color_hex': v.color_hex,
                        'image_url': matched_img or self.primary_image
                    }
            data['available_colors'] = list(color_map.values())

        return data


class ProductVariant(db.Model):
    __tablename__ = 'product_variants'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    size = db.Column(db.String(10), nullable=False)   # XS, S, M, L, XL, XXL
    color = db.Column(db.String(50), nullable=False)  # Black, White, Navy, Olive, etc.
    color_hex = db.Column(db.String(10), default='#000000', nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    additional_price = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    cart_items = db.relationship('CartItem', backref='variant', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'size': self.size,
            'color': self.color,
            'color_hex': self.color_hex,
            'sku': self.sku,
            'stock_quantity': self.stock_quantity,
            'additional_price': self.additional_price,
            'in_stock': self.stock_quantity > 0
        }


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    image_url = db.Column(db.String(500), nullable=False)
    color = db.Column(db.String(50), nullable=True)  # Matching color name
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'image_url': self.image_url,
            'color': self.color,
            'is_primary': self.is_primary,
            'display_order': self.display_order
        }


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id', ondelete='CASCADE'), nullable=False, index=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    def to_dict(self):
        product = self.variant.product if self.variant else None
        effective_unit_price = 0.0
        if product:
            base = product.discount_price if (product.discount_price and product.discount_price > 0) else product.base_price
            effective_unit_price = base + (self.variant.additional_price or 0.0)

        return {
            'id': self.id,
            'user_id': self.user_id,
            'variant_id': self.variant_id,
            'quantity': self.quantity,
            'product_id': product.id if product else None,
            'product_name': product.name if product else 'Unknown Product',
            'product_slug': product.slug if product else '',
            'primary_image': product.primary_image if product else '',
            'size': self.variant.size if self.variant else '',
            'color': self.variant.color if self.variant else '',
            'color_hex': self.variant.color_hex if self.variant else '#000',
            'sku': self.variant.sku if self.variant else '',
            'unit_price': effective_unit_price,
            'total_price': round(effective_unit_price * self.quantity, 2),
            'stock_available': self.variant.stock_quantity if self.variant else 0
        }


class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    discount_type = db.Column(db.String(20), default='percentage', nullable=False)  # 'percentage', 'fixed'
    discount_value = db.Column(db.Float, nullable=False)
    min_order_amount = db.Column(db.Float, default=0.0, nullable=False)
    max_discount_amount = db.Column(db.Float, nullable=True)
    usage_limit = db.Column(db.Integer, default=1000, nullable=False)
    times_used = db.Column(db.Integer, default=0, nullable=False)
    valid_from = db.Column(db.DateTime, default=utcnow, nullable=False)
    valid_to = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def is_valid(self, subtotal=0.0):
        if not self.is_active:
            return False, "This coupon is currently inactive."
        now = datetime.now()
        if self.valid_to and self.valid_to < now:
            return False, "This coupon has expired."
        if self.valid_from and self.valid_from > now:
            return False, "This coupon is not valid yet."
        times_used = self.times_used or 0
        usage_limit = self.usage_limit if self.usage_limit is not None else 1000
        if times_used >= usage_limit:
            return False, "This coupon has reached its usage limit."
        min_order = self.min_order_amount or 0.0
        if subtotal < min_order:
            return False, f"Minimum order subtotal of ${min_order:.2f} required."
        return True, "Coupon is valid."

    def calculate_discount(self, subtotal):
        if self.discount_type == 'percentage':
            discount = (self.discount_value / 100.0) * subtotal
            if self.max_discount_amount and discount > self.max_discount_amount:
                discount = self.max_discount_amount
            return round(discount, 2)
        elif self.discount_type == 'fixed':
            discount = min(self.discount_value, subtotal)
            return round(discount, 2)
        return 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'min_order_amount': self.min_order_amount,
            'max_discount_amount': self.max_discount_amount,
            'usage_limit': self.usage_limit,
            'times_used': self.times_used,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_to': self.valid_to.isoformat() if self.valid_to else None,
            'is_active': self.is_active
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)
    coupon_code = db.Column(db.String(50), nullable=True)
    subtotal = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0, nullable=False)
    shipping_amount = db.Column(db.Float, default=0.0, nullable=False)
    tax_amount = db.Column(db.Float, default=0.0, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='pending', nullable=False)  # pending, processing, shipped, delivered, cancelled
    payment_status = db.Column(db.String(30), default='pending', nullable=False)  # pending, paid, failed, refunded
    payment_method = db.Column(db.String(50), default='card', nullable=False)  # card, upi, netbanking, cod
    tracking_number = db.Column(db.String(100), nullable=True)
    carrier_name = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan', lazy=True)
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    delivery_address = db.relationship('Address', foreign_keys=[address_id])
    return_requests = db.relationship('ReturnRequest', backref='order', cascade='all, delete-orphan', lazy=True)

    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'customer_name': self.user.full_name if self.user else 'Customer',
            'customer_email': self.user.email if self.user else '',
            'customer_code': self.user.customer_code if self.user else f"AUR-CUST-{self.user_id:04d}",
            'address_id': self.address_id,
            'delivery_address': self.delivery_address.to_dict() if self.delivery_address else None,
            'coupon_code': self.coupon_code,
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'shipping_amount': self.shipping_amount,
            'tax_amount': self.tax_amount,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'tracking_number': self.tracking_number,
            'carrier_name': self.carrier_name,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'item_count': sum(item.quantity for item in self.items) if self.items else 0
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
            data['return_requests'] = [req.to_dict() for req in self.return_requests]
        return data


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    variant_size = db.Column(db.String(10), nullable=False)
    variant_color = db.Column(db.String(50), nullable=False)
    sku = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'variant_id': self.variant_id,
            'product_name': self.product_name,
            'variant_size': self.variant_size,
            'variant_color': self.variant_color,
            'sku': self.sku,
            'image_url': self.image_url,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'total_price': self.total_price
        }


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # card, upi, netbanking, cod
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='completed', nullable=False)  # pending, completed, failed, refunded
    payment_details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    title = db.Column(db.String(150), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    is_verified_purchase = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else 'Anonymous',
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'is_verified_purchase': self.is_verified_purchase,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(30), default='order', nullable=False)  # order, promo, account, system
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    link_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'link_url': self.link_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ReturnRequest(db.Model):
    __tablename__ = 'return_requests'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    request_type = db.Column(db.String(30), nullable=False)  # 'cancellation', 'return', 'refund'
    reason = db.Column(db.String(255), nullable=False)
    customer_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='pending', nullable=False)  # 'pending', 'approved', 'rejected'
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'order_number': self.order.order_number if self.order else None,
            'user_id': self.user_id,
            'customer_name': self.user.full_name if self.user else 'Customer',
            'customer_email': self.user.email if self.user else '',
            'customer_code': self.user.customer_code if self.user else f"AUR-CUST-{self.user_id:04d}",
            'request_type': self.request_type,
            'reason': self.reason,
            'customer_notes': self.customer_notes,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
