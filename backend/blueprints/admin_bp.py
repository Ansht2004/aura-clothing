from flask import Blueprint, request, jsonify
from models import (
    db, User, Product, ProductVariant, ProductImage, 
    Category, Coupon, Order, OrderItem, Payment, 
    ReturnRequest, Notification
)
from blueprints.auth_bp import admin_required
from services.inventory_service import inventory_service
from datetime import datetime, timezone
import re

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text)

# ----------------------------------------------------
# 1. Metrics & Overview
# ----------------------------------------------------
@admin_bp.route('/metrics', methods=['GET'])
@admin_required()
def get_metrics():
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.status != 'cancelled'
    ).scalar() or 0.0

    total_orders = Order.query.count()
    total_customers = User.query.filter_by(role='customer').count()
    total_products = Product.query.count()

    # Order status breakdown
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    status_counts = {}
    for st in statuses:
        status_counts[st] = Order.query.filter_by(status=st).count()

    # Low stock variants (< 10 units)
    low_stock_count = ProductVariant.query.filter(ProductVariant.stock_quantity <= 10).count()

    # Pending return requests
    pending_requests_count = ReturnRequest.query.filter_by(status='pending').count()

    # Recent 6 orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(6).all()

    return jsonify({
        'overview': {
            'total_revenue': round(total_revenue, 2),
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_products': total_products,
            'low_stock_count': low_stock_count,
            'pending_requests_count': pending_requests_count
        },
        'status_breakdown': status_counts,
        'recent_orders': [o.to_dict(include_items=False) for o in recent_orders]
    }), 200

# ----------------------------------------------------
# 2. Product Management (CRUD)
# ----------------------------------------------------
@admin_bp.route('/products', methods=['GET'])
@admin_required()
def admin_list_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()

    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    pagination = query.order_by(Product.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'products': [p.to_dict(include_details=True) for p in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages
        }
    }), 200

@admin_bp.route('/products', methods=['POST'])
@admin_required()
def admin_create_product():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    category_id = data.get('category_id')
    base_price = float(data.get('base_price', 0))
    discount_price = float(data.get('discount_price', 0)) if data.get('discount_price') else None
    description = data.get('description', '').strip()
    brand = data.get('brand', 'Aura Apparel').strip()
    material = data.get('material', '').strip()
    fit_type = data.get('fit_type', 'Regular').strip()
    is_featured = bool(data.get('is_featured', False))
    image_url = data.get('image_url', '').strip()

    if not name or not category_id or base_price <= 0:
        return jsonify({'error': 'Name, valid category, and positive base price are required.'}), 400

    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while Product.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    product = Product(
        name=name,
        slug=slug,
        category_id=category_id,
        base_price=base_price,
        discount_price=discount_price,
        description=description,
        brand=brand,
        material=material,
        fit_type=fit_type,
        is_featured=is_featured
    )
    db.session.add(product)
    db.session.flush()

    # Add primary image if provided
    if image_url:
        img = ProductImage(product_id=product.id, image_url=image_url, is_primary=True, display_order=1)
        db.session.add(img)

    # Add default variants if provided
    variants_data = data.get('variants', [])
    if variants_data:
        for v in variants_data:
            sku = f"{product.slug[:4].upper()}-{v.get('size')}-{v.get('color')[:3].upper()}"
            var = ProductVariant(
                product_id=product.id,
                size=v.get('size', 'M'),
                color=v.get('color', 'Standard'),
                color_hex=v.get('color_hex', '#333333'),
                sku=v.get('sku', sku),
                stock_quantity=int(v.get('stock_quantity', 10)),
                additional_price=float(v.get('additional_price', 0.0))
            )
            db.session.add(var)
    else:
        # Default standard variants
        for s in ['S', 'M', 'L']:
            var = ProductVariant(
                product_id=product.id,
                size=s,
                color='Classic',
                color_hex='#2B2D42',
                sku=f"{product.slug[:4].upper()}-{s}-CLS",
                stock_quantity=15
            )
            db.session.add(var)

    db.session.commit()
    return jsonify({'message': 'Product created successfully', 'product': product.to_dict(include_details=True)}), 201

