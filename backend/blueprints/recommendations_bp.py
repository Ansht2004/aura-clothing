from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import Product
from services.recommendation_service import recommendation_engine

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@recommendations_bp.route('/personalized', methods=['GET'])
def personalized_recommendations():
    limit = request.args.get('limit', 8, type=int)
    user_id = None

    try:
        verify_jwt_in_request(optional=True)
        jwt_identity = get_jwt_identity()
        if jwt_identity:
            user_id = int(jwt_identity)
    except Exception:
        user_id = None

    if user_id:
        recommendations = recommendation_engine.get_personalized_recommendations(user_id=user_id, limit=limit)
    else:
        # Fallback to high-rated items
        items = Product.query.filter_by(is_active=True).order_by(
            Product.average_rating.desc(), 
            Product.sales_count.desc()
        ).limit(limit).all()
        recommendations = [{'product': p.to_dict(), 'score': round(p.average_rating / 5.0, 3), 'breakdown': {}} for p in items]

    return jsonify({
        'user_id': user_id,
        'algorithm': 'weighted-multivariate-ranking',
        'recommendations': recommendations
    }), 200

@recommendations_bp.route('/trending', methods=['GET'])
def trending_products():
    limit = request.args.get('limit', 8, type=int)
    trending = Product.query.filter_by(is_active=True).order_by(
        Product.sales_count.desc(),
        Product.average_rating.desc()
    ).limit(limit).all()

    return jsonify({
        'trending': [p.to_dict() for p in trending]
    }), 200
