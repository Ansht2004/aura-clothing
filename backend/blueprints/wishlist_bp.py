from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, WishlistItem, Product

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/api/wishlist')

@wishlist_bp.route('', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = int(get_jwt_identity())
    items = WishlistItem.query.filter_by(user_id=user_id).order_by(WishlistItem.created_at.desc()).all()
    return jsonify({
        'wishlist': [item.to_dict() for item in items]
    }), 200

@wishlist_bp.route('/toggle', methods=['POST'])
@jwt_required()
def toggle_wishlist():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    existing = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'message': 'Removed from wishlist', 'in_wishlist': False}), 200
    else:
        new_item = WishlistItem(user_id=user_id, product_id=product_id)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Added to wishlist', 'in_wishlist': True}), 201

@wishlist_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(product_id):
    user_id = int(get_jwt_identity())
    item = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        return jsonify({'error': 'Item not found in wishlist'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Removed from wishlist', 'in_wishlist': False}), 200