@admin_bp.route('/products/<int:id>', methods=['PUT'])
@admin_required()
def admin_update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}
    if 'name' in data:
        product.name = data['name'].strip()
    if 'category_id' in data:
        product.category_id = data['category_id']
    if 'base_price' in data:
        product.base_price = float(data['base_price'])
    if 'discount_price' in data:
        product.discount_price = float(data['discount_price']) if data['discount_price'] else None
    if 'description' in data:
        product.description = data['description'].strip()
    if 'brand' in data:
        product.brand = data['brand'].strip()
    if 'material' in data:
        product.material = data['material'].strip()
    if 'fit_type' in data:
        product.fit_type = data['fit_type'].strip()
    if 'is_featured' in data:
        product.is_featured = bool(data['is_featured'])
    if 'is_active' in data:
        product.is_active = bool(data['is_active'])

    # Update or add primary image
    if 'image_url' in data and data['image_url']:
        prim_img = ProductImage.query.filter_by(product_id=product.id, is_primary=True).first()
        if prim_img:
            prim_img.image_url = data['image_url']
        else:
            new_img = ProductImage(product_id=product.id, image_url=data['image_url'], is_primary=True)
            db.session.add(new_img)

    db.session.commit()
    return jsonify({'message': 'Product updated successfully', 'product': product.to_dict(include_details=True)}), 200

@admin_bp.route('/products/<int:id>', methods=['DELETE'])
@admin_required()
def admin_delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

# ----------------------------------------------------
# 3. Inventory Management
# ----------------------------------------------------
@admin_bp.route('/inventory', methods=['GET'])
@admin_required()
def admin_get_inventory():
    variants = ProductVariant.query.join(Product).order_by(ProductVariant.stock_quantity.asc()).all()
    return jsonify({
        'inventory': [
            {
                'id': v.id,
                'product_id': v.product_id,
                'product_name': v.product.name if v.product else 'Unknown',
                'sku': v.sku,
                'size': v.size,
                'color': v.color,
                'color_hex': v.color_hex,
                'stock_quantity': v.stock_quantity,
                'additional_price': v.additional_price,
                'is_low_stock': v.stock_quantity <= 10
            } for v in variants
        ]
    }), 200

@admin_bp.route('/inventory/<int:variant_id>', methods=['PUT'])
@admin_required()
def admin_update_stock(variant_id):
    variant = ProductVariant.query.get(variant_id)
    if not variant:
        return jsonify({'error': 'Variant not found'}), 404

    data = request.get_json() or {}
    if 'stock_quantity' in data:
        try:
            variant.stock_quantity = max(0, int(data['stock_quantity']))
        except ValueError:
            return jsonify({'error': 'Invalid stock quantity'}), 400

    if 'additional_price' in data:
        try:
            variant.additional_price = max(0.0, float(data['additional_price']))
        except ValueError:
            return jsonify({'error': 'Invalid additional price'}), 400

    db.session.commit()
    return jsonify({
        'message': 'Stock updated successfully',
        'variant': variant.to_dict()
    }), 200

@admin_bp.route('/products/<int:product_id>/variants', methods=['POST'])
@admin_required()
def admin_add_variant(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}
    size = data.get('size', 'M').strip()
    color = data.get('color', 'Standard').strip()
    color_hex = data.get('color_hex', '#000000').strip()
    stock = int(data.get('stock_quantity', 10))
    add_price = float(data.get('additional_price', 0.0))

    sku = data.get('sku', '').strip()
    if not sku:
        sku = f"{product.slug[:4].upper()}-{size}-{color[:3].upper()}-{ProductVariant.query.count() + 1}"

    variant = ProductVariant(
        product_id=product.id,
        size=size,
        color=color,
        color_hex=color_hex,
        sku=sku,
        stock_quantity=stock,
        additional_price=add_price
    )
    db.session.add(variant)
    db.session.commit()

    return jsonify({'message': 'Variant added successfully', 'variant': variant.to_dict()}), 201

