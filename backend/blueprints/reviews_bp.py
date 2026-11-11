from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Review, Product, Order, OrderItem

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api')

@reviews_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return jsonify({
        'product_id': product_id,
        'average_rating': product.average_rating,
        'review_count': product.review_count,
        'reviews': [r.to_dict() for r in reviews]
    }), 200

@reviews_bp.route('/products/<int:product_id>/reviews', methods=['POST'])
@jwt_required()
def add_product_review(product_id):
    user_id = int(get_jwt_identity())
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}
    rating = data.get('rating')
    title = data.get('title', '').strip()
    comment = data.get('comment', '').strip()

    try:
        rating = int(rating)
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be an integer between 1 and 5.'}), 400
    except (TypeError, ValueError):
        return jsonify({'error': 'Rating must be between 1 and 5.'}), 400

    if not title or not comment:
        return jsonify({'error': 'Title and comment are required.'}), 400

    # Prevent duplicate reviews from the same user for the same product
    existing = Review.query.filter_by(product_id=product_id, user_id=user_id).first()
    if existing:
        return jsonify({'error': 'You have already submitted a review for this product.'}), 400

    # Check verified purchase
    user_orders = Order.query.filter_by(user_id=user_id).all()
    order_ids = [o.id for o in user_orders]
    is_verified = False
    if order_ids:
        has_purchased = OrderItem.query.filter(
            OrderItem.order_id.in_(order_ids),
            OrderItem.product_id == product_id
        ).first()
        is_verified = has_purchased is not None

    review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        title=title,
        comment=comment,
        is_verified_purchase=is_verified
    )
    db.session.add(review)
    db.session.flush()

    # Recalculate product average rating & review count
    all_reviews = Review.query.filter_by(product_id=product_id).all()
    product.review_count = len(all_reviews)
    product.average_rating = round(sum(r.rating for r in all_reviews) / len(all_reviews), 2)

    db.session.commit()

    return jsonify({
        'message': 'Review submitted successfully!',
        'review': review.to_dict()
    }), 201
