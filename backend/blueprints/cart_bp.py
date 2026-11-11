from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, CartItem, ProductVariant, Coupon
from config import Config

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = int(get_jwt_identity())
    items = CartItem.query.filter_by(user_id=user_id).all()

    subtotal = sum(item.to_dict()['total_price'] for item in items)
    tax = round(subtotal * Config.TAX_RATE, 2)
    shipping = 0.0 if (subtotal >= Config.FREE_SHIPPING_THRESHOLD or subtotal == 0) else Config.DEFAULT_SHIPPING_FEE
    total = round(subtotal + tax + shipping, 2)

    return jsonify({
        'items': [item.to_dict() for item in items],
        'summary': {
            'item_count': sum(item.quantity for item in items),
            'subtotal': round(subtotal, 2),
            'tax': tax,
            'shipping': shipping,
            'free_shipping_threshold': Config.FREE_SHIPPING_THRESHOLD,
            'qualifies_for_free_shipping': subtotal >= Config.FREE_SHIPPING_THRESHOLD,
            'total': total
        }
    }), 200

@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    variant_id = data.get('variant_id')
    quantity = data.get('quantity', 1)

    if not variant_id:
        return jsonify({'error': 'variant_id is required'}), 400

    try:
        quantity = int(quantity)
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be at least 1'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity'}), 400

    variant = ProductVariant.query.get(variant_id)
    if not variant:
        return jsonify({'error': 'Product variant not found'}), 404

    # Check existing item in user cart
    cart_item = CartItem.query.filter_by(user_id=user_id, variant_id=variant_id).first()
    new_quantity = (cart_item.quantity + quantity) if cart_item else quantity

    if variant.stock_quantity < new_quantity:
        return jsonify({
            'error': f'Only {variant.stock_quantity} units available in stock for this size and color.'
        }), 400

    if cart_item:
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(user_id=user_id, variant_id=variant_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({
        'message': 'Item added to cart',
        'item': cart_item.to_dict()
    }), 201

@cart_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_cart_item(id):
    user_id = int(get_jwt_identity())
    cart_item = CartItem.query.filter_by(id=id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    data = request.get_json() or {}
    try:
        new_quantity = int(data.get('quantity', 1))
        if new_quantity <= 0:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'message': 'Item removed from cart'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid quantity'}), 400

    variant = cart_item.variant
    if variant and variant.stock_quantity < new_quantity:
        return jsonify({
            'error': f'Only {variant.stock_quantity} units available in stock.'
        }), 400

    cart_item.quantity = new_quantity
    db.session.commit()
    return jsonify({
        'message': 'Cart updated',
        'item': cart_item.to_dict()
    }), 200

@cart_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(id):
    user_id = int(get_jwt_identity())
    cart_item = CartItem.query.filter_by(id=id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200

@cart_bp.route('', methods=['DELETE'])
@jwt_required()
def clear_cart():
    user_id = int(get_jwt_identity())
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared'}), 200
