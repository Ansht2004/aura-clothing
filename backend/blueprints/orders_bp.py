from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderItem, Payment, CartItem, ProductVariant, Address, Coupon, Notification, ReturnRequest
from services.inventory_service import inventory_service
from config import Config
import uuid
from datetime import datetime, timezone

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

def generate_order_number():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    unique_suffix = uuid.uuid4().hex[:6].upper()
    return f"AUR-{timestamp}-{unique_suffix}"

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify({'orders': [o.to_dict(include_items=True) for o in orders]}), 200

@orders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    data = order.to_dict(include_items=True)
    if order.payment:
        data['payment'] = order.payment.to_dict()
    return jsonify({'order': data}), 200

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    address_id = data.get('address_id')
    payment_method = data.get('payment_method', 'card')
    coupon_code = data.get('coupon_code', '').strip().upper()
    order_notes = data.get('notes', '').strip()

    # Verify address belongs to user
    address = Address.query.filter_by(id=address_id, user_id=user_id).first()
    if not address:
        return jsonify({'error': 'Please select a valid delivery address.'}), 400

    # Retrieve items either from cart or direct purchase
    direct_items = data.get('items')
    order_items_data = []

    if direct_items and isinstance(direct_items, list) and len(direct_items) > 0:
        for it in direct_items:
            variant = ProductVariant.query.get(it.get('variant_id'))
            if not variant:
                return jsonify({'error': f"Variant ID {it.get('variant_id')} not found."}), 404
            order_items_data.append({
                'variant': variant,
                'quantity': it.get('quantity', 1)
            })
    else:
        # Use user's cart
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({'error': 'Your cart is empty. Add items before checkout.'}), 400

        for ci in cart_items:
            order_items_data.append({
                'variant': ci.variant,
                'quantity': ci.quantity
            })

    # Validate inventory availability
    inventory_items = [{'variant_id': item['variant'].id, 'quantity': item['quantity']} for item in order_items_data]
    available, err_msgs = inventory_service.check_availability(inventory_items)
    if not available:
        return jsonify({'error': 'Stock availability error', 'details': err_msgs}), 400

    # Calculate Subtotal
    subtotal = 0.0
    prepared_items = []
    for item in order_items_data:
        variant = item['variant']
        product = variant.product
        qty = item['quantity']
        unit_price = product.discount_price if (product.discount_price and product.discount_price > 0) else product.base_price
        unit_price += (variant.additional_price or 0.0)
        item_total = round(unit_price * qty, 2)
        subtotal += item_total

        prepared_items.append({
            'product_id': product.id,
            'variant_id': variant.id,
            'product_name': product.name,
            'variant_size': variant.size,
            'variant_color': variant.color,
            'sku': variant.sku,
            'image_url': product.primary_image,
            'unit_price': unit_price,
            'quantity': qty,
            'total_price': item_total
        })

    subtotal = round(subtotal, 2)

    # Coupon discount
    discount_amount = 0.0
    coupon = None
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code).first()
        if coupon:
            is_valid, _ = coupon.is_valid(subtotal=subtotal)
            if is_valid:
                discount_amount = coupon.calculate_discount(subtotal=subtotal)
                coupon.times_used += 1

    # Tax & Shipping
    tax_amount = round(max(0.0, subtotal - discount_amount) * Config.TAX_RATE, 2)
    shipping_amount = 0.0 if (subtotal >= Config.FREE_SHIPPING_THRESHOLD or subtotal == 0) else Config.DEFAULT_SHIPPING_FEE
    final_total = round(max(0.0, subtotal - discount_amount) + tax_amount + shipping_amount, 2)

    try:
        # Atomic inventory deduction
        inventory_service.reserve_and_deduct(inventory_items)

        # Create Order
        order_num = generate_order_number()
        new_order = Order(
            order_number=order_num,
            user_id=user_id,
            address_id=address.id,
            coupon_code=coupon_code if discount_amount > 0 else None,
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping_amount=shipping_amount,
            tax_amount=tax_amount,
            total_amount=final_total,
            status='processing',
            payment_status='paid' if payment_method != 'cod' else 'pending',
            payment_method=payment_method,
            carrier_name='Aura Express Logistics',
            tracking_number=f"TRK-{uuid.uuid4().hex[:10].upper()}",
            notes=order_notes
        )
        db.session.add(new_order)
        db.session.flush()

        # Add Order Items
        for pi in prepared_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=pi['product_id'],
                variant_id=pi['variant_id'],
                product_name=pi['product_name'],
                variant_size=pi['variant_size'],
                variant_color=pi['variant_color'],
                sku=pi['sku'],
                image_url=pi['image_url'],
                unit_price=pi['unit_price'],
                quantity=pi['quantity'],
                total_price=pi['total_price']
            )
            db.session.add(order_item)

        # Create Payment Record
        txn_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        payment = Payment(
            order_id=new_order.id,
            user_id=user_id,
            payment_method=payment_method,
            transaction_id=txn_id,
            amount=final_total,
            status='completed' if payment_method != 'cod' else 'pending',
            payment_details=f"Payment via {payment_method.upper()}"
        )
        db.session.add(payment)

        # Clear cart if items came from cart
        if not direct_items:
            CartItem.query.filter_by(user_id=user_id).delete()

        # Order Confirmation Notification
        notif = Notification(
            user_id=user_id,
            title=f"Order Confirmed: {order_num}",
            message=f"Thank you! Your order {order_num} of ₹{final_total:,.2f} has been confirmed and is being prepared.",
            type="order",
            link_url=f"/orders/{new_order.id}"
        )
        db.session.add(notif)

        db.session.commit()

        return jsonify({
            'message': 'Order placed successfully!',
            'order': new_order.to_dict(include_items=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process order', 'details': str(e)}), 500

@orders_bp.route('/<int:id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if order.status in ['shipped', 'delivered', 'cancelled']:
        return jsonify({'error': f"Cannot cancel order that is already {order.status}."}), 400

    data = request.get_json() or {}
    reason = data.get('reason', 'Customer requested cancellation')

    try:
        # Restore inventory
        items_to_restore = [{'variant_id': item.variant_id, 'quantity': item.quantity} for item in order.items]
        inventory_service.restore_stock(items_to_restore)

        order.status = 'cancelled'
        if order.payment and order.payment.status == 'completed':
            order.payment_status = 'refunded'
            order.payment.status = 'refunded'

        # Record cancellation request
        req = ReturnRequest(
            order_id=order.id,
            user_id=user_id,
            request_type='cancellation',
            reason=reason,
            status='approved',
            admin_notes='Order cancelled automatically prior to dispatch.'
        )
        db.session.add(req)

        # Notification
        notif = Notification(
            user_id=user_id,
            title=f"Order Cancelled: {order.order_number}",
            message=f"Order {order.order_number} has been cancelled successfully. Any payment made will be refunded within 3-5 business days.",
            type="order",
            link_url=f"/orders/{order.id}"
        )
        db.session.add(notif)

        db.session.commit()
        return jsonify({'message': 'Order cancelled successfully', 'order': order.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel order', 'details': str(e)}), 500

@orders_bp.route('/<int:id>/return-request', methods=['POST'])
@jwt_required()
def submit_return_request(id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if order.status != 'delivered':
        return jsonify({'error': 'Return or refund requests can only be placed for delivered orders.'}), 400

    data = request.get_json() or {}
    request_type = data.get('request_type', 'return')  # 'return', 'refund'
    reason = data.get('reason', '').strip()
    notes = data.get('customer_notes', '').strip()

    if not reason:
        return jsonify({'error': 'Please provide a reason for return/refund.'}), 400

    existing = ReturnRequest.query.filter_by(order_id=order.id, status='pending').first()
    if existing:
        return jsonify({'error': 'A pending request already exists for this order.'}), 400

    ret_req = ReturnRequest(
        order_id=order.id,
        user_id=user_id,
        request_type=request_type,
        reason=reason,
        customer_notes=notes,
        status='pending'
    )
    db.session.add(ret_req)

    notif = Notification(
        user_id=user_id,
        title=f"{request_type.capitalize()} Request Submitted: {order.order_number}",
        message=f"Your {request_type} request for order {order.order_number} has been received and is under review.",
        type="order",
        link_url=f"/orders/{order.id}"
    )
    db.session.add(notif)

    db.session.commit()
    return jsonify({
        'message': f"{request_type.capitalize()} request submitted successfully. Our team will review it within 24 hours.",
        'request': ret_req.to_dict()
    }), 201

@orders_bp.route('/<int:id>/invoice', methods=['GET'])
@jwt_required()
def get_invoice(id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({
        'invoice_number': f"INV-{order.order_number}",
        'date': order.created_at.strftime('%B %d, %Y'),
        'company': {
            'name': 'Aura Apparel Co.',
            'tax_id': 'US-983471029',
            'support_email': 'support@auraapparel.com',
            'address': '742 Evergreen Terrace, Suite 100, New York, NY 10001'
        },
        'customer': {
            'name': order.user.full_name,
            'email': order.user.email,
            'phone': order.user.phone
        },
        'order': order.to_dict(include_items=True)
    }), 200