# ----------------------------------------------------
# 4. Categories Management
# ----------------------------------------------------
@admin_bp.route('/categories', methods=['POST'])
@admin_required()
def admin_create_category():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    image_url = data.get('image_url', '').strip()
    is_featured = bool(data.get('is_featured', False))

    if not name:
        return jsonify({'error': 'Category name is required.'}), 400

    slug = slugify(name)
    if Category.query.filter_by(slug=slug).first():
        return jsonify({'error': 'A category with this name or slug already exists.'}), 409

    category = Category(
        name=name,
        slug=slug,
        description=description,
        image_url=image_url,
        is_featured=is_featured
    )
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully', 'category': category.to_dict()}), 201

@admin_bp.route('/categories/<int:id>', methods=['PUT'])
@admin_required()
def admin_update_category(id):
    cat = Category.query.get(id)
    if not cat:
        return jsonify({'error': 'Category not found'}), 404

    data = request.get_json() or {}
    if 'name' in data:
        cat.name = data['name'].strip()
    if 'description' in data:
        cat.description = data['description'].strip()
    if 'image_url' in data:
        cat.image_url = data['image_url'].strip()
    if 'is_featured' in data:
        cat.is_featured = bool(data['is_featured'])

    db.session.commit()
    return jsonify({'message': 'Category updated successfully', 'category': cat.to_dict()}), 200

# ----------------------------------------------------
# 5. Coupon Management
# ----------------------------------------------------
@admin_bp.route('/coupons', methods=['GET'])
@admin_required()
def admin_list_coupons():
    coupons = Coupon.query.order_by(Coupon.id.desc()).all()
    return jsonify({'coupons': [c.to_dict() for c in coupons]}), 200

@admin_bp.route('/coupons', methods=['POST'])
@admin_required()
def admin_create_coupon():
    data = request.get_json() or {}
    code = data.get('code', '').strip().upper()
    discount_type = data.get('discount_type', 'percentage')
    discount_value = float(data.get('discount_value', 10))
    min_order_amount = float(data.get('min_order_amount', 0))
    max_discount_amount = float(data.get('max_discount_amount')) if data.get('max_discount_amount') else None
    usage_limit = int(data.get('usage_limit', 500))

    if not code:
        return jsonify({'error': 'Coupon code is required'}), 400

    if Coupon.query.filter_by(code=code).first():
        return jsonify({'error': 'Coupon code already exists'}), 409

    coupon = Coupon(
        code=code,
        discount_type=discount_type,
        discount_value=discount_value,
        min_order_amount=min_order_amount,
        max_discount_amount=max_discount_amount,
        usage_limit=usage_limit,
        is_active=True
    )
    db.session.add(coupon)
    db.session.commit()

    return jsonify({'message': 'Coupon created successfully', 'coupon': coupon.to_dict()}), 201

# ----------------------------------------------------
# 6. Orders Management & Status Updates
# ----------------------------------------------------
@admin_bp.route('/orders', methods=['GET'])
@admin_required()
def admin_list_orders():
    status = request.args.get('status')
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Order.query
    if status:
        query = query.filter(Order.status == status)
    if search:
        query = query.filter(
            db.or_(
                Order.order_number.ilike(f"%{search}%"),
                Order.tracking_number.ilike(f"%{search}%")
            )
        )

    pagination = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'orders': [o.to_dict(include_items=True) for o in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages
        }
    }), 200

@admin_bp.route('/orders/<int:id>/status', methods=['PUT'])
@admin_required()
def admin_update_order_status(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json() or {}
    new_status = data.get('status')
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

    if new_status not in valid_statuses:
        return jsonify({'error': f"Invalid status. Choose from: {', '.join(valid_statuses)}"}), 400

    old_status = order.status
    order.status = new_status

    if 'tracking_number' in data and data['tracking_number']:
        order.tracking_number = data['tracking_number'].strip()
    if 'carrier_name' in data and data['carrier_name']:
        order.carrier_name = data['carrier_name'].strip()

    # If status transitioned to delivered, mark payment as paid if cod
    if new_status == 'delivered' and order.payment_status == 'pending':
        order.payment_status = 'paid'
        if order.payment:
            order.payment.status = 'completed'

    # If transitioning to cancelled, restore stock
    if new_status == 'cancelled' and old_status != 'cancelled':
        items_to_restore = [{'variant_id': item.variant_id, 'quantity': item.quantity} for item in order.items]
        inventory_service.restore_stock(items_to_restore)
        if order.payment and order.payment.status == 'completed':
            order.payment_status = 'refunded'
            order.payment.status = 'refunded'

    # Customer notification
    notif = Notification(
        user_id=order.user_id,
        title=f"Order Status Update: {order.order_number}",
        message=f"Your order status has changed to '{new_status.capitalize()}'. Tracking: {order.tracking_number or 'In progress'}.",
        type="order",
        link_url=f"/orders/{order.id}"
    )
    db.session.add(notif)

    db.session.commit()
    return jsonify({'message': f'Order status updated to {new_status}', 'order': order.to_dict()}), 200

# ----------------------------------------------------
# 7. Review & Process Cancellation, Return & Refund Requests
# ----------------------------------------------------
@admin_bp.route('/requests', methods=['GET'])
@admin_required()
def admin_list_requests():
    requests = ReturnRequest.query.order_by(ReturnRequest.created_at.desc()).all()
    return jsonify({'requests': [r.to_dict() for r in requests]}), 200

@admin_bp.route('/requests/<int:id>', methods=['PUT'])
@admin_required()
def admin_process_request(id):
    req = ReturnRequest.query.get(id)
    if not req:
        return jsonify({'error': 'Request not found'}), 404

    data = request.get_json() or {}
    action = data.get('action')  # 'approve', 'reject'
    admin_notes = data.get('admin_notes', '').strip()

    if action not in ['approve', 'reject']:
        return jsonify({'error': "Action must be 'approve' or 'reject'"}), 400

    new_status = 'approved' if action == 'approve' else 'rejected'
    req.status = new_status
    req.admin_notes = admin_notes
    req.updated_at = datetime.now(timezone.utc)

    order = req.order
    if action == 'approve':
        if req.request_type == 'cancellation':
            order.status = 'cancelled'
            items_to_restore = [{'variant_id': item.variant_id, 'quantity': item.quantity} for item in order.items]
            inventory_service.restore_stock(items_to_restore)
            order.payment_status = 'refunded'
            if order.payment:
                order.payment.status = 'refunded'

        elif req.request_type in ['return', 'refund']:
            order.payment_status = 'refunded'
            if order.payment:
                order.payment.status = 'refunded'
            # Restore inventory upon return approval
            items_to_restore = [{'variant_id': item.variant_id, 'quantity': item.quantity} for item in order.items]
            inventory_service.restore_stock(items_to_restore)

    # Customer notification
    notif = Notification(
        user_id=req.user_id,
        title=f"{req.request_type.capitalize()} Request {new_status.capitalize()}",
        message=f"Your {req.request_type} request for order {order.order_number} has been {new_status}. {admin_notes}",
        type="order",
        link_url=f"/orders/{order.id}"
    )
    db.session.add(notif)

    db.session.commit()
    return jsonify({
        'message': f'Request {new_status} successfully',
        'request': req.to_dict()
    }), 200

# ----------------------------------------------------
# 8. Customers Directory
# ----------------------------------------------------
@admin_bp.route('/customers', methods=['GET'])
@admin_required()
def admin_list_customers():
    customers = User.query.filter_by(role='customer').order_by(User.created_at.desc()).all()
    results = []
    for c in customers:
        order_count = Order.query.filter_by(user_id=c.id).count()
        total_spent = db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.user_id == c.id, 
            Order.status != 'cancelled'
        ).scalar() or 0.0
        results.append({
            'id': c.id,
            'customer_code': c.customer_code,
            'full_name': c.full_name,
            'email': c.email,
            'phone': c.phone,
            'created_at': c.created_at.isoformat() if c.created_at else None,
            'order_count': order_count,
            'total_spent': round(total_spent, 2)
        })

    return jsonify({'customers': results}), 200
